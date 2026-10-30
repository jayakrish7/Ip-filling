import os
import csv

def clean_slm_dataset(raw_path: str, clean_path: str):
    """Cleans instruction dataset using standard library."""
    print(f"[SLM Preprocess] Cleaning raw dataset from: {raw_path}")
    with open(raw_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)

    seen = set()
    cleaned_rows = []

    for r in rows:
        inst_id, prompt, summary, domain = r
        if prompt not in seen:
            seen.add(prompt)
            dom_c = domain.strip() if domain.strip() else 'General_IP'
            cleaned_rows.append([inst_id, prompt.strip(), summary.strip(), dom_c])

    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    with open(clean_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(cleaned_rows)

    print(f"[SLM Preprocess] Cleaned dataset saved to: {clean_path} ({len(cleaned_rows)} rows)")
    return cleaned_rows

if __name__ == "__main__":
    clean_slm_dataset(
        "C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/slm/data/raw/slm_raw.csv",
        "C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/slm/data/cleaned/slm_cleaned.csv"
    )
