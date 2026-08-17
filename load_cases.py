import sqlite3
import pandas as pd

DB_NAME = "referral_research.db"
CSV_FILE = "referral_cases.csv"

required_columns = [
    "case_id",
    "initial_note",
    "gold_department",
    "gold_urgency",
    "source_dataset"
]

def load_cases():
    df = pd.read_csv(CSV_FILE)

    print("Loaded CSV:")
    print(df.head())
    print("\nColumns:", list(df.columns))

    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("""
        INSERT OR REPLACE INTO cases (
            case_id,
            initial_note,
            gold_department,
            gold_urgency,
            source_dataset
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            row["case_id"],
            row["initial_note"],
            row["gold_department"],
            row["gold_urgency"],
            row["source_dataset"]
        ))

    conn.commit()
    conn.close()

    print(f"Inserted {len(df)} cases into database.")

if __name__ == "__main__":
    load_cases()
    