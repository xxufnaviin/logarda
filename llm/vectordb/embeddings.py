import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

PDF_FOLDER = "./llm/vectordb/documents"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

client = chromadb.PersistentClient(path="./llm/vectordb/db/")

collection = client.get_or_create_collection(
    name="pdf_docs",
    embedding_function=embedding_functions.DefaultEmbeddingFunction()
)

BATCH_SIZE = 1000  # safe for Chroma


def batch_insert(docs, metas, ids):
    for i in range(0, len(docs), BATCH_SIZE):
        collection.add(
            documents=docs[i:i+BATCH_SIZE],
            metadatas=metas[i:i+BATCH_SIZE],
            ids=ids[i:i+BATCH_SIZE]
        )


def init_embeddings():
    existing = collection.count()
    if existing > 0:
        print(f"Chroma DB already initialized ({existing} chunks found)")
        return

    all_docs = []
    all_metadatas = []
    all_ids = []

    for file_name in os.listdir(PDF_FOLDER):
        if not file_name.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(PDF_FOLDER, file_name)

        loader = PyPDFLoader(file_path)
        pages = loader.load()

        chunks = splitter.split_documents(pages)

        for i, chunk in enumerate(chunks):
            chunk_id = f"{file_name}_chunk_{i}"

            all_docs.append(chunk.page_content)
            all_metadatas.append({
                **chunk.metadata,
                "source_file": file_name
            })
            all_ids.append(chunk_id)

    batch_insert(all_docs, all_metadatas, all_ids)

    print(f"Stored {len(all_docs)} chunks from {len(os.listdir(PDF_FOLDER))} PDFs")


init_embeddings()