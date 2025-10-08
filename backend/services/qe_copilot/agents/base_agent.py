from abc import ABC, abstractmethod
from typing import Dict, Any, List
from langchain.schema import BaseMessage
from langchain.chat_models.base import BaseChatModel
import logging

class BaseAgent(ABC):
    """Base class for all QECopilot agents"""
    
    def __init__(self, llm: BaseChatModel, project_id: str):
        self.llm = llm
        self.project_id = project_id
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return results"""
        pass
    
    @abstractmethod
    def get_prompt_template(self) -> str:
        """Return the prompt template for this agent"""
        pass
    
    async def store_io(self, input_data: Dict, output_data: Dict, execution_time: int, status: str = "success"):
        """Store agent input/output for audit trail"""
        from services.storage_service import StorageService
        storage = StorageService()
        await storage.store_agent_io(
            project_id=self.project_id,
            agent_name=self.__class__.__name__,
            input_data=input_data,
            output_data=output_data,
            execution_time=execution_time,
            status=status
        )