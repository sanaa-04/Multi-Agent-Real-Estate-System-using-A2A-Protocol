import chromadb
from chromadb.utils import embedding_functions
import uuid

# Use a simple embedding function (sentence-transformers or similar if available, otherwise default)
# Since the user specified Ollama gemma2, we could use Ollama for embeddings too if set up.
# For simplicity in this demo, I'll use the default ChromaDB embedding function or a mock if needed.
# Actually, I'll use a local embedding function.

class RAGService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./marketing_agent/chroma_db")
        self.collection = self.client.get_or_create_collection(name="market_insights")
        self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    def store_insight(self, property_id: str, insight_text: str):
        # Chunking (simple)
        chunks = [insight_text[i:i+500] for i in range(0, len(insight_text), 500)]
        ids = [f"{property_id}_{i}" for i in range(len(chunks))]
        metadatas = [{"property_id": property_id} for _ in chunks]
        
        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        return ids

    def query_insights(self, query: str, n_results: int = 3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results["documents"][0] if results["documents"] else []

rag_service = RAGService()
