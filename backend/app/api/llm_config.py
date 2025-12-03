"""
LLM Configuration API Routes
----------------------------
REST API endpoints for managing LLM configurations.

Endpoints:
- POST /api/llm-configs/ - Create new configuration
- GET /api/llm-configs/project/{project_id} - List project configs
- GET /api/llm-configs/{config_id} - Get specific config
- PUT /api/llm-configs/{config_id} - Update configuration
- DELETE /api/llm-configs/{config_id} - Delete configuration
- POST /api/llm-configs/{config_id}/test - Test configuration
- GET /api/llm-configs/{config_id}/health - Health check
- GET /api/llm-configs/project/{project_id}/usage - Usage summary
- WS /api/llm-configs/project/{project_id}/monitor - Real-time monitoring

All endpoints require authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.schemas.llm_config import (
    LLMConfigCreate,
    LLMConfigUpdate,
    LLMConfigResponse,
    LLMTestRequest,
    LLMTestResponse,
    HealthCheckResponse
)
from app.services.llm_config_service import LLMConfigService
from app.services.llm_service import LLMService
from app.services.token_monitor_service import token_monitor

router = APIRouter(prefix="/api/llm-configs", tags=["LLM Configuration"])


@router.post("/", response_model=LLMConfigResponse, status_code=201)
async def create_llm_config(
    config_data: LLMConfigCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new LLM configuration for a project.
    
    Args:
        config_data: Configuration data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created LLM configuration
        
    Raises:
        HTTPException: If project not found or validation fails
    """
    try:
        service = LLMConfigService(db)
        config = service.create_config(config_data)
        return config
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create configuration: {str(e)}")


@router.get("/project/{project_id}", response_model=List[LLMConfigResponse])
async def get_project_configs(
    project_id: int,
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all LLM configurations for a project.
    
    Args:
        project_id: Project ID
        include_inactive: Include inactive configurations
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List of LLM configurations
    """
    service = LLMConfigService(db)
    configs = service.get_project_configs(project_id, include_inactive)
    return configs


@router.get("/{config_id}", response_model=LLMConfigResponse)
async def get_llm_config(
    config_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific LLM configuration by ID.
    
    Args:
        config_id: Configuration ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        LLM configuration
        
    Raises:
        HTTPException: If configuration not found
    """
    service = LLMConfigService(db)
    config = service.get_config(config_id)
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    return config


@router.put("/{config_id}", response_model=LLMConfigResponse)
async def update_llm_config(
    config_id: int,
    config_data: LLMConfigUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing LLM configuration.
    
    Args:
        config_id: Configuration ID
        config_data: Update data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated configuration
        
    Raises:
        HTTPException: If configuration not found
    """
    service = LLMConfigService(db)
    config = service.update_config(config_id, config_data)
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    return config


@router.delete("/{config_id}", status_code=204)
async def delete_llm_config(
    config_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete an LLM configuration.
    
    Args:
        config_id: Configuration ID
        db: Database session
        current_user: Authenticated user
        
    Raises:
        HTTPException: If configuration not found
    """
    service = LLMConfigService(db)
    deleted = service.delete_config(config_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    return None


@router.post("/{config_id}/test", response_model=LLMTestResponse)
async def test_llm_config(
    config_id: int,
    test_request: LLMTestRequest = LLMTestRequest(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Test an LLM configuration with a sample prompt.
    
    Args:
        config_id: Configuration ID
        test_request: Test request with prompt
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Test response with success status and metrics
        
    Raises:
        HTTPException: If configuration not found
    """
    config_service = LLMConfigService(db)
    config = config_service.get_config(config_id)
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    llm_service = LLMService(db)
    result = await llm_service.test_model(config, test_request)
    
    return result


@router.get("/{config_id}/health", response_model=HealthCheckResponse)
async def check_llm_health(
    config_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Perform health check on an LLM configuration.
    
    Args:
        config_id: Configuration ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Health check response
        
    Raises:
        HTTPException: If configuration not found
    """
    config_service = LLMConfigService(db)
    config = config_service.get_config(config_id)
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    llm_service = LLMService(db)
    health_data = await llm_service.check_health(config)
    
    return HealthCheckResponse(**health_data)


@router.get("/project/{project_id}/usage")
async def get_usage_summary(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get token usage summary for all configurations in a project.
    
    Args:
        project_id: Project ID
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Usage summary with token counts and costs
    """
    service = LLMConfigService(db)
    summary = service.get_usage_summary(project_id)
    return summary


@router.websocket("/project/{project_id}/monitor")
async def monitor_token_usage(
    websocket: WebSocket,
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time token usage monitoring.
    
    Broadcasts token usage updates every 5 seconds to all connected clients.
    
    Args:
        websocket: WebSocket connection
        project_id: Project ID to monitor
        db: Database session
    """
    await token_monitor.connect(websocket, project_id)
    
    try:
        # Keep connection alive
        while True:
            # Receive messages (for keep-alive or commands)
            data = await websocket.receive_text()
            
            # Handle commands if needed
            # For now, just echo back
            if data == "ping":
                await websocket.send_text("pong")
    
    except WebSocketDisconnect:
        token_monitor.disconnect(websocket, project_id)