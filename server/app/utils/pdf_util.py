# utils/pdf_utils.py
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_chunk_pdf(file_path: str) -> list[dict]:
    # load PDF
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()

    # chunk with overlap
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    return [
        {"text": chunk.page_content, "pageNumber": chunk.metadata["page"]}
        for chunk in chunks
    ]
