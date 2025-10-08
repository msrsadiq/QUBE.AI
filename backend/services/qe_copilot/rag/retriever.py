from typing import List, Dict, Any
from .vector_store import VectorStoreInterface
import logging

logger = logging.getLogger(__name__)

class SmartRetriever:
    """Smart retriever with advanced retrieval strategies"""
    
    def __init__(self, vector_store: VectorStoreInterface):
        self.vector_store = vector_store
    
    async def hybrid_search(self, query: str, collection: str, k: int = 10) -> List[Dict]:
        """Hybrid search combining semantic and keyword search"""
        # Semantic search
        semantic_results = await self.vector_store.search(query, collection, k)
        
        # Keyword search (if supported by vector store)
        # For now, we'll use semantic search only
        
        # Re-rank results based on relevance
        ranked_results = self._rerank_results(semantic_results, query)
        
        return ranked_results
    
    async def multi_hop_retrieval(self, query: str, collections: List[str], max_hops: int = 2) -> List[Dict]:
        """Multi-hop retrieval across multiple collections"""
        all_results = []
        visited = set()
        
        async def retrieve_hop(q: str, hop: int):
            if hop >= max_hops:
                return
            
            for collection in collections:
                results = await self.vector_store.search(q, collection, k=5)
                
                for result in results:
                    if result["id"] not in visited:
                        visited.add(result["id"])
                        all_results.append(result)
                        
                        # Use result as query for next hop
                        if hop < max_hops - 1:
                            await retrieve_hop(result["text"][:200], hop + 1)
        
        await retrieve_hop(query, 0)
        return all_results
    
    def _rerank_results(self, results: List[Dict], query: str) -> List[Dict]:
        """Re-rank results based on relevance"""
        # Simple keyword-based re-ranking
        query_words = set(query.lower().split())
        
        for result in results:
            text_words = set(result["text"].lower().split())
            overlap = len(query_words.intersection(text_words))
            result["relevance_score"] = overlap / len(query_words) if query_words else 0
        
        # Sort by combined score (semantic distance + keyword relevance)
        results.sort(key=lambda x: (1 - x.get("distance", 1)) + x["relevance_score"], reverse=True)
        
        return results