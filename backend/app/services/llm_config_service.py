from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import httpx
import json

from app.models.llm_config import LLMConfig, AgentLLMMapping
from app.schemas.llm_config import (
    LLMConfigCreate, LLMConfigUpdate, LLMConfigValidationRequest,
    LLMConfigValidationResponse
)


class LLMConfigService:
    """Service for managing LLM configurations"""
    
    @staticmethod
    def create_llm_config(db: Session, project_id: int, config: LLMConfigCreate) -> LLMConfig:
        """Create a new LLM configuration"""
        
        # If setting as default, unset other defaults for this project
        if config.is_default:
            db.query(LLMConfig).filter(
                LLMConfig.project_id == project_id,
                LLMConfig.is_default == True
            ).update({"is_default": False})
        
        db_config = LLMConfig(
            project_id=project_id,
            config_name=config.config_name,
            provider=config.provider.value,
            model_name=config.model_name,
            api_base_url=config.api_base_url,
            api_key=config.api_key,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            top_p=config.top_p,
            provider_specific_params=config.provider_specific_params or {},
            is_default=config.is_default
        )
        
        db.add(db_config)
        db.commit()
        db.refresh(db_config)
        
        return db_config
    
    @staticmethod
    def get_llm_config(db: Session, config_id: int, project_id: int) -> Optional[LLMConfig]:
        """Get a specific LLM configuration"""
        return db.query(LLMConfig).filter(
            LLMConfig.id == config_id,
            LLMConfig.project_id == project_id
        ).first()
    
    @staticmethod
    def get_all_llm_configs(db: Session, project_id: int) -> List[LLMConfig]:
        """Get all LLM configurations for a project"""
        return db.query(LLMConfig).filter(
            LLMConfig.project_id == project_id
        ).order_by(LLMConfig.created_at.desc()).all()
    
    @staticmethod
    def get_default_llm_config(db: Session, project_id: int) -> Optional[LLMConfig]:
        """Get default LLM configuration for a project"""
        return db.query(LLMConfig).filter(
            LLMConfig.project_id == project_id,
            LLMConfig.is_default == True
        ).first()
    
    @staticmethod
    def update_llm_config(db: Session, config_id: int, project_id: int, 
                         update_data: LLMConfigUpdate) -> LLMConfig:
        """Update an LLM configuration"""
        db_config = LLMConfigService.get_llm_config(db, config_id, project_id)
        
        if not db_config:
            raise ValueError(f"LLM config {config_id} not found")
        
        # Handle default setting
        if update_data.is_default is True:
            db.query(LLMConfig).filter(
                LLMConfig.project_id == project_id,
                LLMConfig.is_default == True,
                LLMConfig.id != config_id
            ).update({"is_default": False})
        
        update_dict = update_data.dict(exclude_unset=True)
        
        for field, value in update_dict.items():
            if value is not None:
                setattr(db_config, field, value)
        
        db_config.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_config)
        
        return db_config
    
    @staticmethod
    def delete_llm_config(db: Session, config_id: int, project_id: int) -> bool:
        """Delete an LLM configuration"""
        db_config = LLMConfigService.get_llm_config(db, config_id, project_id)
        
        if not db_config:
            raise ValueError(f"LLM config {config_id} not found")
        
        # Clean up agent mappings
        db.query(AgentLLMMapping).filter(
            AgentLLMMapping.llm_config_id == config_id
        ).delete()
        
        db.delete(db_config)
        db.commit()
        
        return True
    
    @staticmethod
    async def validate_llm_config(validation_req: LLMConfigValidationRequest) -> LLMConfigValidationResponse:
        """Validate LLM configuration by attempting a test call."""
        
        try:
            if validation_req.provider.value == "ollama":
                return await LLMConfigService._validate_ollama(validation_req)
            elif validation_req.provider.value == "openai":
                return await LLMConfigService._validate_openai(validation_req)
            elif validation_req.provider.value == "anthropic":
                return await LLMConfigService._validate_anthropic(validation_req)
            elif validation_req.provider.value == "huggingface":
                return await LLMConfigService._validate_huggingface(validation_req)
            else:
                return LLMConfigValidationResponse(
                    is_valid=False,
                    status="failed",
                    message=f"Unknown provider: {validation_req.provider.value}",
                    provider=validation_req.provider.value,
                    model_name=validation_req.model_name
                )
        
        except Exception as e:
            return LLMConfigValidationResponse(
                is_valid=False,
                status="failed",
                message=f"Validation error: {str(e)}",
                provider=validation_req.provider.value,
                model_name=validation_req.model_name
            )
    
    @staticmethod
    async def _validate_ollama(req: LLMConfigValidationRequest) -> LLMConfigValidationResponse:
        """Validate Ollama configuration"""
        base_url = req.api_base_url or "http://localhost:11434"
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{base_url}/api/generate",
                    json={
                        "model": req.model_name,
                        "prompt": "test",
                        "stream": False,
                        "temperature": float(req.temperature),
                    },
                    timeout=15.0
                )
                
                if response.status_code == 200:
                    return LLMConfigValidationResponse(
                        is_valid=True,
                        status="success",
                        message=f"Successfully connected to Ollama model '{req.model_name}'",
                        provider="ollama",
                        model_name=req.model_name
                    )
                else:
                    return LLMConfigValidationResponse(
                        is_valid=False,
                        status="failed",
                        message=f"Ollama returned status code {response.status_code}: {response.text}",
                        provider="ollama",
                        model_name=req.model_name
                    )
            
            except httpx.ConnectError as e:
                return LLMConfigValidationResponse(
                    is_valid=False,
                    status="failed",
                    message=f"Cannot connect to Ollama at {base_url}. Make sure Ollama is running.",
                    provider="ollama",
                    model_name=req.model_name
                )
            except Exception as e:
                return LLMConfigValidationResponse(
                    is_valid=False,
                    status="failed",
                    message=f"Ollama validation failed: {str(e)}",
                    provider="ollama",
                    model_name=req.model_name
                )
    
    @staticmethod
    async def _validate_openai(req: LLMConfigValidationRequest) -> LLMConfigValidationResponse:
        """Validate OpenAI configuration"""
        if not req.api_key:
            return LLMConfigValidationResponse(
                is_valid=False,
                status="failed",
                message="API key is required for OpenAI",
                provider="openai",
                model_name=req.model_name
            )
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {req.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": req.model_name,
                        "messages": [{"role": "user", "content": "test"}],
                        "max_tokens": 10,
                        "temperature": float(req.temperature)
                    },
                    timeout=15.0
                )
                
                if response.status_code == 200:
                    return LLMConfigValidationResponse(
                        is_valid=True,
                        status="success",
                        message=f"Successfully connected to OpenAI model '{req.model_name}'",
                        provider="openai",
                        model_name=req.model_name
                    )
                else:
                    error_msg = response.json().get("error", {}).get("message", response.text)
                    return LLMConfigValidationResponse(
                        is_valid=False,
                        status="failed",
                        message=f"OpenAI API error: {error_msg}",
                        provider="openai",
                        model_name=req.model_name
                    )
            
            except Exception as e:
                return LLMConfigValidationResponse(
                    is_valid=False,
                    status="failed",
                    message=f"OpenAI validation failed: {str(e)}",
                    provider="openai",
                    model_name=req.model_name
                )
    
    @staticmethod
    async def _validate_anthropic(req: LLMConfigValidationRequest) -> LLMConfigValidationResponse:
        """Validate Anthropic configuration"""
        if not req.api_key:
            return LLMConfigValidationResponse(
                is_valid=False,
                status="failed",
                message="API key is required for Anthropic",
                provider="anthropic",
                model_name=req.model_name
            )
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": req.api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json"
                    },
                    json={
                        "model": req.model_name,
                        "max_tokens": 10,
                        "messages": [{"role": "user", "content": "test"}]
                    },
                    timeout=15.0
                )
                
                if response.status_code == 200:
                    return LLMConfigValidationResponse(
                        is_valid=True,
                        status="success",
                        message=f"Successfully connected to Anthropic model '{req.model_name}'",
                        provider="anthropic",
                        model_name=req.model_name
                    )
                else:
                    return LLMConfigValidationResponse(
                        is_valid=False,
                        status="failed",
                        message=f"Anthropic API error: {response.text}",
                        provider="anthropic",
                        model_name=req.model_name
                    )
            
            except Exception as e:
                return LLMConfigValidationResponse(
                    is_valid=False,
                    status="failed",
                    message=f"Anthropic validation failed: {str(e)}",
                    provider="anthropic",
                    model_name=req.model_name
                )
    
    @staticmethod
    async def _validate_huggingface(req: LLMConfigValidationRequest) -> LLMConfigValidationResponse:
        """Validate HuggingFace configuration"""
        if not req.api_key:
            return LLMConfigValidationResponse(
                is_valid=False,
                status="failed",
                message="API key is required for HuggingFace",
                provider="huggingface",
                model_name=req.model_name
            )
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"https://api-inference.huggingface.co/models/{req.model_name}",
                    headers={"Authorization": f"Bearer {req.api_key}"},
                    json={"inputs": "test"},
                    timeout=15.0
                )
                
                if response.status_code == 200:
                    return LLMConfigValidationResponse(
                        is_valid=True,
                        status="success",
                        message=f"Successfully connected to HuggingFace model '{req.model_name}'",
                        provider="huggingface",
                        model_name=req.model_name
                    )
                else:
                    return LLMConfigValidationResponse(
                        is_valid=False,
                        status="failed",
                        message=f"HuggingFace API error: {response.text}",
                        provider="huggingface",
                        model_name=req.model_name
                    )
            
            except Exception as e:
                return LLMConfigValidationResponse(
                    is_valid=False,
                    status="failed",
                    message=f"HuggingFace validation failed: {str(e)}",
                    provider="huggingface",
                    model_name=req.model_name
                )


