import os
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

LEGAL_CORPUS = [
    {
        "doc_id": "STATUTE-35USC102",
        "title": "35 U.S.C. 102 - Conditions for Patentability; Novelty",
        "category": "Statute",
        "content": "A person shall be entitled to a patent unless the claimed invention was patented, described in a printed publication, or in public use, on sale, or otherwise available to the public before the effective filing date of the claimed invention."
    },
    {
        "doc_id": "STATUTE-35USC103",
        "title": "35 U.S.C. 103 - Conditions for Patentability; Non-Obvious Subject Matter",
        "category": "Statute",
        "content": "A patent for a claimed invention may not be obtained if the differences between the claimed invention and the prior art are such that the claimed invention as a whole would have been obvious before the effective filing date to a person having ordinary skill in the art."
    },
    {
        "doc_id": "PRECEDENT-GRAHAM-1966",
        "title": "Graham v. John Deere Co., 383 U.S. 1 (1966)",
        "category": "Precedent",
        "content": "Sets forth the primary factual inquiries for obviousness: (1) scope and content of prior art, (2) differences between prior art and claims, (3) level of ordinary skill in the art, and (4) secondary considerations such as commercial success and long-felt need."
    },
    {
        "doc_id": "PRECEDENT-KSR-2007",
        "title": "KSR Int'l Co. v. Teleflex Inc., 550 U.S. 398 (2007)",
        "category": "Precedent",
        "content": "Rejects rigid application of the Teaching-Suggestion-Motivation (TSM) test. Analysis of obviousness may consider predictable results, design incentives, and market demand combining known elements."
    },
    {
        "doc_id": "TEMPLATE-NEURAL-CLAIM",
        "title": "Standard Claim Template for AI/ML Hardware Systems",
        "category": "Template",
        "content": "A system comprising: a memory storing instructions; and one or more processors configured by the instructions to perform operations comprising: ingesting legal clause vectors, computing prior art similarity scores, and executing a neural risk scoring model."
    }
]

def build_vector_store(output_path: str):
    """
    Chunks and indexes legal corpus into a searchable vector index.
    Saves vector representations and corpus metadata.
    """
    print(f"[RAG Ingest] Ingesting {len(LEGAL_CORPUS)} legal statutes and precedents...")
    
    texts = [doc["content"] for doc in LEGAL_CORPUS]
    vectorizer = TfidfVectorizer(stop_words='english')
    embeddings = vectorizer.fit_transform(texts).toarray()

    vector_store = {
        "corpus": LEGAL_CORPUS,
        "vocabulary": vectorizer.get_feature_names_out().tolist(),
        "idf": vectorizer.idf_.tolist()
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(vector_store, f, indent=4)

    print(f"[RAG Ingest] Saved legal vector store index to: {output_path}")

def retrieve_top_k(query: str, vector_store_path: str, top_k: int = 2):
    """
    Retrieves top_k relevant legal documents with citation confidence scores.
    """
    with open(vector_store_path, 'r') as f:
        vstore = json.load(f)

    corpus = vstore["corpus"]
    texts = [doc["content"] for doc in corpus]

    vectorizer = TfidfVectorizer(vocabulary=vstore["vocabulary"])
    vectorizer.idf_ = np.array(vstore["idf"])

    doc_matrix = vectorizer.transform(texts).toarray()
    query_vec = vectorizer.transform([query]).toarray()

    sims = cosine_similarity(query_vec, doc_matrix)[0]
    top_indices = sims.argsort()[-top_k:][::-1]

    results = []
    for idx in top_indices:
        results.append({
            "doc_id": corpus[idx]["doc_id"],
            "title": corpus[idx]["title"],
            "category": corpus[idx]["category"],
            "content": corpus[idx]["content"],
            "similarity_score": round(float(sims[idx]), 4)
        })

    return results

if __name__ == "__main__":
    v_path = "C:/Users/jayak/.gemini/antigravity/scratch/IP_Filing_GenAI_Project/genai_rag/vector_store.json"
    build_vector_store(v_path)
    res = retrieve_top_k("obviousness prior art combination", v_path)
    print("\nSample Retrieval Test:")
    for r in res:
        print(f" -> [{r['doc_id']}] {r['title']} (Score: {r['similarity_score']})")
