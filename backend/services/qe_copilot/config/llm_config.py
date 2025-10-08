# backend/services/qe_copilot/config/llm_config.py

from typing import Optional, Dict, Any
from enum import Enum
from langchain.chat_models.base import BaseChatModel
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
import os
import logging

logger = logging.getLogger(__name__)

class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"

class LLMConfig(BaseModel):
    """LLM Configuration Model"""
    provider: LLMProvider = Field(default=LLMProvider.OLLAMA)
    model_name: str = Field(default="llama2")
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=4000)
    timeout: int = Field(default=60)
    custom_params: Dict[str, Any] = Field(default_factory=dict)

class LLMFactory:
    """Factory class for creating LLM instances"""
    
    # Default Ollama models (free, open-source)
    OLLAMA_MODELS = {
        "default": "llama2",
        "coding": "codellama",
        "large": "llama2:13b",
        "small": "llama2:7b",
        "mistral": "mistral",
        "mixtral": "mixtral",
        "phi": "phi",
        "neural-chat": "neural-chat"
    }
    
    @staticmethod
    def create_llm(config: Optional[LLMConfig] = None) -> BaseChatModel:
        """
        Create LLM instance based on configuration.
        Falls back to Ollama if no config provided or if configured provider fails.
        """
        if config is None:
            # Default to Ollama with llama2
            logger.info("No LLM config provided. Using Ollama with llama2 as fallback.")
            return LLMFactory._create_ollama_fallback()
        
        try:
            if config.provider == LLMProvider.OPENAI:
                return LLMFactory._create_openai(config)
            elif config.provider == LLMProvider.ANTHROPIC:
                return LLMFactory._create_anthropic(config)
            elif config.provider == LLMProvider.GOOGLE:
                return LLMFactory._create_google(config)
            elif config.provider == LLMProvider.OLLAMA:
                return LLMFactory._create_ollama(config)
            elif config.provider == LLMProvider.HUGGINGFACE:
                return LLMFactory._create_huggingface(config)
            else:
                logger.warning(f"Unknown provider {config.provider}. Falling back to Ollama.")
                return LLMFactory._create_ollama_fallback()
                
        except Exception as e:
            logger.error(f"Failed to create LLM with provider {config.provider}: {str(e)}")
            logger.info("Falling back to Ollama...")
            return LLMFactory._create_ollama_fallback()
    
    @staticmethod
    def _create_ollama(config: LLMConfig) -> ChatOllama:
        """Create Ollama LLM instance"""
        base_url = config.base_url or "http://localhost:11434"
        model = config.model_name or "llama2"
        
        logger.info(f"Creating Ollama LLM with model: {model}")
        
        return ChatOllama(
            model=model,
            base_url=base_url,
            temperature=config.temperature,
            num_predict=config.max_tokens,
            timeout=config.timeout,
            **config.custom_params
        )
    
    @staticmethod
    def _create_ollama_fallback() -> ChatOllama:
        """Create fallback Ollama instance with default settings"""
        return ChatOllama(
            model="llama2",
            base_url="http://localhost:11434",
            temperature=0.7,
            num_predict=4000,
            timeout=60
        )
    
    @staticmethod
    def _create_openai(config: LLMConfig) -> ChatOpenAI:
        """Create OpenAI LLM instance"""
        if not config.api_key:
            raise ValueError("OpenAI API key is required")
        
        return ChatOpenAI(
            model_name=config.model_name or "gpt-3.5-turbo",
            openai_api_key=config.api_key,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            timeout=config.timeout,
            **config.custom_params
        )
    
    @staticmethod
    def _create_anthropic(config: LLMConfig) -> ChatAnthropic:
        """Create Anthropic Claude LLM instance"""
        if not config.api_key:
            raise ValueError("Anthropic API key is required")
        
        return ChatAnthropic(
            model=config.model_name or "claude-3-sonnet-20240229",
            anthropic_api_key=config.api_key,
            temperature=config.temperature,
            max_tokens_to_sample=config.max_tokens,
            timeout=config.timeout,
            **config.custom_params
        )
    
    @staticmethod
    def _create_google(config: LLMConfig) -> ChatGoogleGenerativeAI:
        """Create Google Gemini LLM instance"""
        if not config.api_key:
            raise ValueError("Google API key is required")
        
        return ChatGoogleGenerativeAI(
            model=config.model_name or "gemini-pro",
            google_api_key=config.api_key,
            temperature=config.temperature,
            max_output_tokens=config.max_tokens,
            timeout=config.timeout,
            **config.custom_params
        )
    
    @staticmethod
    def _create_huggingface(config: LLMConfig):
        """Create HuggingFace LLM instance"""
        from langchain_community.llms import HuggingFaceHub
        
        if not config.api_key:
            raise ValueError("HuggingFace API token is required")
        
        return HuggingFaceHub(
            repo_id=config.model_name or "google/flan-t5-xxl",
            huggingfacehub_api_token=config.api_key,
            model_kwargs={
                "temperature": config.temperature,
                "max_length": config.max_tokens
            },
            **config.custom_params
        )

