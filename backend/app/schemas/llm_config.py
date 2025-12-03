"""
LLM Configuration Schemas
-------------------------
Pydantic schemas for request validation and response serialization.

Schemas:
- LLMConfigBase: Base fields shared across create/update
- LLMConfigCreate: Fields required for creating new config
- LLMConfigUpdate: Fields that can be updated (all optional)
- LLMConfigResponse: Full response including computed fields
- LLMTestRequest: Schema for testing LLM before saving
- LLMTestResponse: Response from test operation
- TokenUsageResponse: Real-time token usage information
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


class TestStatus(str, Enum):
    """Test execution status."""
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


class HealthStatus(str, Enum):
    """Health check status."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    DOWN = "down"
    PENDING = "pending"


class LLMConfigBase(BaseModel):
    """
    Base schema with common LLM configuration fields.
    
    Attributes:
        name: User-friendly name for this configuration
        model_name: Actual model identifier
        provider: LLM provider type
        api_endpoint: Base URL for API calls
        api_key: Optional API key (will be encrypted)
        model_parameters: Model-specific parameters
        token_limit_daily: Daily token usage limit (0 = unlimited)
        token_limit_monthly: Monthly token usage limit (0 = unlimited)
        is_active: Whether configuration is active
        is_default: Whether this is the default config
        fallback_config_id: ID of fallback configuration
        cache_enabled: Enable response caching
        cache_ttl_seconds: Cache time-to-live
        cost_per_1k_tokens: Cost per 1000 tokens
    """
    
    name: str = Field(..., min_length=1, max_length=255, description="Configuration name")
    model_name: str = Field(..., min_length=1, max_length=255, description="Model identifier")
    provider: LLMProvider = Field(..., description="LLM provider")
    api_endpoint: str = Field(..., min_length=1, max_length=500, description="API endpoint URL")
    api_key: Optional[str] = Field(None, description="API key (encrypted in storage)")
    model_parameters: Dict[str, Any] = Field(
        default={
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        },
        description="Model-specific parameters"
    )
    token_limit_daily: int = Field(default=0, ge=0, description="Daily token limit (0 = unlimited)")
    token_limit_monthly: int = Field(default=0, ge=0, description="Monthly token limit (0 = unlimited)")
    is_active: bool = Field(default=True, description="Configuration active status")
    is_default: bool = Field(default=False, description="Default configuration flag")
    fallback_config_id: Optional[int] = Field(None, description="Fallback configuration ID")
    cache_enabled: bool = Field(default=True, description="Enable response caching")
    cache_ttl_seconds: int = Field(default=3600, ge=0, description="Cache TTL in seconds")
    cost_per_1k_tokens: float = Field(default=0.0, ge=0.0, description="Cost per 1K tokens (USD)")

    @validator('model_parameters')
    def validate_model_parameters(cls, v):
        """Validate model parameters contain required fields."""
        required_fields = ['temperature', 'max_tokens']
        for field in required_fields:
            if field not in v:
                raise ValueError(f"model_parameters must contain '{field}'")
        return v


class LLMConfigCreate(LLMConfigBase):
    """
    Schema for creating a new LLM configuration.
    Inherits all fields from LLMConfigBase with project_id added.
    """
    
    project_id: int = Field(..., gt=0, description="Project ID this config belongs to")


class LLMConfigUpdate(BaseModel):
    """
    Schema for updating an existing LLM configuration.
    All fields are optional.
    """
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    model_name: Optional[str] = Field(None, min_length=1, max_length=255)
    provider: Optional[LLMProvider] = None
    api_endpoint: Optional[str] = Field(None, min_length=1, max_length=500)
    api_key: Optional[str] = None
    model_parameters: Optional[Dict[str, Any]] = None
    token_limit_daily: Optional[int] = Field(None, ge=0)
    token_limit_monthly: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None
    fallback_config_id: Optional[int] = None
    cache_enabled: Optional[bool] = None
    cache_ttl_seconds: Optional[int] = Field(None, ge=0)
    cost_per_1k_tokens: Optional[float] = Field(None, ge=0.0)


