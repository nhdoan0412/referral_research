import pandas as pd

papers = [
    {
        "paper_title": "Do LLMs Triage Like Clinicians? A Dynamic Study of Outpatient Referral",
        "year": "2025/2026",
        "dataset": "Outpatient referral scenarios; static and dynamic multi-turn settings",
        "task": "Predict outpatient department and ask follow-up questions under uncertainty",
        "models": "LLMs vs traditional classifiers",
        "method": "Compare static prediction with dynamic information acquisition",
        "metrics": "Referral accuracy, uncertainty reduction, question effectiveness",
        "main_results": "LLMs show more value in dynamic questioning than static prediction",
        "limitations": "Need to study question cost, stopping criteria, and uncertainty calibration",
        "relevance_to_project": "Directly related to interactive outpatient referral"
    },
    {
        "paper_title": "Evaluating Large Language Model Workflows in Clinical Decision Support for Triage and Referral and Diagnosis",
        "year": "2025",
        "dataset": "2,000 MIMIC-IV medical cases",
        "task": "Triage level, specialty referral, and diagnosis prediction",
        "models": "Claude models and RAG workflow",
        "method": "Benchmark multiple LLM workflows on clinical decision support tasks",
        "metrics": "Accuracy and clinical evaluation",
        "main_results": "RAG workflow improves some clinical decision-support performance",
        "limitations": "Mostly static workflow; not focused on minimizing follow-up questions",
        "relevance_to_project": "Useful baseline for triage/referral prediction"
    },
    {
        "paper_title": "MedTriage: A Comprehensive Benchmark for Medical Triage",
        "year": "2026",
        "dataset": "Real-world doctor-patient dialogues across multiple specialties",
        "task": "Medical specialty triage",
        "models": "Multiple LLMs / competition systems",
        "method": "Benchmark and competition-style evaluation",
        "metrics": "Specialty prediction accuracy, robustness",
        "main_results": "Shows strong variation across models and specialties",
        "limitations": "Need to verify whether interaction cost is evaluated",
        "relevance_to_project": "Potential dataset or benchmark for specialty referral"
    },
    {
        "paper_title": "Asking the Right Questions: Benchmarking LLMs in the Development of Clinical Consultation Templates",
        "year": "2025",
        "dataset": "145 expert-crafted Stanford eConsult templates",
        "task": "Generate structured consultation templates",
        "models": "o3, GPT-4o, Claude, Gemini, Llama, Kimi",
        "method": "Prompt optimization, autograding, prioritization evaluation",
        "metrics": "Comprehensiveness, conciseness, prioritization",
        "main_results": "LLMs can generate useful templates but often over-generate and poorly prioritize",
        "limitations": "Need stronger question prioritization under length constraints",
        "relevance_to_project": "Useful for designing follow-up question selection"
    },
    {
        "paper_title": "Improving Musculoskeletal Care with AI-Enhanced Triage through Data-Driven Screening of Referral Letters",
        "year": "2025",
        "dataset": "8,044 GP referral letters from 5,728 patients",
        "task": "Predict RA, osteoarthritis, fibromyalgia, chronic rheumatology follow-up",
        "models": "NLP/ML classification pipeline",
        "method": "Text preprocessing, embeddings/classification, SHAP interpretation",
        "metrics": "AUC-ROC, AUC-PRC, calibration, external validation",
        "main_results": "Referral letters contain useful signal for triage prioritization",
        "limitations": "Specialty-specific and not interactive",
        "relevance_to_project": "Useful non-LLM referral-letter baseline"
    }
]

df = pd.DataFrame(papers)
df.to_csv("literature_review_table.csv", index=False)
print(df)