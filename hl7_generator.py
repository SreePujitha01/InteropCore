import pandas as pd
from datetime import datetime

def format_hl7_datetime(iso_string):
    """Convert Synthea's ISO datetime (2011-02-11T14:03:25Z) to HL7v2 format (20110211140325)"""
    if pd.isna(iso_string):
        return ""
    dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
    return dt.strftime("%Y%m%d%H%M%S")

def format_hl7_date(iso_date):
    """Convert Synthea's date (2005-02-25) to HL7v2 format (20050225)"""
    if pd.isna(iso_date):
        return ""
    dt = datetime.fromisoformat(iso_date)
    return dt.strftime("%Y%m%d")

def get_event_type(encounter_class):
    """Map Synthea's encounter class to an HL7v2 ADT event type"""
    if encounter_class in ("inpatient", "snf"):
        return "A01"  # Admit
    else:
        return "A04"  # Register


def get_patient_class(encounter_class):
    """
Map Synthea's encounter class to a valid HL7v2 PV1-2 Patient Class code
"""
    mapping = {
        "inpatient": "I",
        "snf": "I",
        "emergency": "E",
        "ambulatory": "O",
        "outpatient": "O",
        "wellness": "O",
        "urgentcare": "O",
        "home": "O",
    }
    return mapping.get(encounter_class, "O")

def build_adt_message(row, message_id):
    event_type = get_event_type(row["ENCOUNTERCLASS"])
    event_datetime = format_hl7_datetime(row["START"])
    birthdate = format_hl7_date(row["BIRTHDATE"])
    zip_code = "" if pd.isna(row["ZIP"]) or row["ZIP"] == 0 else str(int(row["ZIP"]))

    msh = f"MSH|^~\\&|InteropCore|Hospital|EHR|Hospital|{event_datetime}||ADT^{event_type}|{message_id}|P|2.5"
    evn = f"EVN|{event_type}|{event_datetime}"
    pid = f"PID|1||{row['Id_patient']}||{row['LAST']}^{row['FIRST']}^{row['MIDDLE']}||{birthdate}|{row['GENDER']}|||{row['ADDRESS']}^^{row['CITY']}^{row['STATE']}^{zip_code}"
    pv1 = f"PV1|1|{get_patient_class(row['ENCOUNTERCLASS'])}|^^^{row['ORGANIZATION']}||||||||||||||||{row['Id_encounter']}"

    return "\n".join([msh, evn, pid, pv1])

import os

# --- Generate messages for all encounters ---
patients = pd.read_csv("data/patients.csv")
encounters = pd.read_csv("data/encounters.csv")
merged = encounters.merge(patients, left_on="PATIENT", right_on="Id", suffixes=("_encounter", "_patient"))

output_dir = "data/hl7"
os.makedirs(output_dir, exist_ok=True)

for i, row in merged.iterrows():
    message_id = f"MSG{i:05d}"
    message = build_adt_message(row, message_id)
    filepath = os.path.join(output_dir, f"{message_id}.hl7")
    with open(filepath, "w") as f:
        f.write(message)

print(f"Generated {len(merged)} HL7v2 messages in {output_dir}/")
