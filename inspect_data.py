import pandas as pd

# Load the two core tables we need
patients = pd.read_csv("data/patients.csv")
encounters = pd.read_csv("data/encounters.csv")

print("=== PATIENTS ===")
print(patients.columns.tolist())
print(patients.head(3))

print("\n=== ENCOUNTERS ===")
print(encounters.columns.tolist())
print(encounters.head(3))

print("\n=== ENCOUNTER CLASSES ===")
print(encounters['ENCOUNTERCLASS'].value_counts())