class LLMConfigResponse(LLMConfigBase):
    """
    Schema for LLM configuration responses.
    Includes all fields plus computed/status fields.
    """
    
    id: int
    project_id: int
    token_usage_today: int
    token_usage_month: int
    last_reset_daily: datetime
    last_reset_monthly: datetime
    last_tested_at: Optional[datetime]
    test_status: TestStatus
    test_response_time_ms: Optional[int]
    health_status: HealthStatus
    last_health_check: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    # Computed fields
    daily_usage_percentage: Optional[float] = None
    monthly_usage_percentage: Optional[float] = None
    estimated_cost_today: Optional[float] = None
    estimated_cost_month: Optional[float] = None

    class Config:
        from_attributes = True

    @validator('daily_usage_percentage', always=True)
    def compute_daily_usage_percentage(cls, v, values):
        """Calculate percentage of daily limit used."""
        if values.get('token_limit_daily', 0) > 0:
            usage = values.get('token_usage_today', 0)
            limit = values['token_limit_daily']
            return round((usage / limit) * 100, 2)
        return None

    @validator('monthly_usage_percentage', always=True)
    def compute_monthly_usage_percentage(cls, v, values):
        """Calculate percentage of monthly limit used."""
        if values.get('token_limit_monthly', 0) > 0:
            usage = values.get('token_usage_month', 0)
            limit = values['token_limit_monthly']
            return round((usage / limit) * 100, 2)
        return None

    @validator('estimated_cost_today', always=True)
    def compute_estimated_cost_today(cls, v, values):
        """Calculate estimated cost for today's usage."""
        usage = values.get('token_usage_today', 0)
        cost_per_1k = values.get('cost_per_1k_tokens', 0.0)
        return round((usage / 1000) * cost_per_1k, 4)

    @validator('estimated_cost_month', always=True)
    def compute_estimated_cost_month(cls, v, values):
        """Calculate estimated cost for this month's usage."""
        usage = values.get('token_usage_month', 0)
        cost_per_1k = values.get('cost_per_1k_tokens', 0.0)
        return round((usage / 1000) * cost_per_1k, 4)


class LLMTestRequest(BaseModel):
    """
    Schema for testing an LLM configuration.
    
    Attributes:
        prompt: Test prompt to send to the model
        stream: Whether to stream the response
    """
    
    prompt: str = Field(
        default="Hello! Please respond with a brief introduction to software testing.",
        description="Test prompt"
    )
    stream: bool = Field(default=False, description="Stream response")


class LLMTestResponse(BaseModel):
    """
    Schema for LLM test response.
    
    Attributes:
        success: Whether test was successful
        response: Model response text
        tokens_used: Number of tokens consumed
        response_time_ms: Response time in milliseconds
        error: Error message if test failed
    """
    
    success: bool
    response: Optional[str] = None
    tokens_used: Optional[int] = None
    response_time_ms: Optional[int] = None
    error: Optional[str] = None
    model_info: Optional[Dict[str, Any]] = None


class TokenUsageResponse(BaseModel):
    """
    Schema for real-time token usage information.
    
    Used by WebSocket for broadcasting usage updates.
    """
    
    config_id: int
    project_id: int
    token_usage_today: int
    token_usage_month: int
    token_limit_daily: int
    token_limit_monthly: int
    daily_usage_percentage: Optional[float]
    monthly_usage_percentage: Optional[float]
    estimated_cost_today: float
    estimated_cost_month: float
    timestamp: datetime


class HealthCheckResponse(BaseModel):
    """
    Schema for health check response.
    
    Attributes:
        config_id: Configuration ID
        status: Health status
        response_time_ms: Response time
        last_check: Timestamp of check
        message: Status message
    """
    
    config_id: int
    status: HealthStatus
    response_time_ms: Optional[int]
    last_check: datetime
    message: str