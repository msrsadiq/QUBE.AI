from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db, get_current_user
from app.models.project import Project
from app.models.llm_config import LLMConfig
from app.schemas.llm_config import (
    LLMConfigCreate, LLMConfigUpdate, LLMConfigResponse,
    LLMConfigValidationRequest, LLMConfigValidationResponse,
    AgentLLMAssignRequest, AgentLLMAssignResponse
)
from app.services.llm_config_service import LLMConfigService, AgentLLMService

router = APIRouter(prefix="/api/v1/projects/{project_id}/llm-configs", tags=["LLM Configuration"])


@router.post("", response_model=LLMConfigResponse, status_code=status.HTTP_201_CREATED)
async def create_llm_config(
    project_id: int,
    config: LLMConfigCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create a new LLM configuration for a project."""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Create the config
    db_config = LLMConfigService.create_llm_config(db, project_id, config)
    
    response = LLMConfigResponse.from_orm(db_config)
    response = LLMConfigResponse.mask_sensitive_data(response)
    
    return response


@router.get("", response_model=List[LLMConfigResponse])
async def get_all_llm_configs(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all LLM configurations for a project"""
    # Verify project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    configs = LLMConfigService.get_all_llm_configs(db, project_id)
    
    responses = [LLMConfigResponse.from_orm(config) for config in configs]
    responses = [LLMConfigResponse.mask_sensitive_data(r) for r in responses]
    
    return responses


@router.get("/{config_id}", response_model=LLMConfigResponse)
async def get_llm_config(
    project_id: int,
    config_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get a specific LLM configuration"""
    config = LLMConfigService.get_llm_config(db, config_id, project_id)
    
    if not config:
        raise HTTPException(status_code=404, detail="LLM config not found")
    
    response = LLMConfigResponse.from_orm(config)
    response = LLMConfigResponse.mask_sensitive_data(response)
    
    return response


@router.put("/{config_id}", response_model=LLMConfigResponse)
async def update_llm_config(
    project_id: int,
    config_id: int,
    update_data: LLMConfigUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update an LLM configuration"""
    try:
        config = LLMConfigService.update_llm_config(db, config_id, project_id, update_data)
        response = LLMConfigResponse.from_orm(config)
        response = LLMConfigResponse.mask_sensitive_data(response)
        return response
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{config_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_llm_config(
    project_id: int,
    config_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete an LLM configuration"""
    try:
        LLMConfigService.delete_llm_config(db, config_id, project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/validate", response_model=LLMConfigValidationResponse)
async def validate_llm_config(
    validation_req: LLMConfigValidationRequest,
    current_user = Depends(get_current_user)
):
    """Validate LLM configuration before saving."""
    result = await LLMConfigService.validate_llm_config(validation_req)
    return result


@router.post("/{config_id}/validate", response_model=LLMConfigValidationResponse)
async def revalidate_llm_config(
    project_id: int,
    config_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Revalidate an existing LLM configuration"""
    config = LLMConfigService.get_llm_config(db, config_id, project_id)
    
    if not config:
        raise HTTPException(status_code=404, detail="LLM config not found")
    
    validation_req = LLMConfigValidationRequest(
        provider=config.provider,
        model_name=config.model_name,
        api_base_url=config.api_base_url,
        api_key=config.api_key,
        temperature=config.temperature,
        max_tokens=config.max_tokens
    )
    
    result = await LLMConfigService.validate_llm_config(validation_req)
    
    # Update validation status in DB
    config.is_validated = result.is_valid
    config.validation_status = result.status
    config.validation_message = result.message
    config.last_validated_at = result.timestamp
    
    db.commit()
    db.refresh(config)
    
    return result


# Agent-LLM Mapping Routes

@router.post("/assign", response_model=AgentLLMAssignResponse, status_code=status.HTTP_201_CREATED)
async def assign_llm_to_agent(
    project_id: int,
    assign_req: AgentLLMAssignRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Assign an LLM configuration to a specific agent."""
    try:
        mapping = AgentLLMService.assign_llm_to_agent(
            db, project_id, assign_req.agent_type, assign_req.llm_config_id
        )
        return mapping
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/agents", response_model=List[AgentLLMAssignResponse])
async def get_all_agent_mappings(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all agent-LLM mappings for a project"""
    mappings = AgentLLMService.get_all_agent_mappings(db, project_id)
    return mappings


@router.get("/agents/{agent_type}", response_model=LLMConfigResponse)
async def get_agent_llm_config(
    project_id: int,
    agent_type: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get the LLM config assigned to a specific agent"""
    config = AgentLLMService.get_agent_llm_config(db, project_id, agent_type)
    
    if not config:
        raise HTTPException(
            status_code=404,
            detail="No LLM config assigned to this agent. Please configure in project settings."
        )
    
    response = LLMConfigResponse.from_orm(config)
    response = LLMConfigResponse.mask_sensitive_data(response)
    
    return response