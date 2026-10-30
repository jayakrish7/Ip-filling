import os
import csv
import random

def generate_raw_slm_dataset(output_path: str, num_samples: int = 800, seed: int = 42):
    """Generates synthetic instruction-tuning dataset for SLM legal summarizer using standard library."""
    random.seed(seed)
    pairs = [
        (
            "The Patentee hereby grants to Licensee a non-exclusive, worldwide, royalty-bearing, non-transferable license...",
            "Licensee gets a non-transferable worldwide right to make and sell products under the patent, but cannot sublicense."
        ),
        (
            "Under 35 U.S.C. 103, claims 1-10 are rejected as obvious over US10984123B2 in view of Smith et al...",
            "Claims 1-10 are rejected as obvious because combining two cited prior art references would be obvious to a skilled engineer."
        ),
        (
            "Assignor hereby conveys, assigns, and transfers all right, title, and interest in US Patent Application 17/999,888.",
            "Assignor transfers 100% ownership of US Patent Application 17/999,888."
        )
    ]

    headers = ["instruction_id", "long_legal_clause", "plain_english_summary", "clause_domain"]
    rows = []

    for i in range(num_samples):
        long_txt, summary = random.choice(pairs)
        prompt = f"Summarize the following legal clause into plain English:\n{long_txt}"
        c_domain = random.choice(["Licensing", "Prosecution", "Assignment", "Litigation", ""])
        rows.append([f"SLM-INST-{40000 + i}", prompt, summary, c_domain])

    dupe_count = int(num_samples * 0.03)
    rows.extend(random.choices(rows, k=dupe_count))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"[SLM Dataset Generator] Created instruction raw dataset with {len(rows)} rows at: {output_path}")

if __name__ == "__main__":
    generate_raw_slm_dataset("C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/slm/data/raw/slm_raw.csv")
