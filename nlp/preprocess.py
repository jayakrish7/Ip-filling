import os
import csv
import re

def clean_nlp_dataset(raw_path: str, clean_path: str):
    """Cleans raw legal clauses dataset using standard library."""
    print(f"[NLP Preprocess] Loading raw dataset from: {raw_path}")
    with open(raw_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)

    initial_len = len(rows)

    seen_texts = set()
    cleaned_rows = []

    label_map = {
        'claims': 'Claims', 'Claims': 'Claims',
        'prior_art_objection': 'Prior_Art_Objection', 'Prior_Art_Objection': 'Prior_Art_Objection',
        'abstract': 'Abstract', 'Abstract': 'Abstract',
        'assignment': 'Assignment', 'Assignment': 'Assignment',
        'office_action_response': 'Office_Action_Response', 'Office_Action_Response': 'Office_Action_Response'
    }

    for row in rows:
        c_id, c_type, text, pat_num, f_date, org = row

        text_norm = re.sub(r'\s+', ' ', text.strip())
        if len(text_norm) <= 10 or text_norm in seen_texts:
            continue
        seen_texts.add(text_norm)

        c_type_norm = label_map.get(c_type.strip(), 'Claims')
        pat_num_norm = pat_num.strip() if pat_num.strip() else 'N/A'
        f_date_norm = f_date.strip() if f_date.strip() else 'Unknown'
        org_norm = org.strip() if org.strip() else 'Unassigned'

        cleaned_rows.append([c_id, c_type_norm, text_norm, pat_num_norm, f_date_norm, org_norm])

    print(f"  -> Step 1: Removed {initial_len - len(cleaned_rows)} duplicate/short text rows.")

    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    with open(clean_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(cleaned_rows)

    print(f"[NLP Preprocess] Cleaned dataset saved to: {clean_path} ({len(cleaned_rows)} rows)")
    return cleaned_rows

if __name__ == "__main__":
    clean_nlp_dataset(
        "C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/nlp/data/raw/clauses_raw.csv",
        "C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/nlp/data/cleaned/clauses_cleaned.csv"
    )
