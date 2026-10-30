import os
import csv
import statistics

def clean_dl_datasets(raw_tab_path: str, raw_ts_path: str, clean_tab_path: str, clean_ts_path: str):
    """Cleans DL tabular and time-series datasets using standard library."""
    print(f"[DL Preprocess] Cleaning raw datasets...")

    # Clean Tabular
    with open(raw_tab_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers_tab = next(reader)
        rows_tab = list(reader)

    seen_tab = set()
    cleaned_tab = []
    for r in rows_tab:
        if r[0] not in seen_tab:
            seen_tab.add(r[0])
            f_id, f_type, w, c, p, ex, att, fee, out = r
            f_type_c = f_type.strip().title() if f_type.strip() else 'Patent'
            att_c = 'Yes' if att.strip().title() in ['Yes', 'Y'] else 'No'
            w_c = w if w != "" else "4800"
            fee_c = fee if fee != "" and float(fee) >= 0 else "2000.0"
            cleaned_tab.append([f_id, f_type_c, w_c, c, p, ex, att_c, fee_c, out])

    # Clean Time-series
    with open(raw_ts_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers_ts = next(reader)
        rows_ts = list(reader)

    seen_ts = set()
    cleaned_ts = []
    for r in rows_ts:
        if r[0] not in seen_ts:
            seen_ts.add(r[0])
            seq = [r[0]] + [str(max(0, int(val))) if val != "" else "0" for val in r[1:]]
            cleaned_ts.append(seq)

    os.makedirs(os.path.dirname(clean_tab_path), exist_ok=True)
    os.makedirs(os.path.dirname(clean_ts_path), exist_ok=True)

    with open(clean_tab_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f).writerow(headers_tab)
        csv.writer(f).writerows(cleaned_tab)

    with open(clean_ts_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f).writerow(headers_ts)
        csv.writer(f).writerows(cleaned_ts)

    print(f"[DL Preprocess] Cleaned tabular: {clean_tab_path} ({len(cleaned_tab)} rows)")
    print(f"[DL Preprocess] Cleaned time-series: {clean_ts_path} ({len(cleaned_ts)} rows)")

if __name__ == "__main__":
    clean_dl_datasets(
        "C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/dl/data/raw/dl_raw.csv",
        "C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/dl/data/raw/dl_timeseries_raw.csv",
        "C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/dl/data/cleaned/dl_cleaned.csv",
        "C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/dl/data/cleaned/dl_timeseries_cleaned.csv"
    )
