from typing import List, Dict, Any, Optional
from .vector_store import VectorStoreInterface, ChromaDBStore
from .retriever import SmartRetriever
import logging

logger = logging.getLogger(__name__)

class RAGService:
    """Main RAG service for QECopilot"""
    
    def __init__(self, vector_store: Optional[VectorStoreInterface] = None):
        self.vector_store = vector_store or ChromaDBStore()
        self.retriever = SmartRetriever(self.vector_store)
        
        # Collection names for different data types
        self.collections = {
            "requirements": "requirements_collection",
            "test_cases": "test_cases_collection",
            "bugs": "bugs_collection",
            "test_results": "test_results_collection",
            "knowledge": "knowledge_base_collection"
        }
    
    async def index_requirements(self, project_id: str, requirements: List[Dict]) -> List[str]:
        """Index project requirements"""
        collection = f"{self.collections['requirements']}_{project_id}"
        
        # Prepare documents for indexing
        documents = []
        for req in requirements:
            doc = {
                "type": "requirement",
                "project_id": project_id,
                "title": req.get("title"),
                "description": req.get("description"),
                "acceptance_criteria": req.get("acceptance_criteria", []),
                "metadata": {
                    "requirement_id": req.get("id"),
                    "source_type": req.get("source_type"),
                    "version": req.get("version", 1)
                }
            }
            documents.append(doc)
        
        return await self.vector_store.add_documents(documents, collection)
    
    async def index_test_cases(self, project_id: str, test_cases: List[Dict]) -> List[str]:
        """Index test cases"""
        collection = f"{self.collections['test_cases']}_{project_id}"
        
        documents = []
        for tc in test_cases:
            doc = {
                "type": "test_case",
                "project_id": project_id,
                "title": tc.get("title"),
                "description": tc.get("description"),
                "test_steps": tc.get("test_steps", []),
                "expected_results": tc.get("expected_results", []),
                "metadata": {
                    "test_case_id": tc.get("id"),
                    "requirement_id": tc.get("requirement_id"),
                    "test_type": tc.get("test_type"),
                    "priority": tc.get("priority")
                }
            }
            documents.append(doc)
        
        return await self.vector_store.add_documents(documents, collection)
    
    async def find_similar_requirements(self, project_id: str, query: str, k: int = 5) -> List[Dict]:
        """Find similar requirements"""
        collection = f"{self.collections['requirements']}_{project_id}"
        return await self.vector_store.search(query, collection, k)
    
    async def find_similar_test_cases(self, project_id: str, query: str, k: int = 10, test_type: str = None) -> List[Dict]:
        """Find similar test cases"""
        collection = f"{self.collections['test_cases']}_{project_id}"
        
        filters = {"project_id": project_id}
        if test_type:
            filters["test_type"] = test_type
        
        return await self.vector_store.search(query, collection, k, filters)
    
    async def find_test_gaps(self, project_id: str, requirement: Dict) -> List[Dict]:
        """Find potential test coverage gaps for a requirement"""
        # Search for similar requirements
        similar_reqs = await self.find_similar_requirements(
            project_id, 
            requirement.get("description", ""),
            k=3
        )
        
        recommendations = []
        
        for similar_req in similar_reqs:
            # Find test cases for similar requirements
            similar_test_cases = await self.find_similar_test_cases(
                project_id,
                similar_req["text"],
                k=5
            )
            
            # Analyze gaps
            for tc in similar_test_cases:
                if not self._is_covered(requirement, tc):
                    recommendations.append({
                        "type": "potential_gap",
                        "source_requirement": similar_req["metadata"]["requirement_id"],
                        "suggested_test": tc["metadata"]["test_case_id"],
                        "reason": "Similar requirement has this test case"
                    })
        
        return recommendations
    
    def _is_covered(self, requirement: Dict, test_case: Dict) -> bool:
        """Check if requirement is covered by test case"""
        # Simple implementation - can be enhanced
        req_text = f"{requirement.get('title', '')} {requirement.get('description', '')}"
        tc_text = f"{test_case.get('text', '')}"
        
        # Check for keyword overlap
        req_words = set(req_text.lower().split())
        tc_words = set(tc_text.lower().split())
        
        overlap = len(req_words.intersection(tc_words))
        return overlap > len(req_words) * 0.3  # 30% overlap threshold