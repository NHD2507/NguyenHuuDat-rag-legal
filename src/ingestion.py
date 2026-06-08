from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf(pdf_path: str):
    """Load PDF and return to list page."""

    reader = PdfReader(pdf_path)

    pages = []

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:
            pages.append(
                {
                    "text": text,
                    "page": page_num + 1,
                    "source": pdf_path,
                }
            )

    return pages


def create_chunks(pages):
    """Chunk document và giữ metadata."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    chunks = []

    for page in pages:
        page_chunks = splitter.split_text(page["text"])

        for chunk in page_chunks:
            chunks.append(
                {
                    "text": chunk,
                    "page": page["page"],
                    "source": page["source"],
                }
            )

    return chunks