import sqlite3
import pandas as pd

DB_NAME = "referral_research.db"

conn = sqlite3.connect(DB_NAME)

df = pd.read_sql_query("SELECT * FROM cases", conn)

print(df)
print("\nNumber of cases:", len(df))
print("\nDepartments:")
print(df["gold_department"].value_counts())

conn.close()