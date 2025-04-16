import os
import random
from dotenv import load_dotenv
from crate import client

# === Load environment variables ===
load_dotenv()

CRATEDB_HOST = os.getenv("CRATEDB_HOST")
CRATEDB_PORT = os.getenv("CRATEDB_PORT")
CRATEDB_USER = os.getenv("CRATEDB_USER")
CRATEDB_PASSWORD = os.getenv("CRATEDB_PASSWORD")
CRATEDB_SCHEMA = os.getenv("CRATEDB_SCHEMA")

# === Fictional Manual Generator ===
brands = ["AtlasTech", "RotoFlow", "MechAxis", "IndustraCore"]
models = ["VX100", "MX200", "TQ350", "RG450"]
year_range = list(range(2017, 2023))


def generate_manual(machine_id):
    brand = random.choice(brands)
    model = random.choice(models)
    year = random.choice(year_range)

    vib_max = round(random.uniform(1.2, 1.6), 2)
    temp_max = round(random.uniform(65, 75), 1)
    rpm_max = random.randint(1550, 1650)

    content = f"""
🛠️ Machine Manual — ID: {machine_id}

**Manufacturer:** {brand}
**Model:** {model}
**Year of Installation:** {year}

---

**Operational Limits:**
- Max Vibration: {vib_max} units
- Max Temperature: {temp_max}°C
- Max RPM: {rpm_max} rotations/min

**Anomaly Detection:**
- Vibration > {vib_max} may indicate imbalance or bearing issues
- Temperature > {temp_max} may suggest overheating
- RPM deviations > ±100 RPM require inspection

---

**Maintenance Schedule:**
- Weekly: Inspect vibration and temperature logs
- Monthly: Lubricate bearings and check alignment
- Quarterly: Full motor calibration and safety check

**Emergency Protocol:**
If vibration exceeds {vib_max + 0.2} or temperature exceeds {temp_max + 5}:
1. Immediately reduce load
2. Shut down the motor if anomaly persists for >5 mins
3. Notify operations lead and schedule maintenance

---

**Contact:**
- Support: support@{brand.lower()}.com
- Manual Version: 1.0
"""
    return content.strip()


def store_manuals_in_cratedb():
    connection = client.connect(
        f"https://{CRATEDB_HOST}:{CRATEDB_PORT}",
        username=CRATEDB_USER,
        password=CRATEDB_PASSWORD
    )
    cursor = connection.cursor()

    # Create table if not exists
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {CRATEDB_SCHEMA}.machine_manuals (
        machine_id INTEGER PRIMARY KEY,
        manual TEXT
    )
    """)

    # Get unique machine IDs from motor_readings
    cursor.execute(f"""
    SELECT DISTINCT machine_id FROM {CRATEDB_SCHEMA}.motor_readings ORDER BY machine_id
    """)
    machine_ids = [row[0] for row in cursor.fetchall()]

    print(f"🔍 Found {len(machine_ids)} unique machine IDs.")

    # Upsert manuals
    for machine_id in machine_ids:
        manual = generate_manual(machine_id)
        cursor.execute(f"""
        INSERT INTO {CRATEDB_SCHEMA}.machine_manuals (machine_id, manual)
        VALUES (?, ?)
        ON CONFLICT (machine_id) DO UPDATE SET manual = ?
        """, (machine_id, manual, manual))

    connection.close()
    print("✅ Fictional machine manuals stored (or updated) in CrateDB.")

# === Main Execution ===
if __name__ == "__main__":
    store_manuals_in_cratedb()