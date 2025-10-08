# Example migration wrapper for future vector store changes
"""
# backend/services/qe_copilot/rag/qdrant_store.py

from qdrant_client import QdrantClient
from .vector_store import VectorStoreInterface

class QdrantStore(VectorStoreInterface):
    # Implement the same interface for easy migration
    def __init__(self, url: str = "localhost", port: int = 6333):
        self.client = QdrantClient(url, port=port)
    
    async def add_documents(self, documents: List[Dict], collection_name: str) -> List[str]:
        # Qdrant implementation
        pass
    
    async def search(self, query: str, collection_name: str, k: int = 5) -> List[Dict]:
        # Qdrant implementation
        pass
    
    # ... other methods

# To migrate, just change the initialization:
# rag_service = RAGService(vector_store=QdrantStore())
"""