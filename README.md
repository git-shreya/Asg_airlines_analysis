# ASG Airlines: Data Engineering Case Study

End-to-end pipeline for ASG Airlines' flight operations data: ingestion, cleaning, PII masking, dimensional modelling, and a Power BI dashboard on top.

## Architecture

```
Excel source -> Python ETL (notebook) -> Local MySQL Server -> Power BI Desktop
```

Python (pandas) handles ingestion, cleaning, and modelling. A local MySQL Server holds the data in two databases: `asg_airlines` for reporting, `asg_airlines_restricted` for PII, with access control enforced through MySQL users and GRANT/REVOKE. Full reasoning and the complete data model are in `docs/ASG_Airlines_Documentation.docx` (Section 2).

## Repository structure

```
/notebook/ASG_Airlines_Pipeline.ipynb   pipeline: ingestion through KPI calculation
/data/cleaned/
    fact_flights.csv
    fact_bookings.csv
    fact_payments.csv
    dim_passenger.csv
    dim_airport.csv
    secure_booking_pii.csv              restricted, PII, not for the reporting database
/scripts/
    load_to_mysql.py                    loads the cleaned CSVs into MySQL
    mysql_governance.sql                creates the restricted reporting user
/dashboard/
    ASG_Airlines_Dashboard.pbix
    screenshots/                        one image per report page
/docs/
    ASG_Airlines_Documentation.docx
    architecture_diagram.png
README.md
```

## Reproducing the pipeline

1. Place the source file `UseCase_-_Airlines.xlsx` in `/notebook/` and run `ASG_Airlines_Pipeline.ipynb` top to bottom. It writes the 6 CSVs in `/data/cleaned/`.
2. Install MySQL Community Server if not already installed.
3. Edit `ROOT_PASSWORD` in `load_to_mysql.py`, then run it. It creates `asg_airlines` and `asg_airlines_restricted` and loads all 6 tables.
4. Run `mysql_governance.sql` as root. It creates a `reporting_reader` user with SELECT on `asg_airlines` only.
5. In Power BI Desktop, connect to the MySQL database `asg_airlines` using the `reporting_reader` credentials, Import mode.

## Key decisions and assumptions

- No scheduled-time field exists in the source data, so a true delay (actual vs. scheduled) can't be computed. "Anomalies" in the dashboard refer to data-quality issues found: corrupted timestamps and reused flight identifiers.
- A `flight_id` was found reused across two genuinely different flights. Both are kept, distinguished by a surrogate key (`flight_sk`), rather than deduped away.
- Aadhaar ID and passport number are one-way hashed or kept in the restricted database only; email, phone, and date of birth are masked or bucketed in the reporting layer.

Full rationale, the complete data quality table, and the data model are in `docs/ASG_Airlines_Documentation.docx`.

## Business KPIs

- Average flight duration (overall, by airline, by route)
- Route-wise traffic
- Distribution of flights by airline
- Anomalies (corrupted timestamps, reused flight IDs, ambiguous booking references)
- Revenue by airline and route
- Booking status funnel
- Payment method mix
- Passenger age-band distribution
