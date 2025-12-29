"""
LLM Configuration Model
-----------------------
SQLAlchemy model for managing Large Language Model configurations per project.

Features:
- Multi-provider support (Ollama, OpenAI, Anthropic, Google Gemini)
- Token usage tracking (daily/monthly limits)
- Health monitoring with automatic checks
- Fallback chain for reliability
- Response caching for performance
- Cost estimation based on provider pricing

Each project can have multiple LLM configurations with one marked as default.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class LLMConfig(Base):
    """
    LLM Configuration entity for project-specific model management.
    
    Attributes:
        id: Primary key
        project_id: Foreign key to projects table
        name: User-friendly name for this configuration
        model_name: Actual model identifier (e.g., "llama3.1:8b", "gpt-4")
        provider: LLM provider ("ollama", "openai", "anthropic", "google")
        api_endpoint: Base URL for API calls
        api_key: Encrypted API key (nullable for local models)
        model_parameters: JSON object with temperature, max_tokens, top_p, etc.
        token_limit_daily: Maximum tokens allowed per day (0 = unlimited)
        token_limit_monthly: Maximum tokens allowed per month (0 = unlimited)
        token_usage_today: Current day's token usage
        token_usage_month: Current month's token usage
        last_reset_daily: Last date when daily counter was reset
        last_reset_monthly: Last date when monthly counter was reset
        is_active: Whether this config is currently active
        is_default: Whether this is the default config for the project
        last_tested_at: Timestamp of last successful test
        test_status: Status of last test ("success", "failed", "pending")
        test_response_time_ms: Response time from last test
        health_status: Current health status ("healthy", "degraded", "down")
        last_health_check: Timestamp of last health check
        fallback_config_id: ID of fallback config if this one fails
        cache_enabled: Whether to cache responses
        cache_ttl_seconds: Time-to-live for cached responses
        cost_per_1k_tokens: Cost per 1000 tokens for estimation
    """
    
    __tablename__ = "llm_configs"

    # Primary fields
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    
    # Model configuration
    model_name = Column(String(255), nullable=False)
    provider = Column(String(50), nullable=False, index=True)  # ollama, openai, anthropic, google
    api_endpoint = Column(String(500), nullable=False)
    api_key = Column(Text, nullable=True)  # Encrypted, nullable for local models
    model_parameters = Column(JSON, nullable=False, default={
        "temperature": 0.7,
        "max_tokens": 2048,
        "top_p": 0.9,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    })
    
    # Token tracking
    token_limit_daily = Column(Integer, default=0)  # 0 = unlimited
    token_limit_monthly = Column(Integer, default=0)  # 0 = unlimited
    token_usage_today = Column(Integer, default=0)
    token_usage_month = Column(Integer, default=0)
    last_reset_daily = Column(DateTime(timezone=True), server_default=func.now())
    last_reset_monthly = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status flags
    is_active = Column(Boolean, default=True, index=True)
    is_default = Column(Boolean, default=False, index=True)
    
    # Testing and health
    last_tested_at = Column(DateTime(timezone=True), nullable=True)
    test_status = Column(String(20), default="pending")  # success, failed, pending
    test_response_time_ms = Column(Integer, nullable=True)
    health_status = Column(String(20), default="pending", index=True)  # healthy, degraded, down, pending
    last_health_check = Column(DateTime(timezone=True), nullable=True)
    
    # Reliability features
    fallback_config_id = Column(Integer, ForeignKey("llm_configs.id", ondelete="SET NULL"), nullable=True)
    
    # Caching configuration
    cache_enabled = Column(Boolean, default=True)
    cache_ttl_seconds = Column(Integer, default=3600)  # 1 hour default
    
    # Cost tracking
    cost_per_1k_tokens = Column(Float, default=0.0)  # For cost estimation
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    from sqlalchemy.orm import backref
    project = relationship("Project", backref=backref("llm_configs", lazy="selectin", cascade="all, delete-orphan"))
    fallback_config = relationship("LLMConfig", remote_side=[id], uselist=False)
    
    def __repr__(self):
        """String representation for debugging."""
        return f"<LLMConfig(id={self.id}, name='{self.name}', model='{self.model_name}', provider='{self.provider}')>"
    
    def reset_daily_usage(self):
        """Reset daily token usage counter."""
        self.token_usage_today = 0
        self.last_reset_daily = func.now()
    
    def reset_monthly_usage(self):
        """Reset monthly token usage counter."""
        self.token_usage_month = 0
        self.last_reset_monthly = func.now()
    
    def is_within_limits(self, tokens_to_use: int) -> bool:
        """
        Check if using specified tokens would exceed limits.
        
        Args:
            tokens_to_use: Number of tokens about to be consumed
            
        Returns:
            True if within limits, False otherwise
        """
        if self.token_limit_daily > 0:
            if self.token_usage_today + tokens_to_use > self.token_limit_daily:
                return False
        
        if self.token_limit_monthly > 0:
            if self.token_usage_month + tokens_to_use > self.token_limit_monthly:
                return False
        
        return True
    
    def add_token_usage(self, tokens_used: int):
        """
        Add token usage to counters.
        
        Args:
            tokens_used: Number of tokens consumed
        """
        self.token_usage_today += tokens_used
        self.token_usage_month += tokens_used
    
    def estimate_cost(self, tokens: int) -> float:
        """
        Estimate cost for given number of tokens.
        
        Args:
            tokens: Number of tokens
            
        Returns:
            Estimated cost in USD
        """
        return (tokens / 1000) * self.cost_per_1k_tokens