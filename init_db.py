import sqlite3

DB_NAME = "referral_research.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cases (
        case_id TEXT PRIMARY KEY,
        initial_note TEXT NOT NULL,
        gold_department TEXT NOT NULL,
        gold_urgency TEXT,
        source_dataset TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT NOT NULL,
        model_name TEXT NOT NULL,
        setting TEXT,
        predicted_department TEXT,
        confidence REAL,
        num_questions INTEGER DEFAULT 0,
        prompt_tokens INTEGER,
        completion_tokens INTEGER,
        latency_seconds REAL,
        is_correct INTEGER,
        FOREIGN KEY(case_id) REFERENCES cases(case_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS interaction_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id TEXT NOT NULL,
        model_name TEXT,
        turn_number INTEGER,
        question_asked TEXT,
        patient_answer TEXT,
        model_uncertainty REAL,
        current_prediction TEXT,
        FOREIGN KEY(case_id) REFERENCES cases(case_id)
    )
    """)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()