class AgentLLMService:
    """Service for managing agent-LLM mappings"""
    
    @staticmethod
    def assign_llm_to_agent(db: Session, project_id: int, agent_type: str, 
                           llm_config_id: int) -> AgentLLMMapping:
        """Assign an LLM config to an agent"""
        
        # Verify LLM config exists
        llm_config = db.query(LLMConfig).filter(
            LLMConfig.id == llm_config_id,
            LLMConfig.project_id == project_id
        ).first()
        
        if not llm_config:
            raise ValueError(f"LLM config {llm_config_id} not found for project {project_id}")
        
        # Check if mapping already exists
        existing = db.query(AgentLLMMapping).filter(
            AgentLLMMapping.project_id == project_id,
            AgentLLMMapping.agent_type == agent_type
        ).first()
        
        if existing:
            existing.llm_config_id = llm_config_id
            existing.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return existing
        
        # Create new mapping
        mapping = AgentLLMMapping(
            project_id=project_id,
            agent_type=agent_type,
            llm_config_id=llm_config_id
        )
        
        db.add(mapping)
        db.commit()
        db.refresh(mapping)
        
        return mapping
    
    @staticmethod
    def get_agent_llm_config(db: Session, project_id: int, agent_type: str) -> Optional[LLMConfig]:
        """Get the LLM config assigned to an agent"""
        mapping = db.query(AgentLLMMapping).filter(
            AgentLLMMapping.project_id == project_id,
            AgentLLMMapping.agent_type == agent_type
        ).first()
        
        if mapping:
            return mapping.llm_config
        
        # Fall back to default config
        return LLMConfigService.get_default_llm_config(db, project_id)
    
    @staticmethod
    def get_all_agent_mappings(db: Session, project_id: int) -> List[AgentLLMMapping]:
        """Get all agent-LLM mappings for a project"""
        return db.query(AgentLLMMapping).filter(
            AgentLLMMapping.project_id == project_id
        ).all()