class LLMManager:
    """Manages LLM instances and configurations for projects"""
    
    def __init__(self):
        self._llm_cache: Dict[str, BaseChatModel] = {}
        self._config_cache: Dict[str, LLMConfig] = {}
    
    def get_llm_for_project(self, project_id: str) -> BaseChatModel:
        """Get LLM instance for a specific project"""
        if project_id in self._llm_cache:
            return self._llm_cache[project_id]
        
        # Load config from database
        config = self._load_project_config(project_id)
        
        # Create LLM instance
        llm = LLMFactory.create_llm(config)
        
        # Cache for future use
        self._llm_cache[project_id] = llm
        if config:
            self._config_cache[project_id] = config
        
        return llm
    
    def update_project_config(self, project_id: str, config: LLMConfig):
        """Update LLM configuration for a project"""
        # Validate config by trying to create LLM
        llm = LLMFactory.create_llm(config)
        
        # Update caches
        self._llm_cache[project_id] = llm
        self._config_cache[project_id] = config
        
        # Save to database
        self._save_project_config(project_id, config)
    
    def test_configuration(self, config: LLMConfig) -> Dict[str, Any]:
        """Test if LLM configuration works"""
        try:
            llm = LLMFactory.create_llm(config)
            
            # Try a simple query
            response = llm.predict("Hello, please respond with 'Configuration working'")
            
            return {
                "success": True,
                "message": "Configuration is valid",
                "response": response
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Configuration failed: {str(e)}",
                "error": str(e)
            }
    
    def get_available_models(self, provider: LLMProvider) -> List[str]:
        """Get list of available models for a provider"""
        models = {
            LLMProvider.OLLAMA: list(LLMFactory.OLLAMA_MODELS.values()),
            LLMProvider.OPENAI: ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview"],
            LLMProvider.ANTHROPIC: ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
            LLMProvider.GOOGLE: ["gemini-pro", "gemini-pro-vision"],
            LLMProvider.HUGGINGFACE: ["google/flan-t5-xxl", "mistralai/Mixtral-8x7B-Instruct-v0.1"]
        }
        return models.get(provider, [])
    
    def _load_project_config(self, project_id: str) -> Optional[LLMConfig]:
        """Load LLM configuration from database"""
        # Implementation to load from database
        # For now, return None to use fallback
        return None
    
    def _save_project_config(self, project_id: str, config: LLMConfig):
        """Save LLM configuration to database"""
        # Implementation to save to database
        pass

# Example Ollama setup script
"""
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull recommended models for QECopilot
ollama pull llama2
ollama pull codellama
ollama pull mistral
ollama pull mixtral

# Start Ollama service
ollama serve
"""