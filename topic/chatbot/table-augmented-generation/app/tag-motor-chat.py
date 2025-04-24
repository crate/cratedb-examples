import os
import pandas as pd
from crate import client
from openai import OpenAI
from dotenv import load_dotenv
import datetime
import re
from dateutil import parser as date_parser

# === Load environment variables ===
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CRATEDB_HOST = os.getenv("CRATEDB_HOST")
CRATEDB_PORT = os.getenv("CRATEDB_PORT")
CRATEDB_USER = os.getenv("CRATEDB_USER")
CRATEDB_PASSWORD = os.getenv("CRATEDB_PASSWORD")
CRATEDB_SCHEMA = os.getenv("CRATEDB_SCHEMA")
ANOMALY_THRESHOLD = 1.5

client_ai = OpenAI(api_key=OPENAI_API_KEY)


# === Fetch Table Schema ===
def fetch_table_schema(table_name):
    connection = client.connect(
        f"https://{CRATEDB_HOST}:{CRATEDB_PORT}",
        username=CRATEDB_USER,
        password=CRATEDB_PASSWORD
    )
    cursor = connection.cursor()
    query = f"""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = '{CRATEDB_SCHEMA}' AND table_name = 'motor_readings'
    ORDER BY ordinal_position
    """
    cursor.execute(query)
    columns = cursor.fetchall()
    connection.close()
    schema_text = f"Table: {table_name}\nColumns:\n"
    for col_name, data_type in columns:
        schema_text += f"- {col_name} ({data_type})\n"
    return schema_text


# === Fetch Time Series Data ===
def fetch_timeseries_data(limit=1000):
    connection = client.connect(
        f"https://{CRATEDB_HOST}:{CRATEDB_PORT}",
        username=CRATEDB_USER,
        password=CRATEDB_PASSWORD
    )
    cursor = connection.cursor()
    query = f"""
    SELECT machine_id, timestamp, vibration, temperature, rotations
    FROM {CRATEDB_SCHEMA}.motor_readings
    ORDER BY timestamp DESC
    LIMIT {limit}
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=["machine_id", "timestamp", "vibration", "temperature", "rotations"])
    connection.close()
    return df


# === Fetch Machine Manual ===
def fetch_machine_manual(machine_id):
    connection = client.connect(
        f"https://{CRATEDB_HOST}:{CRATEDB_PORT}",
        username=CRATEDB_USER,
        password=CRATEDB_PASSWORD
    )
    cursor = connection.cursor()
    query = f"""
    SELECT manual FROM {CRATEDB_SCHEMA}.machine_manuals WHERE machine_id = ?
    """
    cursor.execute(query, (machine_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None


# === Extract Anomaly Section from Manual ===
def extract_anomaly_info(manual):
    anomaly_section = re.search(r"\*\*Anomaly Detection:\*\*(.*?)---", manual, re.DOTALL)
    emergency_section = re.search(r"\*\*Emergency Protocol:\*\*(.*?)---", manual, re.DOTALL)
    anomaly_text = anomaly_section.group(1).strip() if anomaly_section else "No anomaly info found."
    emergency_text = emergency_section.group(1).strip() if emergency_section else "No emergency protocol found."
    return anomaly_text, emergency_text


# === Generate Data Profile ===
def generate_data_profile(df):
    anomalies = df[df["vibration"] > ANOMALY_THRESHOLD]
    min_ts = datetime.datetime.fromtimestamp(df['timestamp'].min() / 1000)
    max_ts = datetime.datetime.fromtimestamp(df['timestamp'].max() / 1000)
    machine_ids = sorted(df['machine_id'].unique().tolist(), reverse=True)

    profile = f"""
