from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import hashlib
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class VectorStoreInterface(ABC):
    """Abstract interface for vector stores - makes migration easy"""
    
    @abstractmethod
    async def add_documents(self, documents: List[Dict], collection_name: str) -> List[str]:
        pass
    
    @abstractmethod
    async def search(self, query: str, collection_name: str, k: int = 5) -> List[Dict]:
        pass
    
    @abstractmethod
    async def delete(self, ids: List[str], collection_name: str) -> bool:
        pass
    
    @abstractmethod
    async def update(self, documents: List[Dict], collection_name: str) -> bool:
        pass

class ChromaDBStore(VectorStoreInterface):
    """ChromaDB implementation of vector store"""
    
    def __init__(self, persist_directory: str = "./chroma_db", embedding_model: str = "all-MiniLM-L6-v2"):
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Use sentence transformers for embeddings (free and efficient)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )
        
        self.collections = {}
        logger.info(f"Initialized ChromaDB with persist directory: {persist_directory}")
    
    def _get_or_create_collection(self, collection_name: str):
        """Get or create a collection"""
        if collection_name not in self.collections:
            try:
                self.collections[collection_name] = self.client.get_collection(
                    name=collection_name,
                    embedding_function=self.embedding_function
                )
            except:
                self.collections[collection_name] = self.client.create_collection(
                    name=collection_name,
                    embedding_function=self.embedding_function,
                    metadata={"hnsw:space": "cosine"}
                )
        return self.collections[collection_name]
    
    async def add_documents(self, documents: List[Dict], collection_name: str) -> List[str]:
        """Add documents to collection"""
        collection = self._get_or_create_collection(collection_name)
        
        ids = []
        texts = []
        metadatas = []
        
        for doc in documents:
            # Generate unique ID based on content
            doc_id = hashlib.md5(json.dumps(doc, sort_keys=True).encode()).hexdigest()
            ids.append(doc_id)
            
            # Extract text for embedding
            text = self._extract_text(doc)
            texts.append(text)
            
            # Prepare metadata
            metadata = {
                "type": doc.get("type", "unknown"),
                "project_id": doc.get("project_id"),
                "created_at": doc.get("created_at", datetime.now().isoformat()),
                "source": doc.get("source", "manual"),
                **doc.get("metadata", {})
            }
            metadatas.append(metadata)
        
        collection.add(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        
        logger.info(f"Added {len(documents)} documents to collection {collection_name}")
        return ids
    
    async def search(self, query: str, collection_name: str, k: int = 5, filters: Dict = None) -> List[Dict]:
        """Search for similar documents"""
        collection = self._get_or_create_collection(collection_name)
        
        where_clause = filters if filters else None
        
        results = collection.query(
            query_texts=[query],
            n_results=k,
            where=where_clause
        )
        
        # Format results
        formatted_results = []
        if results["ids"][0]:
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else None
                })
        
        return formatted_results
    
    async def delete(self, ids: List[str], collection_name: str) -> bool:
        """Delete documents by IDs"""
        try:
            collection = self._get_or_create_collection(collection_name)
            collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents from collection {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error deleting documents: {str(e)}")
            return False
    
    async def update(self, documents: List[Dict], collection_name: str) -> bool:
        """Update existing documents"""
        try:
            # Delete old versions
            ids = [hashlib.md5(json.dumps(doc, sort_keys=True).encode()).hexdigest() for doc in documents]
            await self.delete(ids, collection_name)
            
            # Add updated versions
            await self.add_documents(documents, collection_name)
            return True
        except Exception as e:
            logger.error(f"Error updating documents: {str(e)}")
            return False
    
    def _extract_text(self, doc: Dict) -> str:
        """Extract text from document for embedding"""
        text_parts = []
        
        # Add main content
        if "title" in doc:
            text_parts.append(f"Title: {doc['title']}")
        if "description" in doc:
            text_parts.append(f"Description: {doc['description']}")
        if "content" in doc:
            text_parts.append(f"Content: {doc['content']}")
        
        # Add test case specific fields
        if "test_steps" in doc:
            steps = " ".join([step.get("action", "") for step in doc["test_steps"]])
            text_parts.append(f"Test Steps: {steps}")
        if "expected_results" in doc:
            text_parts.append(f"Expected Results: {' '.join(doc['expected_results'])}")
        
        # Add requirement specific fields
        if "acceptance_criteria" in doc:
            text_parts.append(f"Acceptance Criteria: {' '.join(doc['acceptance_criteria'])}")
        
        return " ".join(text_parts)