
import os
import pandas as pd
from crate import client
from openai import OpenAI
from dotenv import load_dotenv
import datetime
import re
from dateutil import parser as date_parser
import streamlit as st

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

st.set_page_config(page_title="TAG Motor Chat", layout="wide")
st.title("🔧 Motor Monitoring Chatbot (TAG-Driven)")

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

# === Fetch Machine Manual ===
def fetch_machine_manual(machine_id):
    connection = client.connect(
        f"https://{CRATEDB_HOST}:{CRATEDB_PORT}",
        username=CRATEDB_USER,
        password=CRATEDB_PASSWORD
    )
    cursor = connection.cursor()
    query = f"SELECT manual FROM {CRATEDB_SCHEMA}.machine_manuals WHERE machine_id = ?"
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

# === Clean hallucinated table names & inject schema ===
def clean_and_inject_schema(sql, schema):
    # Fix hallucinated table names
    for wrong in ["machine_data", "sensor_data", "motor_data"]:
        sql = re.sub(rf"\b{wrong}\b", "motor_readings", sql, flags=re.IGNORECASE)

    # Only inject schema if not already qualified
    for table in ["motor_readings", "machine_manuals"]:
        if not re.search(rf"\b{schema}\.{table}\b", sql, flags=re.IGNORECASE):
            sql = re.sub(rf"\b{table}\b", f"{schema}.{table}", sql)
    return sql

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
        columns = [desc[0] for desc in cursor.description]
        connection.close()
        return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        connection.close()
        return f"SQL Error: {str(e)}"

# === Build system prompt with schema ===
if "conversation" not in st.session_state:
    schema = fetch_table_schema("motor_readings")
    system_prompt = f"""
You are a helpful assistant for industrial motor monitoring.
Use the following schema and guidelines to answer questions:

{schema}
- Anomalies: vibration > {ANOMALY_THRESHOLD}
- Do NOT use CURRENT_DATE, INTERVAL, DATE_TRUNC in SQL
- If the user asks about a machine's anomaly, look up its manual
- SQL queries must use schema: {CRATEDB_SCHEMA}

If a question is about next steps or safety protocols, extract relevant info from the manual.
"""
    st.session_state.conversation = [{"role": "system", "content": system_prompt}]

# === Chat UI ===

# === Layout Columns ===
col1, col2 = st.columns([3, 1])

with col2:
    st.markdown("### 💡 Example Questions")
    st.markdown("- What should I do if machine 2 has an anomaly?")
    st.markdown("- Show me the average temperature for machine 5 when vibration > 1.5")
    st.markdown("- How many anomalies happened last week?")
    st.markdown("- What does the maintenance plan for machine 1 look like?")

with col1:
    user_input = st.chat_input("Ask your question")

    if user_input:
        st.markdown("### 🧾 Your Question")
        st.info(user_input)

if user_input:
    # Inject manual context if needed
    machine_id_match = re.search(r"machine\s*(\d+)", user_input.lower())
    if machine_id_match:
        machine_id = int(machine_id_match.group(1))
        manual = fetch_machine_manual(machine_id)
        if manual:
            anomaly, emergency = extract_anomaly_info(manual)
            manual_context = f"\nManual Guidance for Machine {machine_id}:\n--- Anomaly Detection ---\n{anomaly}\n--- Emergency Protocol ---\n{emergency}"
            user_input += manual_context

    st.session_state.conversation.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        response = client_ai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.conversation
        )
        reply = response.choices[0].message.content
        st.session_state.conversation.append({"role": "assistant", "content": reply})

    st.markdown("### 🤖 LLM Suggestion")
    st.markdown(reply)

    # Try to extract and run SQL
    sql_blocks = re.findall(r"```sql(.*?)```", reply, re.DOTALL | re.IGNORECASE)
    if sql_blocks:
        raw_sql = sql_blocks[0].strip()
        raw_sql = clean_and_inject_schema(raw_sql, CRATEDB_SCHEMA)
        st.markdown("### 🧠 Cleaned SQL")
        st.code(raw_sql, language="sql")
        result = execute_sql(raw_sql)
        if isinstance(result, str):
            st.error(result)
        else:
            st.markdown("### 📊 Query Result")
            st.dataframe(result)
