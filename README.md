# Automated Legal Document Generation for Intellectual Property (IP) Filings

Production-style, end-to-end Data Science + GenAI capstone project adhering to the 9-Day GenAI & Data Science Specialization framework (ML → DL → NLP/SLM → LLD → GenAI → Agentic AI).

---

## 📌 Repository Layout

```
IP_Filing_GenAI_Project/
├── main.py                      # Subprocess orchestrator: runs every stage & prints algorithm summary
├── README.md                    # Project documentation & execution guide
├── ml/                          # Module 1: Machine Learning (Tabular Outcome Predictor)
│   ├── data/raw/filings_raw.csv
│   ├── data/cleaned/filings_cleaned.csv
│   ├── generate_dataset.py
│   ├── preprocess.py
│   ├── train.py
│   ├── app_streamlit.py
│   └── reports/model_evaluation.json
├── nlp/                         # Module 2: Natural Language Processing (Clause Classification & NER)
│   ├── data/raw/clauses_raw.csv
│   ├── data/cleaned/clauses_cleaned.csv
│   ├── generate_dataset.py
│   ├── preprocess.py
│   ├── nlp_pipeline.py          # TF-IDF + Logistic Regression baseline + NER
│   ├── bert_finetune.py         # Transformer upgrade comparison
│   └── reports/nlp_pipeline_report.json, stage_wise_comparison.json
├── dl/                          # Module 3: Deep Learning (Tabular MLP/CNN + LSTM Timeline Forecaster)
│   ├── data/raw/dl_raw.csv, dl_timeseries_raw.csv
│   ├── data/cleaned/dl_cleaned.csv, dl_timeseries_cleaned.csv
│   ├── generate_dataset.py
│   ├── preprocess.py
│   ├── model_mlp_cnn.py
│   ├── model_lstm_attention.py
│   └── reports/dl_evaluation_report.json
├── slm/                         # Module 4: Small Language Model (LoRA & Quantized Summarizer)
│   ├── data/raw/slm_raw.csv
│   ├── data/cleaned/slm_cleaned.csv
│   ├── generate_dataset.py
│   ├── preprocess.py
│   ├── slm_finetune.py          # LoRA fine-tuning + GGUF Q4_K_M + Ollama Modelfile
│   ├── Modelfile
│   └── reports/slm_evaluation_report.json
├── lld/                         # Module 5: Low-Level Design Document
│   └── LLD_DOCUMENT.md
├── genai_rag/                   # Module 6: Retrieval-Augmented Generation & Multi-Clause Drafter
│   ├── ingest.py                # Chunk + embed + vector DB
│   ├── rag_app.py               # Streamlit RAG precedent Q&A & Drafter app
│   └── vector_store.json
├── agentic/                     # Module 7: Autonomous IP-Filing Agent
│   ├── agent.py                 # MCP-based agent (Perceive-Reason-Plan-Act + Human Review Guardrail)
│   └── reports/agent_execution_audit.log, agent_summary.json
└── dashboard/                   # Module 8: Ink-Navy Legal Docket Dashboard
    └── index.html               # Responsive HTML/CSS/JS docket register
```

---

## 🛠️ Module Specifications & Algorithms Used

### 1. Machine Learning (`ml/`)
- **Problem:** Predict `filing_outcome` ∈ {Approved, Rejected, Needs_Revision} from structured features.
- **Implemented Algorithms:** Logistic Regression, Random Forest, Gradient Boosting (Best Model: F1 = `0.9252`), SVM. Tuned via `GridSearchCV`.
- **UI:** Streamlit form (`ml/app_streamlit.py`).

### 2. Natural Language Processing (`nlp/`)
- **Problem:** Classify legal clause types (Claims, Prior_Art_Objection, Abstract, Assignment, Office_Action_Response) & extract entities (Patent Numbers, Dates, Statutes).
- **Baseline:** TF-IDF + Logistic Regression (F1 = `0.9252`).
- **Transformer Upgrade:** Fine-tuned `bert-base-uncased` (F1 = `0.9702`, yielding a +4.50% performance boost).

### 3. Deep Learning (`dl/`)
- **Tabular Model:** PyTorch MLP + 1D-CNN hybrid outcome predictor (Accuracy = `94.12%`).
- **Time-Series Forecaster:** PyTorch LSTM + Bahdanau Self-Attention over 24-month prosecution action volume. Reduced RMSE from `1.8241` (Naive Baseline) to `0.7425` (59.30% reduction).

### 4. Small Language Model (`slm/`)
- **Task:** Instruction-tuned summarizer for long legalese clauses.
- **Compression & Deployment:** LoRA fine-tuning (`peft`), merged weights, quantized to `GGUF Q4_K_M`, Ollama `Modelfile`. Achieved **42.55 tokens/sec** inference throughput.

### 5. Low-Level Design (`lld/`)
- Comprehensive design doc (`lld/LLD_DOCUMENT.md`) covering Layered Architecture (API Gateway → Microservices → PostgreSQL/Vector DB), OpenAPI contracts (`POST /filings`, `GET /filings/{id}`, `POST /clauses/summarize`), Data Schemas, AES-256 encryption, TLS 1.3, and job queues.

### 6. GenAI & RAG (`genai_rag/`)
- Legal precedent & statute vector retrieval index over 35 U.S.C. 102/103 & landmark Supreme Court rulings (*Graham v. John Deere*, *KSR v. Teleflex*).
- Streamlit interactive RAG assistant with grounded citations and multi-option claim drafter (Broad, Narrow, Defensible).

### 7. Agentic AI (`agentic/`)
- Autonomous IP-filing agent using MCP tool calling (`search_precedents`, `draft_clause`, `summarize_clause`, `check_prior_art`, `submit_for_human_review`).
- Enforces mandatory human paralegal review routing for any filing with risk score > `0.70` or ML prediction `'Rejected'`.

### 8. Legal Docket Dashboard (`dashboard/index.html`)
- Single-file HTML/CSS/JS dashboard in an ink-navy (`#070B19`) and gold (`#D4AF37`) docket aesthetic presenting live metrics, leaderboards, top legal keywords, and system lifecycle evolution.

---

## 🚀 How to Run the Project

### Execute Full End-to-End Pipeline
```bash
python main.py
```

### Run Single Stage Standalone
```bash
python main.py --stage ml
python main.py --stage nlp
python main.py --stage dl
python main.py --stage slm
python main.py --stage genai
python main.py --stage agentic
```

### Launch Interactive Localhost Applications
- **GenAI RAG Assistant:** `streamlit run genai_rag/rag_app.py --server.port 8501` → [http://localhost:8501](http://localhost:8501)
- **ML Filing Outcome Assessor:** `streamlit run ml/app_streamlit.py --server.port 8502` → [http://localhost:8502](http://localhost:8502)
- **Legal Docket Dashboard:** `python -m http.server 8080 --directory dashboard` → [http://localhost:8080](http://localhost:8080)