Data Overview:
- Total readings: {len(df)}
- Time range: {min_ts.strftime('%Y-%m-%d %H:%M:%S')} to {max_ts.strftime('%Y-%m-%d %H:%M:%S')}
- Machines: {machine_ids}
- Vibration range: {df['vibration'].min():.2f} to {df['vibration'].max():.2f}
- Temperature range: {df['temperature'].min():.2f}°C to {df['temperature'].max():.2f}°C
- Rotations range: {df['rotations'].min():.0f} RPM to {df['rotations'].max():.0f} RPM
- Anomalies (vibration > {ANOMALY_THRESHOLD}): {len(anomalies)}
"""
    if not anomalies.empty:
        for machine_id in anomalies['machine_id'].unique():
            manual = fetch_machine_manual(machine_id)
            if manual:
                anomaly_text, emergency_text = extract_anomaly_info(manual)
                profile += f"\n📌 Manual Excerpt for Machine {machine_id}:\n--- Anomaly Detection ---\n{anomaly_text}\n--- Emergency Protocol ---\n{emergency_text}\n"
    return profile


# === Execute SQL in CrateDB ===
def execute_sql(query):
    connection = client.connect(
        f"https://{CRATEDB_HOST}:{CRATEDB_PORT}",
        username=CRATEDB_USER,
        password=CRATEDB_PASSWORD
    )
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except Exception as e:
        rows = f"SQL Error: {str(e)}"
    connection.close()
    return rows


# === Parse Date Filters ===
def parse_date_filter(question):
    question = question.lower()
    now = datetime.datetime.now(datetime.timezone.utc)

    if "last week" in question:
        start = now - datetime.timedelta(days=now.weekday() + 7)
        end = start + datetime.timedelta(days=7)
        return int(start.timestamp() * 1000), int(end.timestamp() * 1000)

    match = re.search(r"\bon (\w+ \d{1,2})\b", question)
    if match:
        date_str = match.group(1) + f" {now.year}"
        date_obj = date_parser.parse(date_str)
        start = datetime.datetime(date_obj.year, date_obj.month, date_obj.day, tzinfo=datetime.timezone.utc)
        end = start + datetime.timedelta(days=1)
        return int(start.timestamp() * 1000), int(end.timestamp() * 1000)

    match = re.search(r"between (\w+ \d{1,2}) and (\w+ \d{1,2})", question)
    if match:
        date1 = date_parser.parse(match.group(1) + f" {now.year}")
        date2 = date_parser.parse(match.group(2) + f" {now.year}")
        start = datetime.datetime(date1.year, date1.month, date1.day, tzinfo=datetime.timezone.utc)
        end = datetime.datetime(date2.year, date2.month, date2.day, tzinfo=datetime.timezone.utc) + datetime.timedelta(days=1)
        return int(start.timestamp() * 1000), int(end.timestamp() * 1000)

    return None, None


# === Remove LLM's bad date logic ===
def clean_llm_sql(sql):
    sql = re.sub(r"(AND|WHERE)\s+.*(CURRENT_DATE|INTERVAL|DATE_TRUNC|CURRENT_TIMESTAMP).*", "", sql, flags=re.IGNORECASE)
    return sql

# === Add schema in the mix ====
def inject_schema(sql, schema):
    # Replace common table names with schema-qualified ones
    tables = ["motor_readings", "machine_manuals"]
    for table in tables:
        # Use word boundaries to avoid partial replacements
        sql = re.sub(rf"\b{table}\b", f"{schema}.{table}", sql)
    return sql

# === Format timestamps in query results ===

# === Detect Manual-Related Intent ===
def detect_manual_intent(query):
    keywords = ["manual", "anomaly", "what should i do", "protocol", "emergency", "maintenance"]
    return any(keyword in query.lower() for keyword in keywords)

# === Extract Machine ID from Query ===
def extract_machine_id_from_query(query):
    match = re.search(r"machine\s*(\d+)", query.lower())
    if match:
        return int(match.group(1))
    return None

def format_timestamps(result):
    def format_value(value):
        if isinstance(value, int) and len(str(value)) >= 13:
            try:
                dt = datetime.datetime.fromtimestamp(value / 1000, tz=datetime.timezone.utc)
                return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
            except Exception:
                return value
        return value

    formatted = []
    for row in result:
        formatted.append([format_value(val) for val in row])
    return formatted


# === Chat Loop ===
def chat():
    print("Timeseries Q&A Assistant (type 'exit' to quit)\n")

    print("Example Questions:")
    print("• What is the average temperature when vibration > 1.5?")
    print("• What is the average temperature when vibration > 1.5 for motor 5?")
    print("• How many anomalies happened last week?")
    print("• What is the machine with the higest number of anomalies last week?")
    print("• What was the time of highest vibration for each machine?")
    print("• What should I do if machine 2 has an anomaly?")
    print("• What does the maintenace plan for machine 1 look like?")

    # Schema & Profile
    table_schema = fetch_table_schema("motor_readings")
    df = fetch_timeseries_data(limit=1000)
    profile_text = generate_data_profile(df)
    print(profile_text)

    # System prompt
    system_prompt = f"""
You are a data assistant for industrial motor monitoring.
You have access to this CrateDB table:

{table_schema}

Anomalies = vibration > {ANOMALY_THRESHOLD}.
Time filters like \"last week\", \"on March 28\" will be injected automatically.
Do NOT generate SQL with CURRENT_DATE, INTERVAL or DATE_TRUNC.

