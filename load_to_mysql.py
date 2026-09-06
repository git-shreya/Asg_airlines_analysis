"""
Loads the cleaned CSVs into a local MySQL server.

Prereqs:
  - MySQL Community Server installed and running
  - pip install pymysql sqlalchemy cryptography

Two separate databases are used, not just tables, so access control is a
real GRANT/REVOKE boundary:
  - asg_airlines             -> reporting layer (what Power BI connects to)
  - asg_airlines_restricted  -> secure_booking_pii only

Run mysql_governance.sql (as root) after this script.
"""
import pymysql  # noqa: F401
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from pathlib import Path
import pandas as pd

ROOT_USER = "root"
ROOT_PASSWORD = ""  # fill in your MySQL root password
HOST = "localhost"

DATA_DIR = Path(__file__).resolve().parent  # put all 6 CSVs next to this file

def make_engine(database=None):
    url = URL.create("mysql+pymysql", username=ROOT_USER, password=ROOT_PASSWORD,
                      host=HOST, database=database)
    return create_engine(url)

engine_admin = make_engine()
with engine_admin.begin() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS asg_airlines"))
    conn.execute(text("CREATE DATABASE IF NOT EXISTS asg_airlines_restricted"))

engine_reporting = make_engine("asg_airlines")
engine_restricted = make_engine("asg_airlines_restricted")

tables = {
    "fact_flights": "fact_flights.csv",
    "fact_bookings": "fact_bookings.csv",
    "fact_payments": "fact_payments.csv",
    "dim_passenger": "dim_passenger.csv",
    "dim_airport": "dim_airport.csv",
}

for table, csv in tables.items():
    df = pd.read_csv(DATA_DIR / csv)
    df.to_sql(table, engine_reporting, if_exists="replace", index=False)
    print(f"loaded asg_airlines.{table}: {len(df)} rows")

secure_df = pd.read_csv(DATA_DIR / "secure_booking_pii.csv")
secure_df.to_sql("secure_booking_pii", engine_restricted, if_exists="replace", index=False)
print(f"loaded asg_airlines_restricted.secure_booking_pii: {len(secure_df)} rows")
