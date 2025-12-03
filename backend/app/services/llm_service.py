"""
LLM Service
-----------
Service layer for LLM operations including testing, health checks, and API calls.

Features:
- Multi-provider support (Ollama, OpenAI, Anthropic, Google)
- Model testing before saving configuration
- Automatic health monitoring
- Token counting and usage tracking
- Response caching
- Fallback chain support
- Cost estimation

This service abstracts away provider-specific implementation details.
"""

import aiohttp
import time
import asyncio
from typing import Optional, Dict, Any, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.llm_config import LLMConfig
from app.schemas.llm_config import (
    LLMTestRequest, 
    LLMTestResponse, 
    HealthStatus,
    LLMProvider
)
from app.services.cache_service import CacheService


class LLMService:
    """
    Service for interacting with various LLM providers.
    
    Supports:
    - Ollama (local models)
    - OpenAI (GPT models)
    - Anthropic (Claude models)
    - Google (Gemini models)
    """
    
    def __init__(self, db: Session, cache_service: Optional[CacheService] = None):
        """
        Initialize LLM service.
        
        Args:
            db: Database session
            cache_service: Optional cache service for response caching
        """
        self.db = db
        self.cache_service = cache_service or CacheService()
    
    async def test_model(
        self, 
        config: LLMConfig, 
        test_request: LLMTestRequest
    ) -> LLMTestResponse:
        """
        Test an LLM configuration with a sample prompt.
        
        Args:
            config: LLM configuration to test
            test_request: Test request with prompt
            
        Returns:
            Test response with success status, response text, and metrics
        """
        start_time = time.time()
        
        try:
            # Route to appropriate provider
            if config.provider == LLMProvider.OLLAMA:
                response_text, tokens = await self._test_ollama(config, test_request.prompt)
            elif config.provider == LLMProvider.OPENAI:
                response_text, tokens = await self._test_openai(config, test_request.prompt)
            elif config.provider == LLMProvider.ANTHROPIC:
                response_text, tokens = await self._test_anthropic(config, test_request.prompt)
            elif config.provider == LLMProvider.GOOGLE:
                response_text, tokens = await self._test_google(config, test_request.prompt)
            else:
                raise ValueError(f"Unsupported provider: {config.provider}")
            
            response_time_ms = int((time.time() - start_time) * 1000)
            
            # Update config test status
            config.last_tested_at = func.now()
            config.test_status = "success"
            config.test_response_time_ms = response_time_ms
            config.health_status = "healthy"
            config.last_health_check = func.now()
            self.db.commit()
            
            return LLMTestResponse(
                success=True,
                response=response_text,
                tokens_used=tokens,
                response_time_ms=response_time_ms,
                model_info={
                    "model": config.model_name,
                    "provider": config.provider,
                    "parameters": config.model_parameters
                }
            )
        
        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            
            # Update config test status
            config.test_status = "failed"
            config.test_response_time_ms = response_time_ms
            config.health_status = "down"
            config.last_health_check = func.now()
            self.db.commit()
            
            return LLMTestResponse(
                success=False,
                error=str(e),
                response_time_ms=response_time_ms
            )
    
    async def _test_ollama(self, config: LLMConfig, prompt: str) -> Tuple[str, int]:
        """
        Test Ollama model.
        
        Args:
            config: LLM configuration
            prompt: Test prompt
            
        Returns:
            Tuple of (response_text, tokens_used)
        """
        async with aiohttp.ClientSession() as session:
            url = f"{config.api_endpoint}/api/generate"
            payload = {
                "model": config.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": config.model_parameters.get("temperature", 0.7),
                    "num_predict": config.model_parameters.get("max_tokens", 2048),
                    "top_p": config.model_parameters.get("top_p", 0.9)
                }
            }
            
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status != 200:
                    raise Exception(f"Ollama API error: {response.status}")
                
                data = await response.json()
                response_text = data.get("response", "")
                
                # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
                tokens = len(prompt + response_text) // 4
                
                return response_text, tokens
    
    async def _test_openai(self, config: LLMConfig, prompt: str) -> Tuple[str, int]:
        """
        Test OpenAI model.
        
        Args:
            config: LLM configuration
            prompt: Test prompt
            
        Returns:
            Tuple of (response_text, tokens_used)
        """
        if not config.api_key:
            raise ValueError("OpenAI requires an API key")
        
        async with aiohttp.ClientSession() as session:
            url = f"{config.api_endpoint}/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": config.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": config.model_parameters.get("temperature", 0.7),
                "max_tokens": config.model_parameters.get("max_tokens", 2048),
                "top_p": config.model_parameters.get("top_p", 0.9)
            }
            
            async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"OpenAI API error: {response.status} - {error_text}")
                
                data = await response.json()
                response_text = data["choices"][0]["message"]["content"]
                tokens = data["usage"]["total_tokens"]
                
                return response_text, tokens
    
    async def _test_anthropic(self, config: LLMConfig, prompt: str) -> Tuple[str, int]:
        """
        Test Anthropic (Claude) model.
        
        Args:
            config: LLM configuration
            prompt: Test prompt
            
        Returns:
            Tuple of (response_text, tokens_used)
        """
        if not config.api_key:
            raise ValueError("Anthropic requires an API key")
        
        async with aiohttp.ClientSession() as session:
            url = f"{config.api_endpoint}/v1/messages"
            headers = {
                "x-api-key": config.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            payload = {
                "model": config.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": config.model_parameters.get("temperature", 0.7),
                "max_tokens": config.model_parameters.get("max_tokens", 2048)
            }
            
            async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Anthropic API error: {response.status} - {error_text}")
                
                data = await response.json()
                response_text = data["content"][0]["text"]
                tokens = data["usage"]["input_tokens"] + data["usage"]["output_tokens"]
                
                return response_text, tokens
    
    async def _test_google(self, config: LLMConfig, prompt: str) -> Tuple[str, int]:
        """
        Test Google (Gemini) model.
        
        Args:
            config: LLM configuration
            prompt: Test prompt
            
        Returns:
            Tuple of (response_text, tokens_used)
        """
        if not config.api_key:
            raise ValueError("Google requires an API key")
        
        async with aiohttp.ClientSession() as session:
            url = f"{config.api_endpoint}/v1/models/{config.model_name}:generateContent?key={config.api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": config.model_parameters.get("temperature", 0.7),
                    "maxOutputTokens": config.model_parameters.get("max_tokens", 2048),
                    "topP": config.model_parameters.get("top_p", 0.9)
                }
            }
            
            async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=60)) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"Google API error: {response.status} - {error_text}")
                
                data = await response.json()
                response_text = data["candidates"][0]["content"]["parts"][0]["text"]
                
                # Google doesn't return token count in all responses, estimate
                tokens = len(prompt + response_text) // 4
                
                return response_text, tokens
    
    async def check_health(self, config: LLMConfig) -> Dict[str, Any]:
        """
        Perform health check on an LLM configuration.
        
        Args:
            config: LLM configuration to check
            
        Returns:
            Dictionary with health status and metrics
        """
        test_request = LLMTestRequest(prompt="Respond with 'OK' if you receive this.")
        result = await self.test_model(config, test_request)
        
        return {
            "config_id": config.id,
            "status": config.health_status,
            "response_time_ms": result.response_time_ms,
            "last_check": config.last_health_check,
            "message": "Health check completed successfully" if result.success else result.error
        }
    
    async def check_and_reset_token_limits(self, config: LLMConfig):
        """
        Check if token usage counters need to be reset based on time periods.
        
        Args:
            config: LLM configuration to check
        """
        now = datetime.now()
        
        # Reset daily counter if it's a new day
        if config.last_reset_daily.date() < now.date():
            config.reset_daily_usage()
        
        # Reset monthly counter if it's a new month
        if (config.last_reset_monthly.year < now.year or 
            config.last_reset_monthly.month < now.month):
            config.reset_monthly_usage()
        
        self.db.commit()
    
    def add_token_usage(self, config: LLMConfig, tokens: int):
        """
        Add token usage to configuration counters.
        
        Args:
            config: LLM configuration
            tokens: Number of tokens to add
        """
        config.add_token_usage(tokens)
        self.db.commit()
    
    async def call_with_fallback(
        self, 
        config_id: int, 
        prompt: str,
        max_retries: int = 3
    ) -> Tuple[str, int, int]:
        """
        Call LLM with automatic fallback to backup config if primary fails.
        
        Args:
            config_id: Primary configuration ID
            prompt: Prompt to send
            max_retries: Maximum retry attempts
            
        Returns:
            Tuple of (response_text, tokens_used, config_id_used)
        """
        config = self.db.query(LLMConfig).filter(LLMConfig.id == config_id).first()
        if not config:
            raise ValueError(f"Configuration {config_id} not found")
        
        # Check token limits
        await self.check_and_reset_token_limits(config)
        
        # Try primary config
        for attempt in range(max_retries):
            try:
                test_request = LLMTestRequest(prompt=prompt)
                result = await self.test_model(config, test_request)
                
                if result.success:
                    self.add_token_usage(config, result.tokens_used)
                    return result.response, result.tokens_used, config.id
                
            except Exception as e:
                if attempt == max_retries - 1:
                    break
                await asyncio.sleep(1)  # Wait before retry
        
        # If primary fails and fallback exists, try fallback
        if config.fallback_config_id:
            fallback_config = self.db.query(LLMConfig).filter(
                LLMConfig.id == config.fallback_config_id
            ).first()
            
            if fallback_config:
                test_request = LLMTestRequest(prompt=prompt)
                result = await self.test_model(fallback_config, test_request)
                
                if result.success:
                    self.add_token_usage(fallback_config, result.tokens_used)
                    return result.response, result.tokens_used, fallback_config.id
        
        raise Exception("All LLM configurations failed")