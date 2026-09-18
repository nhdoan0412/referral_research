# Interactive Outpatient Referral Research

An experimental research codebase for studying **efficient outpatient referral routing** and the tradeoffs between prediction quality, interaction cost, and latency.

The repository currently contains a classical NLP baseline, SQLite-backed experiment tracking, referral cases, prediction inspection utilities, and literature-review tooling.

## Research Direction

A referral system may need to decide which specialty or department should receive a patient case. A useful interactive system should not only predict accurately; it should also avoid asking unnecessary questions and keep inference cost and latency manageable.

This repository is structured to support experiments around:

- referral-department prediction,
- confidence-aware routing,
- interactive question collection,
- number of questions asked,
- latency,
- prompt/completion token usage, and
- comparison between simple baselines and future LLM-based approaches.

## Current Baseline

The implemented baseline uses:

```text
Initial referral note
        ↓
TF-IDF vectorization
(unigrams + bigrams)
        ↓
Logistic Regression
(class_weight="balanced")
        ↓
Predicted department + confidence
        ↓
SQLite experiment log
```

The baseline records per-case information including the predicted department, confidence, latency, correctness, and experiment setting.

## Why Start With TF-IDF + Logistic Regression?

A simple classical baseline is useful because it provides:

- a reproducible reference point,
- low inference cost,
- interpretable experimental behavior, and
- a benchmark that more complex interactive or LLM systems should outperform meaningfully.

The code also includes safeguards for very small datasets so pipeline tests are not accidentally reported as meaningful evaluation results.

## Repository Structure

| File | Purpose |
| --- | --- |
| `baseline_tfidf.py` | TF-IDF + Logistic Regression referral baseline |
| `init_db.py` | Creates the SQLite experiment schema |
| `load_cases.py` | Loads referral cases into the database |
| `check_predictions.py` | Inspects saved predictions and aggregate accuracy |
| `check_db.py` | Database inspection utility |
| `literature_review_table.py` | Generates/maintains literature-review data |
| `literature_review_table.csv` | Structured review of related work |
| `referral_cases.csv` | Development referral cases |
| `referral_research.db` | Local experiment database snapshot |

## Experiment Tracking

Predictions are persisted with fields designed for both static and interactive systems:

- `case_id`
- `model_name`
- `setting`
- `predicted_department`
- `confidence`
- `num_questions`
- `prompt_tokens`
- `completion_tokens`
- `latency_seconds`
- `is_correct`

This makes the database suitable for comparing a no-question classical baseline with later interactive approaches.

## Running the Baseline

Install the Python dependencies used by the scripts, initialize/load the experiment database, and then run:

```bash
python baseline_tfidf.py
```

Inspect saved results with:

```bash
python check_predictions.py
```

## Evaluation Notes

The baseline uses a stratified train/test split when the dataset has enough examples per class. When the dataset is too small for a meaningful split, the script explicitly warns that same-data training/testing is only being used to verify the pipeline and **must not be reported as real model accuracy**.

## Next Research Steps

- Expand the evaluation dataset with more cases per department.
- Add stronger non-LLM baselines.
- Add interactive question-selection strategies.
- Compare static versus dynamic referral settings.
- Track accuracy against number of questions and inference cost.
- Add uncertainty/calibration analysis.
- Add reproducible experiment configuration and result tables.

## Research Status

This repository is a **work in progress**. It contains baseline infrastructure and experiment scaffolding rather than a completed clinical system. It should be treated as research code, not medical advice or a production clinical decision-support tool.
