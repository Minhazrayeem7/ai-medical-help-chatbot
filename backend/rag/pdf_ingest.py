# IMPORTS: Load document loaders, text splitters, vector store, and embeddings
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# CONFIGURATION: Define path for the vector database
DB_PATH="vector_db"

# PDF INGESTION: Read, split, and embed PDF documents into the vector database
def ingest_pdf(pdf_path):

    loader=PyPDFLoader(pdf_path)
    docs=loader.load()

    splitter=RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    chunks=splitter.split_documents(docs)

    embeddings=HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Load existing DB or create new
    if os.path.exists(DB_PATH):
        db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
        new_db = FAISS.from_documents(chunks, embeddings)
        db.merge_from(new_db)
    else:
        db = FAISS.from_documents(chunks, embeddings)

    db.save_local(DB_PATH)

    return "PDF added to knowledge base"

# TEXT/OCR INGESTION: Process and store text (like image OCR) into the vector database
def ingest_text(text, source="OCR Image"):

    doc = Document(page_content=text, metadata={"source": source})

    splitter=RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200
    )

    chunks=splitter.split_documents([doc])

    embeddings=HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Load existing DB or create new
    if os.path.exists(DB_PATH):
        db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
        new_db = FAISS.from_documents(chunks, embeddings)
        db.merge_from(new_db)
    else:
        db = FAISS.from_documents(chunks, embeddings)

    db.save_local(DB_PATH)

    return "Image description added to knowledge base"