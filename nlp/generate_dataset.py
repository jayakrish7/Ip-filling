import os
import csv
import random

def generate_raw_nlp_dataset(output_path: str, num_samples: int = 1200, seed: int = 42):
    """Generates synthetic raw legal clauses dataset using standard library."""
    random.seed(seed)
    clause_types = ['Claims', 'Prior_Art_Objection', 'Abstract', 'Assignment', 'Office_Action_Response']

    templates = {
        'Claims': [
            "We claim an automated neural network processor for IP filing verification comprising a memory unit and a tensor engine.",
            "A system for legal document parsing comprising: a text vectorizer, a transformer classifier, and an output queue.",
            "What is claimed is a method of generating patent claims using multi-stage heuristic algorithms.",
            "  The method of claim 1, further comprising comparing patent claim vectors against a vector database of prior art.  ",
            "A computer-implemented apparatus comprising one or more processors configured to execute deep learning models for prior art detection."
        ],
        'Prior_Art_Objection': [
            "The examiner rejects claims 1-5 under 35 U.S.C. 102 as being anticipated by patent US10984123B2 to Apex Corp on 2021-04-15.",
            "Claim 3 is rejected under 35 U.S.C. 103 as being obvious over reference US9876543A in view of US8765432B1.",
            "The prior art cited by the patent office demonstrates substantially similar claim elements as disclosed in US11223344B2.",
            "Objection under 37 CFR 1.104: The specification fails to provide written description support for the claimed invention.",
            "Rejection based on prior art reference US10555666A filed on 2019-11-20 by Cyberdyne Systems."
        ],
        'Abstract': [
            "An concise summary of the patent invention disclosing a distributed ledger framework for automated trademark registration.",
            "The present disclosure relates to deep learning architectures for natural language processing of legal filing documents.",
            "A method and apparatus for real-time risk assessment of patent applications before USPTO submission.",
            "  Abstract: System and method for processing legal contracts and extracting key clause categories automatically.  ",
            "This invention describes an intelligent agent pipeline designed for autonomous intellectual property filing workflows."
        ],
        'Assignment': [
            "This Assignment of Patent Rights is executed on 2024-01-10 between Assignor BioGenetics Inc and Assignee NovaPharm Ltd.",
            "The inventor hereby transfers, assigns, and conveys all right, title, and interest in US10123456B2 to TechCorp Global.",
            "Patent Assignment Agreement: Assignor agrees to convey worldwide patent rights to Acme Intellectual Property LLC.",
            "Assignment recorded with the USPTO assigning all rights of patent application US11998877A to Quantum Dynamics Inc.",
            "Whereas Assignor has invented new neural network hardware, Assignor assigns full ownership to Synthetic Intelligence Corp."
        ],
        'Office_Action_Response': [
            "Applicant respectfully requests reconsideration of the final rejection of claims 1-10 in light of the attached amendments.",
            "In response to the Office Action dated 2023-08-12, Applicant amends claim 1 to clarify the structural limitations.",
            "Applicant submits that reference US10984123B2 fails to teach or suggest the neural attention layer of claim 1.",
            "Response under 37 CFR 1.111: Applicant traverses the obviousness rejection and provides comparative experimental data.",
            "Applicant respectfully requests withdrawal of the objection and allowance of patent application US10445566B1."
        ]
    }

    orgs = ["Apex Corp", "Cyberdyne Systems", "BioGenetics Inc", "NovaPharm Ltd", "TechCorp Global", ""]
    dates = ["2021-04-15", "2019-11-20", "2024-01-10", "2023-08-12", ""]

    headers = ['clause_id', 'clause_type', 'clause_text', 'patent_number', 'filing_date', 'applicant_org']
    rows = []

    for i in range(num_samples):
        c_type = random.choice(clause_types)
        text = random.choice(templates[c_type])
        c_id = f"CLS-2026-{20000 + i}"
        pat_num = f"US{random.randint(1000000, 9999999)}B2" if random.random() > 0.3 else ""
        date_val = random.choice(dates)
        org_val = random.choice(orgs)

        if random.random() < 0.08:
            text = text.upper()
        if random.random() < 0.08:
            text = f"   {text}   \n"

        c_label = c_type if random.random() > 0.03 else c_type.lower()
        rows.append([c_id, c_label, text, pat_num, date_val, org_val])

    # Inject duplicates
    dupe_count = int(num_samples * 0.04)
    rows.extend(random.choices(rows, k=dupe_count))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"[NLP Dataset Generator] Created raw NLP dataset with {len(rows)} rows at: {output_path}")

if __name__ == "__main__":
    generate_raw_nlp_dataset("C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/nlp/data/raw/clauses_raw.csv")
