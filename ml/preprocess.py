import os
import csv
import statistics

def clean_ml_dataset(raw_path: str, clean_path: str):
    """
    Cleans raw IP filing dataset using Python standard library.
    
    Cleaning Steps:
    1. Deduplication: Removes duplicate rows.
    2. Whitespace & Casing Normalization.
    3. Outlier Handling: Removes negative fees and extreme word counts (> 50000).
    4. Imputation: Fills missing numerical features with column median.
    """
    print(f"[ML Preprocess] Loading raw dataset from: {raw_path}")
    with open(raw_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)

    initial_len = len(rows)

    # 1. Deduplication
    unique_rows = []
    seen = set()
    for row in rows:
        row_tuple = tuple(row)
        if row_tuple not in seen:
            seen.add(row_tuple)
            unique_rows.append(row)

    dedup_len = len(unique_rows)
    print(f"  -> Step 1: Removed {initial_len - dedup_len} duplicate rows.")

    # Parse and clean values
    parsed = []
    word_counts, claims_counts, prior_arts, workloads, fees_list = [], [], [], [], []

    for row in unique_rows:
        f_id, f_type, w_cnt, c_cnt, p_art, ex_wrk, att, fee, outcome = row

        # Clean strings
        f_type = f_type.strip().title()
        if f_type not in ['Patent', 'Trademark', 'Design', 'Copyright']:
            f_type = 'Patent'

        att = att.strip().title()
        att = 'Yes' if att in ['Yes', 'Y'] else 'No'

        # Clean numbers
        w_val = float(w_cnt) if w_cnt != "" else None
        if w_val is not None and (w_val < 0 or w_val > 50000):
            w_val = None
        if w_val is not None:
            word_counts.append(w_val)

        c_val = int(c_cnt) if c_cnt != "" else 15
        claims_counts.append(c_val)

        p_val = float(p_art) if p_art != "" else None
        if p_val is not None and 0.0 <= p_val <= 1.0:
            prior_arts.append(p_val)
        else:
            p_val = None

        ex_val = int(ex_wrk) if ex_wrk != "" else 25
        workloads.append(ex_val)

        fee_val = float(fee) if fee != "" else None
        if fee_val is not None and fee_val < 0:
            fee_val = None
        if fee_val is not None:
            fees_list.append(fee_val)

        parsed.append({
            'filing_id': f_id,
            'filing_type': f_type,
            'word_count': w_val,
            'claims_count': c_val,
            'prior_art_similarity': p_val,
            'examiner_workload': ex_val,
            'attorney_assistance': att,
            'fees_paid': fee_val,
            'filing_outcome': outcome
        })

    # Compute Medians for Imputation
    med_word = statistics.median(word_counts) if word_counts else 4500.0
    med_part = statistics.median(prior_arts) if prior_arts else 0.25
    med_fee = statistics.median(fees_list) if fees_list else 2000.0

    cleaned_rows = []
    for item in parsed:
        w_final = item['word_count'] if item['word_count'] is not None else med_word
        p_final = item['prior_art_similarity'] if item['prior_art_similarity'] is not None else med_part
        f_final = item['fees_paid'] if item['fees_paid'] is not None else med_fee

        cleaned_rows.append([
            item['filing_id'], item['filing_type'], str(round(w_final, 1)),
            str(item['claims_count']), str(round(p_final, 4)),
            str(item['examiner_workload']), item['attorney_assistance'],
            str(round(f_final, 2)), item['filing_outcome']
        ])

    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    with open(clean_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(cleaned_rows)

    print(f"[ML Preprocess] Cleaned dataset saved to: {clean_path} ({len(cleaned_rows)} rows)")
    return cleaned_rows

if __name__ == "__main__":
    clean_ml_dataset(
        "C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/ml/data/raw/filings_raw.csv",
        "C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/ml/data/cleaned/filings_cleaned.csv"
    )
