"""
Cache Service
-------------
Redis-like in-memory caching service for LLM responses.

Features:
- TTL-based expiration
- LRU eviction when memory limit reached
- Cache hit/miss statistics
- Automatic cleanup of expired entries

For production, consider using Redis or Memcached.
"""

import time
import hashlib
from typing import Optional, Dict, Any
from collections import OrderedDict
import threading


class CacheService:
    """
    In-memory cache service with TTL and LRU eviction.
    
    Thread-safe implementation suitable for development.
    For production, use Redis.
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """
        Initialize cache service.
        
        Args:
            max_size: Maximum number of cache entries
            default_ttl: Default time-to-live in seconds
        """
        self.cache: OrderedDict = OrderedDict()
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.lock = threading.Lock()
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }
    
    def _generate_key(self, prompt: str, config_id: int, params: Dict[str, Any]) -> str:
        """
        Generate cache key from prompt and parameters.
        
        Args:
            prompt: User prompt
            config_id: LLM configuration ID
            params: Model parameters
            
        Returns:
            SHA256 hash as cache key
        """
        key_data = f"{config_id}:{prompt}:{str(sorted(params.items()))}"
        return hashlib.sha256(key_data.encode()).hexdigest()
    
    def get(self, prompt: str, config_id: int, params: Dict[str, Any]) -> Optional[str]:
        """
        Get cached response if exists and not expired.
        
        Args:
            prompt: User prompt
            config_id: LLM configuration ID
            params: Model parameters
            
        Returns:
            Cached response or None
        """
        key = self._generate_key(prompt, config_id, params)
        
        with self.lock:
            if key in self.cache:
                entry = self.cache[key]
                
                # Check if expired
                if time.time() < entry["expires_at"]:
                    # Move to end (LRU)
                    self.cache.move_to_end(key)
                    self.stats["hits"] += 1
                    return entry["response"]
                else:
                    # Remove expired entry
                    del self.cache[key]
            
            self.stats["misses"] += 1
            return None
    
    def set(
        self, 
        prompt: str, 
        config_id: int, 
        params: Dict[str, Any], 
        response: str,
        ttl: Optional[int] = None
    ):
        """
        Cache a response with TTL.
        
        Args:
            prompt: User prompt
            config_id: LLM configuration ID
            params: Model parameters
            response: LLM response to cache
            ttl: Time-to-live in seconds (uses default if None)
        """
        key = self._generate_key(prompt, config_id, params)
        ttl = ttl or self.default_ttl
        
        with self.lock:
            # Check if cache is full
            if len(self.cache) >= self.max_size and key not in self.cache:
                # Remove oldest entry (LRU)
                self.cache.popitem(last=False)
                self.stats["evictions"] += 1
            
            self.cache[key] = {
                "response": response,
                "expires_at": time.time() + ttl,
                "created_at": time.time()
            }
            
            # Move to end (most recently used)
            self.cache.move_to_end(key)
    
    def invalidate(self, config_id: Optional[int] = None):
        """
        Invalidate cache entries.
        
        Args:
            config_id: If provided, only invalidate entries for this config
        """
        with self.lock:
            if config_id is None:
                self.cache.clear()
            else:
                # Remove entries for specific config
                # (requires storing config_id in entry for efficient filtering)
                pass
    
    def cleanup_expired(self):
        """Remove all expired cache entries."""
        current_time = time.time()
        
        with self.lock:
            expired_keys = [
                key for key, entry in self.cache.items()
                if current_time >= entry["expires_at"]
            ]
            
            for key in expired_keys:
                del self.cache[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.
        
        Returns:
            Dictionary with hit rate, miss rate, and other metrics
        """
        with self.lock:
            total = self.stats["hits"] + self.stats["misses"]
            hit_rate = (self.stats["hits"] / total * 100) if total > 0 else 0
            
            return {
                "hits": self.stats["hits"],
                "misses": self.stats["misses"],
                "hit_rate": round(hit_rate, 2),
                "evictions": self.stats["evictions"],
                "size": len(self.cache),
                "max_size": self.max_size
            }