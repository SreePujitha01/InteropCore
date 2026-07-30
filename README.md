\# InteropCore



A healthcare interoperability data engineering project: synthetic patient data generated end-to-end through both legacy (HL7v2) and modern (FHIR) healthcare data formats, loaded into a validated, dimensionally-modeled Snowflake data warehouse, mapped to USCDI federal interoperability standards.



\## Why this project



Real hospitals and payers exchange patient data using two standards side by side: the legacy \*\*HL7v2\*\* messaging format still running inside most hospital systems, and the modern \*\*FHIR\*\* standard now required under CMS prior authorization rules and the TEFCA nationwide exchange framework. This project demonstrates working with both — not just consuming a modern API, but understanding and building the bridge between old and new.



\## Architecture

## What's in this repo



| Folder/File | Purpose |

|---|---|

| `hl7\_generator.py` | Converts Synthea's CSV patient/encounter data into valid HL7v2 ADT messages (MSH/EVN/PID/PV1 segments), with correct ADT event type and patient class mapping |

| `upload\_fhir.py` | Uploads FHIR R4 bundles to a HAPI FHIR server via REST, with dependency-aware upload ordering (hospitals/practitioners before patients) |

| `inspect\_data.py` | Utility script for exploring Synthea's raw CSV structure |

| `sql/01-06\_\*.sql` | The full Snowflake pipeline: warehouse/database setup, raw table creation, staging, data loading, data quality validation, and dimensional modeling |

| `sample\_data/` | A handful of example FHIR JSON and HL7v2 message files for reference |

| `requirements.txt` | Python dependencies |



\## Key engineering decisions and problems solved



\- \*\*HL7v2 generation from scratch\*\*: this version of Synthea has no built-in HL7v2 exporter, so `hl7\_generator.py` was written to convert patient/encounter data into properly-structured HL7v2 ADT messages, including correct mapping of encounter types (inpatient, emergency, ambulatory, etc.) to HL7v2 ADT event codes and patient class codes.

\- \*\*FHIR upload dependency ordering\*\*: Synthea's FHIR bundles reference Practitioner/Organization resources by identifier rather than embedding them, so `upload\_fhir.py` explicitly sorts uploads to load hospital and practitioner reference data before patient bundles.

\- \*\*Data quality as an explicit pipeline stage\*\*: rather than treating a successful load as proof of correctness, `05\_data\_quality\_checks.sql` runs 24 automated checks across completeness, referential integrity, validity, and uniqueness — catching real issues including duplicate loads from re-run pipeline steps, which were found and fixed during development.

\- \*\*USCDI mapping\*\*: every table in the dimensional model is explicitly mapped to its corresponding USCDI v3/v4 data class (Patient Demographics, Encounter Information, Problems, Medications, Allergies and Intolerances, Care Team Members, Facility Information), documented via Snowflake table/column comments.



\## Scope and future extensions



\- HL7v2 messages are generated and validated as a standalone artifact but not yet parsed back into the Snowflake pipeline — this is an intentional scope boundary, not an oversight.

\- A HAPI FHIR + Postgres server setup is included and was fully verified (46 patients, 2,009 conditions, 3,754 encounters, all confirmed queryable via live REST calls) but is not required to run the Snowflake side of the pipeline.



\## Tech stack



Python, Pandas, Requests, Docker, HAPI FHIR, PostgreSQL, Snowflake, SQL

