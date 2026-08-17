import sqlite3
import time
import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

DB_NAME = "referral_research.db"


def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM cases", conn)
    conn.close()
    return df


def save_predictions(result_df):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Prevent duplicate predictions each time you rerun the script
    cur.execute("""
    DELETE FROM predictions
    WHERE model_name = ? AND setting = ?
    """, ("tfidf_logistic_regression", "static_baseline"))

    for _, row in result_df.iterrows():
        cur.execute("""
        INSERT INTO predictions (
            case_id,
            model_name,
            setting,
            predicted_department,
            confidence,
            num_questions,
            prompt_tokens,
            completion_tokens,
            latency_seconds,
            is_correct
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["case_id"],
            "tfidf_logistic_regression",
            "static_baseline",
            row["predicted_department"],
            float(row["confidence"]),
            0,
            None,
            None,
            float(row["latency_seconds"]),
            int(row["is_correct"])
        ))

    conn.commit()
    conn.close()


def run_baseline():
    df = load_data()

    print("Dataset preview:")
    print(df.head())

    print("\nNumber of cases:", len(df))

    print("\nDepartment counts:")
    print(df["gold_department"].value_counts())

    if len(df) < 20:
        print("\nWARNING: You have fewer than 20 cases.")
        print("This is enough to test the code, but not enough for a meaningful ML baseline.")
        print("For real results, collect more cases per department.\n")

    X = df["initial_note"]
    y = df["gold_department"]

    n_samples = len(df)
    n_classes = y.nunique()
    min_class_count = y.value_counts().min()

    # Stratified split requires:
    # 1. At least 2 examples per class
    # 2. Test set size >= number of classes
    if min_class_count < 2:
        print("At least one department has fewer than 2 examples.")
        print("Training and testing on the same data just to test the pipeline.")
        print("Do NOT report this as real accuracy.\n")

        X_train, X_test = X, X
        y_train, y_test = y, y

    else:
        # Make sure test set has at least one sample per class
        minimum_test_size = n_classes / n_samples
        test_size = max(0.2, minimum_test_size)

        print(f"Using test_size = {test_size:.2f}")

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=42,
            stratify=y
        )

    model = make_pipeline(
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=5000
        ),
        LogisticRegression(
            max_iter=1000,
            class_weight="balanced"
        )
    )

    start_time = time.time()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    latency = time.time() - start_time

    # Get confidence from predicted probability
    probs = model.predict_proba(X_test)
    confidences = probs.max(axis=1)

    result_df = pd.DataFrame({
        "case_id": df.loc[X_test.index, "case_id"],
        "note": X_test,
        "gold_department": y_test,
        "predicted_department": preds,
        "confidence": confidences
    })

    result_df["is_correct"] = (
        result_df["gold_department"] == result_df["predicted_department"]
    ).astype(int)

    result_df["latency_seconds"] = latency / len(result_df)

    print("\nPredictions:")
    print(result_df[[
        "case_id",
        "gold_department",
        "predicted_department",
        "confidence",
        "is_correct",
        "latency_seconds"
    ]])

    print("\nAccuracy:", accuracy_score(y_test, preds))

    print("\nClassification report:")
    print(classification_report(y_test, preds, zero_division=0))

    save_predictions(result_df)

    print("\nSaved predictions to database.")


if __name__ == "__main__":
    run_baseline()