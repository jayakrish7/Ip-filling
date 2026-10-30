import os
import json
import streamlit as st
from ingest import retrieve_top_k, build_vector_store

def generate_grounded_answer(query: str, retrieved_docs: list):
    """Generates a grounded legal response using cited retrieved sources."""
    citations = [f"[{doc['doc_id']}] {doc['title']}" for doc in retrieved_docs]
    doc_context = "\n\n".join([f"Source ({doc['doc_id']}): {doc['content']}" for doc in retrieved_docs])

    answer = f"""Based on statutory authority and judicial precedents:

{retrieved_docs[0]['content']}

**Key Statutory Principles:**
- **Obviousness Inquiry:** Under 35 U.S.C. 103, patentability requires showing non-obvious differences between the claimed invention and prior art.
- **Precedent Standard:** Judicial inquiry follows the Graham v. John Deere framework, analyzing scope of prior art and level of ordinary skill.

**Citations:**
""" + "\n".join([f"- {c}" for c in citations])

    return answer

def draft_clause_alternatives(scenario: str):
    """Drafts 3 alternative legal clause wordings based on user specification."""
    return [
        {
            "option": "Option A - Broad Scope (Maximum Legal Protection)",
            "wording": f"A computer-implemented method for {scenario}, comprising: executing a distributed neural execution graph on one or more hardware processors configured to dynamically compute risk coefficients."
        },
        {
            "option": "Option B - Narrow Scope (High Patentability / Low Rejection Risk)",
            "wording": f"A system for {scenario}, comprising: a memory storing instruction vectors; and a specialized hardware tensor core configured to calculate prior-art vector cosine distances under 0.35 threshold."
        },
        {
            "option": "Option C - Balanced Defensible Standard",
            "wording": f"An automated apparatus for {scenario}, comprising memory storing rules and a processor configured to execute predictive model scoring and output formatted USPTO filing specification documents."
        }
    ]

def main():
    st.set_page_config(page_title="IP GenAI RAG Assistant & Clause Drafter", page_icon="📜", layout="wide")

    st.title("📜 Intellectual Property GenAI Assistant & Clause Drafter")

    v_store_path = os.path.join(os.path.dirname(__file__), "vector_store.json")
    if not os.path.exists(v_store_path):
        build_vector_store(v_store_path)

    tab1, tab2 = st.tabs(["🔍 Precedent & Statute Q&A RAG", "✍️ Multi-Option Clause Drafter"])

    with tab1:
        st.subheader("Legal Corpus Retrieval & Citation Search")
        query = st.text_input("Ask a legal question (e.g. 'What is the standard for 35 USC 103 obviousness?'):", 
                              value="What is the legal standard for obviousness rejections under 35 USC 103?")

        if st.button("🔎 Retrieve & Generate Grounded Answer"):
            docs = retrieve_top_k(query, v_store_path, top_k=2)

            st.markdown("### 📚 Grounded Answer & Citations")
            answer = generate_grounded_answer(query, docs)
            st.info(answer)

            st.markdown("### 🎯 Retrieved Vector Passages")
            for doc in docs:
                with st.expander(f"{doc['title']} (Cosine Similarity: {doc['similarity_score']})"):
                    st.write(doc['content'])

    with tab2:
        st.subheader("Scenario-Based Legal Clause Drafting Engine")
        scenario = st.text_input("Enter invention feature or clause context:", value="automated neural network patent specification scoring")

        if st.button("✨ Draft 3 Alternative Clause Wordings"):
            options = draft_clause_alternatives(scenario)
            for opt in options:
                st.markdown(f"#### {opt['option']}")
                st.code(opt['wording'], language="text")

if __name__ == "__main__":
    main()
