"""
LLM Configuration API Routes
----------------------------
FastAPI router for LLM configuration management.

This module will be implemented in Phase 3.
For now, it provides placeholder endpoints to prevent import errors.

Future Implementation (Phase 3):
    POST   /api/llm-configs/          - Add LLM configuration to project
    GET    /api/llm-configs/{project_id} - Get all LLM configs for project
    PUT    /api/llm-configs/{id}      - Update LLM configuration
    DELETE /api/llm-configs/{id}      - Delete LLM configuration
"""

from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.models.user import User

# Create router with prefix and tags
router = APIRouter(prefix="/llm-configs", tags=["LLM Configuration"])


@router.get("/")
async def list_llm_configs(
    current_user: User = Depends(get_current_user)
):
    """
    Placeholder endpoint for listing LLM configurations.
    
    Will be implemented in Phase 3.
    
    Args:
        current_user: Authenticated user
        
    Returns:
        dict: Placeholder response
    """
    return {
        "message": "LLM Configuration endpoints - Coming in Phase 3",
        "endpoints": [
            "POST /api/llm-configs/ - Add LLM config",
            "GET /api/llm-configs/{project_id} - List configs for project",
            "PUT /api/llm-configs/{id} - Update config",
            "DELETE /api/llm-configs/{id} - Delete config"
        ]
    }