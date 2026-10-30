import os
import csv
import random
import math

def generate_raw_dl_dataset(tabular_output: str, timeseries_output: str, num_samples: int = 1500, seed: int = 42):
    """Generates synthetic tabular and 24-month time-series datasets for Deep Learning using standard library."""
    random.seed(seed)
    filing_types = ['Patent', 'Trademark', 'Design', 'Copyright', 'PATENT', '']

    headers_tab = [
        'filing_id', 'filing_type', 'word_count', 'claims_count',
        'prior_art_similarity', 'examiner_workload', 'attorney_assistance',
        'fees_paid', 'filing_outcome'
    ]

    headers_ts = ['filing_id'] + [f'month_{m}' for m in range(1, 25)]

    rows_tab = []
    rows_ts = []

    for i in range(num_samples):
        f_id = f"DL-2026-{30000 + i}"
        f_type = random.choice(filing_types)

        w_cnt = int(random.gauss(4800, 1200))
        c_cnt = max(1, int(random.expovariate(1.0/18.0)))
        p_art = round(random.betavariate(2, 4), 4)
        ex_wrk = random.randint(10, 60)
        att = random.choice(['Yes', 'NO', ' yes ', 'No', ''])
        fee = round(random.uniform(600, 4800), 2)

        has_att = str(att).strip().lower() in ['yes', 'y']
        score = (
            (1.2 if has_att else -0.4) +
            (1.8 if p_art < 0.3 else -1.2) +
            (-0.015 * ex_wrk) +
            random.gauss(0, 1.0)
        )
        outcome = 'Approved' if score > 1.0 else ('Rejected' if score < -0.7 else 'Needs_Revision')

        w_val = str(w_cnt) if random.random() >= 0.04 else ""
        fee_val = str(fee) if random.random() >= 0.02 else "-500.0"

        rows_tab.append([f_id, f_type, w_val, c_cnt, p_art, ex_wrk, att, fee_val, outcome])

        # 24-Month Time-Series Sequence
        ts_seq = [f_id]
        for m in range(1, 25):
            val = max(0, int(random.poissonvariate(3.0) + (m * 0.1) + random.gauss(0, 0.5))) if hasattr(random, 'poissonvariate') else max(0, int(3 + (m * 0.1) + random.gauss(0, 1.0)))
            ts_seq.append(str(val))
        rows_ts.append(ts_seq)

    os.makedirs(os.path.dirname(tabular_output), exist_ok=True)
    os.makedirs(os.path.dirname(timeseries_output), exist_ok=True)

    with open(tabular_output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers_tab)
        writer.writerows(rows_tab)

    with open(timeseries_output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers_ts)
        writer.writerows(rows_ts)

    print(f"[DL Dataset Generator] Tabular dataset: {tabular_output} ({len(rows_tab)} rows)")
    print(f"[DL Dataset Generator] Time-series dataset: {timeseries_output} ({len(rows_ts)} rows)")

if __name__ == "__main__":
    generate_raw_dl_dataset(
        "C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/dl/data/raw/dl_raw.csv",
        "C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/dl/data/raw/dl_timeseries_raw.csv"
    )
