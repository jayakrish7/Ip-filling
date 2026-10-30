import os
import sys
import argparse
import subprocess

# Ensure UTF-8 output encoding on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ALGORITHMS_SUMMARY = """
===================================================================================
AUTOMATED LEGAL DOCUMENT GENERATION FOR IP FILINGS
===================================================================================
ALGORITHMS USED PER MODULE:
-----------------------------------------------------------------------------------
1. ML (Machine Learning):
   - Logistic Regression (interpretable linear baseline)
   - Random Forest (bagging ensemble)
   - Gradient Boosting (boosting ensemble)
   - SVM (Support Vector Machine with RBF/linear kernels)
   - Hyperparameter Tuning: GridSearchCV

2. NLP (Natural Language Processing):
   - Baseline: TF-IDF Vectorizer + Logistic Regression (CPU, scikit-learn)
   - Entity Extractor: Heuristic/Regex Parser (Patent Numbers, Dates, Statutes)
   - Upgrade: Fine-tuned BERT (bert-base-uncased) / Transformer Architecture

3. DL (Deep Learning):
   - Tabular Outcome Predictor: PyTorch MLP + 1D-CNN Hybrid Architecture
   - Prosecution Timeline Forecaster: PyTorch LSTM + Bahdanau Self-Attention
   - Baseline Evaluator: Naive Last-Step Persistence

4. SLM (Small Language Model):
   - Instruction Tuning: LoRA (Low-Rank Adaptation with PEFT)
   - Model Compression: GGUF Q4_K_M 4-bit Quantization
   - Deployment Engine: Ollama Modelfile Local Runtime

5. LLD (Low-Level Design):
   - Architectural Blueprint: API Gateway -> Microservices -> PostgreSQL + Vector DB
   - REST API Specifications: OpenAPI 3.0 Contract for Filings, Generation & SLM
   - Security & Scalability: AES-256 Encryption at Rest, Async Job Queues

6. GenAI & RAG:
   - Chunking & Vector Search: TF-IDF / Cosine Similarity Vector Index
   - Grounded Q&A: Precedent & Statute Citation Engine
   - Clause Drafter: Multi-Option Wording Engine (Broad / Narrow / Defensible)

7. Agentic AI:
   - Autonomous Architecture: Perceive -> Reason -> Plan -> Act Execution Loop
   - Tool Integration: MCP Tool Registry (search_precedents, check_prior_art, etc.)
   - Safety Guardrails: Mandatory Risk Threshold Routing to Human Attorney Queue
===================================================================================
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STAGES = {
    "ml": [
        os.path.join(BASE_DIR, "ml", "generate_dataset.py"),
        os.path.join(BASE_DIR, "ml", "preprocess.py"),
        os.path.join(BASE_DIR, "ml", "train.py")
    ],
    "nlp": [
        os.path.join(BASE_DIR, "nlp", "generate_dataset.py"),
        os.path.join(BASE_DIR, "nlp", "preprocess.py"),
        os.path.join(BASE_DIR, "nlp", "nlp_pipeline.py"),
        os.path.join(BASE_DIR, "nlp", "bert_finetune.py")
    ],
    "dl": [
        os.path.join(BASE_DIR, "dl", "generate_dataset.py"),
        os.path.join(BASE_DIR, "dl", "preprocess.py"),
        os.path.join(BASE_DIR, "dl", "model_mlp_cnn.py"),
        os.path.join(BASE_DIR, "dl", "model_lstm_attention.py")
    ],
    "slm": [
        os.path.join(BASE_DIR, "slm", "generate_dataset.py"),
        os.path.join(BASE_DIR, "slm", "preprocess.py"),
        os.path.join(BASE_DIR, "slm", "slm_finetune.py")
    ],
    "genai": [
        os.path.join(BASE_DIR, "genai_rag", "ingest.py")
    ],
    "agentic": [
        os.path.join(BASE_DIR, "agentic", "agent.py")
    ]
}

def run_script(script_path: str):
    """Executes a single python script in a subprocess with error capturing."""
    rel_path = os.path.relpath(script_path, BASE_DIR)
    print(f"\n[RUNNING] {rel_path}")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        result = subprocess.run([sys.executable, script_path], check=True, text=True, capture_output=True, env=env)
        print(result.stdout)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error running {rel_path}:")
        print(e.stderr)
        return False, e.stderr

def run_stage(stage_name: str):
    """Runs all scripts in a specified module stage."""
    print(f"\n=======================================================")
    print(f" EXECUTING STAGE: [{stage_name.upper()}]")
    print(f"=======================================================")
    
    scripts = STAGES.get(stage_name.lower())
    if not scripts:
        print(f"Unknown stage: '{stage_name}'. Available: {list(STAGES.keys())}")
        return False

    success = True
    for script in scripts:
        ok, _ = run_script(script)
        if not ok:
            print(f"[WARNING] Stage [{stage_name}] encountered a non-fatal script issue.")
            success = False

    if success:
        print(f"[SUCCESS] Stage [{stage_name.upper()}] completed successfully.")
    else:
        print(f"[WARNING] Stage [{stage_name.upper()}] completed with warnings.")
    return success

def main():
    parser = argparse.ArgumentParser(description="Orchestrator for IP Legal Filing GenAI Project")
    parser.add_argument("--stage", type=str, help="Run specific stage: ml, nlp, dl, slm, genai, agentic")
    args = parser.parse_args()

    print(ALGORITHMS_SUMMARY)

    if args.stage:
        run_stage(args.stage)
    else:
        print("\nExecuting Full End-to-End Project Pipeline...")
        for stage_name in STAGES.keys():
            run_stage(stage_name)
        print("\nFull Pipeline Execution Finished!")

if __name__ == "__main__":
    main()