When the user asks:
- SQL query → write the query
- Analysis → summarize
After query execution, explain result in simple language.
"""

    conversation = [{"role": "system", "content": system_prompt}]

    # Chat loop
    while True:
        manual_context_added = False
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        
        # Check if query needs manual context
        if detect_manual_intent(user_input):
            machine_id = extract_machine_id_from_query(user_input)
            if machine_id:
                manual = fetch_machine_manual(machine_id)
                if manual:
                    anomaly_text, emergency_text = extract_anomaly_info(manual)
                    manual_context = f"\nManual Guidance for Machine {machine_id}:\n--- Anomaly Detection ---\n{anomaly_text}\n--- Emergency Protocol ---\n{emergency_text}"
                    user_input += f"\n{manual_context}"
                    manual_context_added = True

        conversation.append({"role": "user", "content": user_input})
        start_epoch, end_epoch = parse_date_filter(user_input)

        response = client_ai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        reply = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": reply})

        print(f"\n LLM Suggestion:\n{reply}")

        if "SELECT" in reply.upper():
            try:
                sql_query = reply.strip().split("```")[1].replace("sql", "").strip()
                sql_query = clean_llm_sql(sql_query)
                sql_query = inject_schema(sql_query, CRATEDB_SCHEMA)

                if start_epoch and end_epoch:
                    condition = f"timestamp >= {start_epoch} AND timestamp < {end_epoch}"
                    if "WHERE" in sql_query.upper():
                        sql_query = re.sub(r"(WHERE\s+)", f"WHERE {condition} AND ", sql_query, flags=re.IGNORECASE)
                    else:
                        sql_query += f" WHERE {condition}"

                print(f"\n Running SQL:\n{sql_query}")
                result = execute_sql(sql_query)

                if isinstance(result, list):
                    result = format_timestamps(result)
                    print(f"\n Formatted Result:\n{result}")
                else:
                    print(f"\n Query Result:\n{result}")

                # Add result to conversation
                conversation.append({"role": "user", "content": f"Query Result: {result}"})

                # Check for anomaly timestamps per machine
                if (
                    isinstance(result, list)
                    and all(isinstance(row, list) and len(row) == 2 for row in result)
                    and all(isinstance(row[0], int) and isinstance(row[1], str) for row in result)
                ):
                    print("\n📌 Summary: Most recent anomaly per machine")
                    for row in result:
                        print(f"- Machine {row[0]}: {row[1]}")

                # Check for top vibration events
                elif (
                    isinstance(result, list)
                    and len(result) > 0
                    and isinstance(result[0], list)
                    and len(result[0]) >= 3
                    and "vibration" in sql_query.lower()
                    and any(isinstance(val, float) and val > ANOMALY_THRESHOLD for row in result for val in row if isinstance(val, (float, int)))
                ):
                    print("\n📌 Summary: High vibration events")
                    for row in result[:5]:
                        try:
                            machine_id = row[0]
                            ts = row[1]
                            vib = row[2]
                            print(f"- Machine {machine_id}: {vib:.2f} at {ts}")
                        except IndexError:
                            print(f"- Result (incomplete): {row}")

                    # Show manual if applicable
                    affected_ids = list({row[0] for row in result if len(row) > 2 and isinstance(row[0], int) and row[2] > ANOMALY_THRESHOLD})
                    for machine_id in affected_ids:
                        if manual_context_added:
                            continue
                            manual = fetch_machine_manual(machine_id)
                            if manual:
                                anomaly_text, emergency_text = extract_anomaly_info(manual)
                                print(f"\n📘 Manual Guidance for Machine {machine_id}:")
                                print(f"--- Anomaly Detection ---\n{anomaly_text}\n--- Emergency Protocol ---\n{emergency_text}")
                            else:
                                print(f"\n📘 No manual guidance found for Machine {machine_id}.")

                    # 📘 Add manual advice for affected machines
                    affected_ids = list({row[0] for row in result if row[2] > ANOMALY_THRESHOLD})
                    for machine_id in affected_ids:
                        if manual_context_added:
                            continue
                            manual = fetch_machine_manual(machine_id)
                            if manual:
                                anomaly_text, emergency_text = extract_anomaly_info(manual)
                                print(f"\n📘 Manual Guidance for Machine {machine_id}:")
                                print(f"--- Anomaly Detection ---\n{anomaly_text}\n--- Emergency Protocol ---\n{emergency_text}")
                            else:
                                print(f"\n📘 No manual guidance found for Machine {machine_id}.")

                # Default to LLM explanation
                else:
                    explanation = client_ai.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=conversation
                    )
                    print(f"\n💡 Explanation:\n{explanation.choices[0].message.content}")

            except Exception as e:
                print(f"\n SQL Error: {str(e)}")

if __name__ == "__main__":
    chat()
