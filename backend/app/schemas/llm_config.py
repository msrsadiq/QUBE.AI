from typing import Optional, Any
from pydantic import BaseModel, ConfigDict


class LLMConfigCreate(BaseModel):
    config_name: str
    provider: str
    model_name: str
    api_base_url: Optional[str] = None
    api_key: Optional[str] = None
    temperature: str = "0.7"
    max_tokens: int = 2048
    top_p: str = "1.0"
    provider_specific_params: Optional[dict] = None
    
    model_config = ConfigDict(protected_namespaces=())


class LLMConfigUpdate(BaseModel):
    config_name: Optional[str] = None
    temperature: Optional[str] = None
    max_tokens: Optional[int] = None
    top_p: Optional[str] = None
    provider_specific_params: Optional[dict] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    
    model_config = ConfigDict(protected_namespaces=())


class LLMConfigResponse(BaseModel):
    id: int
    project_id: int
    config_name: str
    provider: str
    model_name: str
    api_base_url: Optional[str]
    temperature: str
    max_tokens: int
    top_p: str
    is_active: bool
    is_validated: bool
    is_default: bool
    validation_status: str
    created_at: Any
    updated_at: Any
    
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())


class LLMConfigValidationRequest(BaseModel):
    provider: str
    model_name: str
    api_base_url: str
    temperature: str = "0.7"
    max_tokens: int = 2048
    
    model_config = ConfigDict(protected_namespaces=())


class LLMConfigValidationResponse(BaseModel):
    is_valid: bool
    message: str
    model_name: str
    provider: str
    
    model_config = ConfigDict(protected_namespaces=())


class AgentLLMAssignRequest(BaseModel):
    """Schema to assign LLM config to an agent"""
    agent_type: str
    llm_config_id: int
    
    model_config = ConfigDict(protected_namespaces=())


class AgentLLMMapping(BaseModel):
    """Schema for agent-LLM mapping response"""
    id: int
    project_id: int
    agent_type: str
    llm_config_id: int
    created_at: Any
    updated_at: Any
    
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())


class AgentLLMGetResponse(BaseModel):
    """Schema to get LLM config for an agent"""
    agent_type: str
    llm_config: LLMConfigResponse
    
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())