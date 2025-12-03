"""
LLM Configuration Service
-------------------------
Business logic for LLM configuration CRUD operations.

Features:
- Create, read, update, delete LLM configurations
- Ensure only one default config per project
- Validate configuration before saving
- Handle encryption of API keys
- Manage relationships with projects

This service layer separates business logic from API endpoints.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from cryptography.fernet import Fernet
import os

from app.models.llm_config import LLMConfig
from app.models.project import Project
from app.schemas.llm_config import LLMConfigCreate, LLMConfigUpdate, LLMConfigResponse


class LLMConfigService:
    """
    Service for managing LLM configurations.
    
    Handles:
    - CRUD operations
    - API key encryption/decryption
    - Default config management
    - Validation
    """
    
    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        
        # Initialize encryption key (in production, use environment variable)
        encryption_key = os.getenv("ENCRYPTION_KEY")
        if not encryption_key:
            # Generate a key for development (DON'T do this in production)
            encryption_key = Fernet.generate_key()
        
        self.cipher = Fernet(encryption_key if isinstance(encryption_key, bytes) else encryption_key.encode())
    
    def _encrypt_api_key(self, api_key: Optional[str]) -> Optional[str]:
        """
        Encrypt API key before storing in database.
        
        Args:
            api_key: Plain text API key
            
        Returns:
            Encrypted API key or None
        """
        if not api_key:
            return None
        
        return self.cipher.encrypt(api_key.encode()).decode()
    
    def _decrypt_api_key(self, encrypted_key: Optional[str]) -> Optional[str]:
        """
        Decrypt API key from database.
        
        Args:
            encrypted_key: Encrypted API key
            
        Returns:
            Plain text API key or None
        """
        if not encrypted_key:
            return None
        
        return self.cipher.decrypt(encrypted_key.encode()).decode()
    
    def create_config(self, config_data: LLMConfigCreate) -> LLMConfig:
        """
        Create a new LLM configuration.
        
        Args:
            config_data: Configuration data from request
            
        Returns:
            Created LLM configuration
            
        Raises:
            ValueError: If project doesn't exist
        """
        # Verify project exists
        project = self.db.query(Project).filter(Project.id == config_data.project_id).first()
        if not project:
            raise ValueError(f"Project {config_data.project_id} not found")
        
        # If this is set as default, unset other defaults for this project
        if config_data.is_default:
            self._unset_default_configs(config_data.project_id)
        
        # Encrypt API key if provided
        encrypted_key = self._encrypt_api_key(config_data.api_key)
        
        # Create config
        db_config = LLMConfig(
            **config_data.dict(exclude={"api_key"}),
            api_key=encrypted_key
        )
        
        self.db.add(db_config)
        self.db.commit()
        self.db.refresh(db_config)
        
        return db_config
    
    def get_config(self, config_id: int) -> Optional[LLMConfig]:
        """
        Get LLM configuration by ID.
        
        Args:
            config_id: Configuration ID
            
        Returns:
            LLM configuration or None
        """
        return self.db.query(LLMConfig).filter(LLMConfig.id == config_id).first()
    
    def get_project_configs(
        self, 
        project_id: int, 
        include_inactive: bool = False
    ) -> List[LLMConfig]:
        """
        Get all LLM configurations for a project.
        
        Args:
            project_id: Project ID
            include_inactive: Whether to include inactive configs
            
        Returns:
            List of LLM configurations
        """
        query = self.db.query(LLMConfig).filter(LLMConfig.project_id == project_id)
        
        if not include_inactive:
            query = query.filter(LLMConfig.is_active == True)
        
        return query.order_by(LLMConfig.created_at.desc()).all()
    
    def get_default_config(self, project_id: int) -> Optional[LLMConfig]:
        """
        Get the default LLM configuration for a project.
        
        Args:
            project_id: Project ID
            
        Returns:
            Default LLM configuration or None
        """
        return self.db.query(LLMConfig).filter(
            and_(
                LLMConfig.project_id == project_id,
                LLMConfig.is_default == True,
                LLMConfig.is_active == True
            )
        ).first()
    
    def update_config(self, config_id: int, config_data: LLMConfigUpdate) -> Optional[LLMConfig]:
        """
        Update an existing LLM configuration.
        
        Args:
            config_id: Configuration ID
            config_data: Update data
            
        Returns:
            Updated configuration or None
        """
        db_config = self.get_config(config_id)
        if not db_config:
            return None
        
        # If setting as default, unset other defaults
        if config_data.is_default and config_data.is_default != db_config.is_default:
            self._unset_default_configs(db_config.project_id, exclude_id=config_id)
        
        # Update fields
        update_data = config_data.dict(exclude_unset=True, exclude={"api_key"})
        for field, value in update_data.items():
            setattr(db_config, field, value)
        
        # Handle API key separately if provided
        if config_data.api_key is not None:
            db_config.api_key = self._encrypt_api_key(config_data.api_key)
        
        self.db.commit()
        self.db.refresh(db_config)
        
        return db_config
    
    def delete_config(self, config_id: int) -> bool:
        """
        Delete an LLM configuration.
        
        Args:
            config_id: Configuration ID
            
        Returns:
            True if deleted, False if not found
        """
        db_config = self.get_config(config_id)
        if not db_config:
            return False
        
        # If this was the default, we might want to set another as default
        # For now, just delete
        self.db.delete(db_config)
        self.db.commit()
        
        return True
    
    def _unset_default_configs(self, project_id: int, exclude_id: Optional[int] = None):
        """
        Unset default flag for all configs in a project.
        
        Args:
            project_id: Project ID
            exclude_id: Config ID to exclude from update
        """
        query = self.db.query(LLMConfig).filter(
            and_(
                LLMConfig.project_id == project_id,
                LLMConfig.is_default == True
            )
        )
        
        if exclude_id:
            query = query.filter(LLMConfig.id != exclude_id)
        
        configs = query.all()
        for config in configs:
            config.is_default = False
        
        self.db.commit()
    
    def get_usage_summary(self, project_id: int) -> dict:
        """
        Get token usage summary for all configs in a project.
        
        Args:
            project_id: Project ID
            
        Returns:
            Dictionary with usage statistics
        """
        configs = self.get_project_configs(project_id, include_inactive=False)
        
        total_tokens_today = sum(c.token_usage_today for c in configs)
        total_tokens_month = sum(c.token_usage_month for c in configs)
        total_cost_today = sum(c.estimate_cost(c.token_usage_today) for c in configs)
        total_cost_month = sum(c.estimate_cost(c.token_usage_month) for c in configs)
        
        return {
            "project_id": project_id,
            "total_configs": len(configs),
            "active_configs": len([c for c in configs if c.is_active]),
            "total_tokens_today": total_tokens_today,
            "total_tokens_month": total_tokens_month,
            "estimated_cost_today": round(total_cost_today, 4),
            "estimated_cost_month": round(total_cost_month, 4)
        }