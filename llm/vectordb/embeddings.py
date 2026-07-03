import os
import re
import chromadb
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.utils import embedding_functions

PDF_FOLDER = "./llm/vectordb/documents"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=120,
    separators=[
        "\n\n",
        "\n",
        ". ",
        "; ",
        ", ",
        " "
    ]
)

client = chromadb.PersistentClient(path="./llm/vectordb/db/")

collection = client.get_or_create_collection(
    name="pdf_docs",
    embedding_function=embedding_functions.DefaultEmbeddingFunction()
)

BATCH_SIZE = 500

def clean_text(text: str) -> str:
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")

    # remove JSON-like blobs
    text = re.sub(r"\{[\s\S]*?\}", "", text)

    # remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()

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

        for page in pages:
            cleaned = clean_text(page.page_content)

            # skip junk pages
            if len(cleaned) < 80:
                continue

            chunks = splitter.split_text(cleaned)

            for i, chunk in enumerate(chunks):
                chunk_id = f"{file_name}_p{page.metadata.get('page', 0)}_c{i}"

                all_docs.append(chunk)

                # CLEAN METADATA (IMPORTANT FIX)
                all_metadatas.append({
                    "source_file": file_name,
                    "page": page.metadata.get("page"),
                    "page_label": page.metadata.get("page_label"),
                    "title": page.metadata.get("title")
                })

                all_ids.append(chunk_id)

    batch_insert(all_docs, all_metadatas, all_ids)

    print(f"Stored {len(all_docs)} clean chunks from PDFs")


init_embeddings()