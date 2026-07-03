import chromadb
from chromadb.utils import embedding_functions


class ChromaDB:
    client:str
    collection:str

    def init_client():
        ChromaDB.client =  chromadb.PersistentClient(path="./vectordb/db/")
        ChromaDB.collection = ChromaDB.client.get_or_create_collection(
            name="pdf_docs",
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )

    def query(text:str):
        results = ChromaDB.collection.query(
                query_texts=[text],
                n_results=1
            )
        
        return results["documents"][0]