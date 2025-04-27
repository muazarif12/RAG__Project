from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS, Chroma
import os

class HadithEmbedder:
    def __init__(self, model_name="BAAI/bge-small-en"):
        self.embedding_model = HuggingFaceEmbeddings(model_name=model_name)
        
    def create_vector_store(self, documents, save_path="data/vector_store"):
        os.makedirs(save_path, exist_ok=True)
        
        texts = [doc.page_content for doc in documents]
        metadata = [doc.metadata for doc in documents]
        
        # Using Chroma (you can switch to FAISS if preferred)
        vector_store = Chroma.from_texts(
            texts=texts,
            embedding=self.embedding_model,
            metadatas=metadata,
            persist_directory=save_path
        )
        
        vector_store.persist()
        return vector_store