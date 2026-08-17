import sqlite3
import pandas as pd

DB_NAME = "referral_research.db"

conn = sqlite3.connect(DB_NAME)

df = pd.read_sql_query("""
SELECT 
    p.id,
    p.case_id,
    c.initial_note,
    c.gold_department,
    p.predicted_department,
    p.model_name,
    p.setting,
    p.confidence,
    p.latency_seconds,
    p.is_correct
FROM predictions p
JOIN cases c ON p.case_id = c.case_id
ORDER BY p.id ASC
""", conn)

print(df)
print("\nNumber of saved predictions:", len(df))

if len(df) > 0:
    print("\nAccuracy from database:", df["is_correct"].mean())

conn.close()