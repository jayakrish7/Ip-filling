import os
import csv
import random
import math

def generate_raw_ml_dataset(output_path: str, num_samples: int = 1500, seed: int = 42):
    """
    Generates synthetic raw dataset for IP filing outcome prediction using standard library.
    Introduces realistic messiness:
    - Missing values (nulls)
    - Inconsistent casing and whitespace
    - Duplicate rows
    - Outliers (negative fees, extreme word counts)
    """
    random.seed(seed)

    filing_types = ['Patent', 'Trademark', 'Design', 'Copyright', 'PATENT', ' trademark ', 'design', '']
    attorney_choices = ['Yes', 'NO', ' yes ', 'No', 'YES', '', 'n/a']

    headers = [
        'filing_id', 'filing_type', 'word_count', 'claims_count',
        'prior_art_similarity', 'examiner_workload', 'attorney_assistance',
        'fees_paid', 'filing_outcome'
    ]

    rows = []
    for i in range(num_samples):
        f_id = f"IP-2026-{10000 + i}"
        f_type = random.choice(filing_types)
        
        # Gaussian approx using Box-Muller
        u1, u2 = random.random(), random.random()
        z = math.sqrt(-2.0 * math.log(max(u1, 1e-9))) * math.cos(2.0 * math.pi * u2)
        word_count = int(4500 + z * 1500)
        
        claims_count = max(1, int(random.expovariate(1.0/15.0)))
        prior_art_sim = round(random.betavariate(2, 5), 4)
        examiner_workload = random.randint(5, 50)
        attorney = random.choice(attorney_choices)
        fees = round(random.uniform(500, 5000), 2)

        # Underlying outcome logic
        attorney_clean = str(attorney).strip().lower()
        has_attorney = attorney_clean in ['yes', 'y']
        
        score = (
            (1.5 if has_attorney else -0.5) +
            (2.0 if prior_art_sim < 0.35 else -1.5) +
            (1.0 if claims_count <= 25 else -0.5) +
            (-0.02 * examiner_workload) +
            random.gauss(0, 1.0)
        )

        if score > 1.2:
            outcome = 'Approved'
        elif score < -0.8:
            outcome = 'Rejected'
        else:
            outcome = 'Needs_Revision'

        # Inject Messiness
        w_val = str(word_count) if random.random() >= 0.05 else ""
        p_val = str(prior_art_sim) if random.random() >= 0.05 else ""
        f_val = str(fees) if random.random() >= 0.04 else ""

        # Outliers
        if random.random() < 0.02 and w_val != "":
            w_val = "999999"
        if random.random() < 0.01 and f_val != "":
            f_val = "-1200.0"

        rows.append([
            f_id, f_type, w_val, claims_count, p_val,
            examiner_workload, attorney, f_val, outcome
        ])

    # Inject duplicates
    dupe_count = int(num_samples * 0.03)
    dupes = random.choices(rows, k=dupe_count)
    rows.extend(dupes)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"[ML Dataset Generator] Created raw dataset with {len(rows)} rows at: {output_path}")

if __name__ == "__main__":
    generate_raw_ml_dataset("C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/ml/data/raw/filings_raw.csv")
