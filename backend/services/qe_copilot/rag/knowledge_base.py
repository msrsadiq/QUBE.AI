from typing import List, Dict, Any
import yaml
import json
from pathlib import Path
from .rag_service import RAGService
import logging

logger = logging.getLogger(__name__)

class KnowledgeBase:
    """Manages testing knowledge base for RAG"""
    
    def __init__(self, rag_service: RAGService):
        self.rag_service = rag_service
        self.knowledge_dir = Path("./knowledge_base")
        self.knowledge_dir.mkdir(exist_ok=True)
    
    async def load_testing_patterns(self):
        """Load testing patterns and best practices into RAG"""
        patterns = [
            {
                "title": "API Testing Best Practices",
                "content": """
                1. Test happy path scenarios first
                2. Include negative test cases for error handling
                3. Validate response status codes
                4. Check response time and performance
                5. Verify response schema and data types
                6. Test with different authentication scenarios
                7. Include boundary value testing
                8. Test pagination and filtering
                9. Validate error messages and codes
                10. Test idempotency for PUT/DELETE operations
                """,
                "tags": ["api", "best_practices"]
            },
            {
                "title": "Security Testing Checklist",
                "content": """
                1. SQL Injection testing
                2. Cross-Site Scripting (XSS) validation
                3. Authentication bypass attempts
                4. Authorization and access control
                5. Session management testing
                6. Input validation testing
                7. File upload security
                8. API rate limiting
                9. Sensitive data exposure checks
                10. HTTPS/TLS configuration
                """,
                "tags": ["security", "checklist"]
            },
            {
                "title": "Performance Testing Guidelines",
                "content": """
                1. Define performance criteria and SLAs
                2. Identify critical user journeys
                3. Establish baseline metrics
                4. Load testing with expected traffic
                5. Stress testing beyond limits
                6. Spike testing for sudden load
                7. Volume testing with large data
                8. Endurance testing for memory leaks
                9. Monitor resource utilization
                10. Analyze bottlenecks and optimize
                """,
                "tags": ["performance", "guidelines"]
            },
            {
                "title": "Mobile Testing Considerations",
                "content": """
                1. Test on multiple device sizes
                2. Portrait and landscape orientations
                3. Different OS versions
                4. Network conditions (3G/4G/5G/WiFi)
                5. Battery consumption testing
                6. Interruption testing (calls, notifications)
                7. Gesture and touch interactions
                8. App permissions testing
                9. Offline functionality
                10. App update scenarios
                """,
                "tags": ["mobile", "testing"]
            }
        ]
        
        # Index patterns into knowledge base
        documents = []
        for pattern in patterns:
            doc = {
                "type": "knowledge",
                "title": pattern["title"],
                "content": pattern["content"],
                "metadata": {
                    "tags": pattern["tags"]
                }
            }
            documents.append(doc)
        
        await self.rag_service.vector_store.add_documents(
            documents, 
            "knowledge_base_collection"
        )
        
        logger.info(f"Loaded {len(patterns)} testing patterns into knowledge base")
    
    async def search_knowledge(self, query: str, tags: List[str] = None) -> List[Dict]:
        """Search knowledge base"""
        filters = {"tags": {"$in": tags}} if tags else None
        
        return await self.rag_service.vector_store.search(
            query,
            "knowledge_base_collection",
            k=5,
            filters=filters
        )
    
    async def add_custom_knowledge(self, title: str, content: str, tags: List[str]):
        """Add custom knowledge to the base"""
        doc = {
            "type": "custom_knowledge",
            "title": title,
            "content": content,
            "metadata": {
                "tags": tags,
                "source": "user_defined"
            }
        }
        
        await self.rag_service.vector_store.add_documents(
            [doc],
            "knowledge_base_collection"
        )
        
        logger.info(f"Added custom knowledge: {title}")