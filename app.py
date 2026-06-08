import streamlit as st
from src.generator import generate_answer
from pathlib import Path

from src.ingestion import (
    load_pdf,
    create_chunks,
)

from src.retriever import LegalRetriever

st.set_page_config(
    page_title="Legal RAG Assistant",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Legal RAG Assistant")
@st.cache_resource
def initialize_retriever():

    all_pages = []

    pdf_files = Path("data").glob("*.pdf")

    for pdf_file in pdf_files:

        pages = load_pdf(str(pdf_file))

        all_pages.extend(pages)

    chunks = create_chunks(pages)

    retriever = LegalRetriever()

    retriever.add_documents(chunks)

    return retriever

retriever = initialize_retriever()

question = st.chat_input(
    "Nhập câu hỏi..."
)

if question:

    results = retriever.retrieve(question)

    distance = results["distances"][0][0]

    st.metric(
        "Relevance Score",
        round(distance, 3)
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n\n".join(documents)

    st.subheader("Answer")

    answer = generate_answer(
        question,
        context
    )

    st.write(answer)
    # st.write(context[:1500])

    with st.expander("Sources"):
        for meta in metadatas:
            st.write(
                f"Page {meta['page']}"
            )

    with st.expander("Retrieved Chunks"):
        for doc in documents:
            st.write(doc[:1000])
            st.divider()

