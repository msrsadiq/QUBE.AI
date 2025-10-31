from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base


class LLMConfig(Base):
    """Model to store multiple LLM configurations per project"""
    __tablename__ = "llm_configs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    
    # LLM Provider Details
    config_name = Column(String(255), nullable=False)
    provider = Column(String(50), nullable=False)
    model_name = Column(String(255), nullable=False)
    
    # Connection Details
    api_base_url = Column(String(500), nullable=True)
    api_key = Column(String(500), nullable=True)
    
    # Model Parameters - Core
    temperature = Column(String(10), default="0.7")
    max_tokens = Column(Integer, default=2048)
    top_p = Column(String(10), default="1.0")
    
    # Provider-Specific Parameters
    provider_specific_params = Column(JSON, nullable=True, default={})
    
    # Status & Validation
    is_active = Column(Boolean, default=True)
    is_validated = Column(Boolean, default=False)
    validation_status = Column(String(50), default="pending")
    validation_message = Column(Text, nullable=True)
    last_validated_at = Column(DateTime, nullable=True)
    
    # Metadata
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    project = relationship("Project", back_populates="llm_configs")
    agent_mappings = relationship("AgentLLMMapping", back_populates="llm_config")
    
    class Config:
        from_attributes = True  # ✅ Changed from orm_mode


class AgentLLMMapping(Base):
    """Model to map which LLM config each agent uses for a project"""
    __tablename__ = "agent_llm_mappings"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    agent_type = Column(String(50), nullable=False)
    llm_config_id = Column(Integer, ForeignKey("llm_configs.id"), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    llm_config = relationship("LLMConfig", back_populates="agent_mappings")
    
    class Config:
        from_attributes = True  # ✅ Changed from orm_mode