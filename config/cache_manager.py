"""
Cache management system for the Media Management Bot.
Supports both Redis (when available) and in-memory caching (fallback).
"""

import os
import json
import logging
from typing import Optional, Any, Dict
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class InMemoryCache:
    """Simple in-memory cache implementation as Redis fallback."""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._max_size = 1000  # Limit memory usage
    
    def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        if key in self._cache:
            item = self._cache[key]
            # Check expiration
            if item['expires_at'] and datetime.utcnow() > item['expires_at']:
                del self._cache[key]
                return None
            return item['value']
        return None
    
    def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        """Set value in cache with optional expiration."""
        # Prevent memory overflow
        if len(self._cache) >= self._max_size:
            # Remove oldest entries
            oldest_keys = sorted(self._cache.keys(), 
                               key=lambda k: self._cache[k]['created_at'])[:100]
            for old_key in oldest_keys:
                del self._cache[old_key]
        
        expires_at = None
        if ex:
            expires_at = datetime.utcnow() + timedelta(seconds=ex)
        
        self._cache[key] = {
            'value': value,
            'created_at': datetime.utcnow(),
            'expires_at': expires_at
        }
        return True
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        return self.get(key) is not None
    
    def clear(self) -> bool:
        """Clear all cache."""
        self._cache.clear()
        return True
    
    def keys(self, pattern: str = "*") -> list:
        """Get keys matching pattern (simplified)."""
        if pattern == "*":
            return list(self._cache.keys())
        # Simple pattern matching
        return [k for k in self._cache.keys() if pattern.replace("*", "") in k]


class CacheManager:
    """Cache manager that works with Redis or falls back to in-memory cache."""
    
    def __init__(self):
        self.redis_client = None
        self.memory_cache = InMemoryCache()
        self.redis_enabled = os.getenv('REDIS_ENABLED', 'true').lower() == 'true'
        self.using_redis = False
        
        if self.redis_enabled:
            self._init_redis()
    
    def _init_redis(self):
        """Initialize Redis connection if available."""
        try:
            import redis
            
            redis_url = os.getenv('REDIS_URL')
            if redis_url:
                self.redis_client = redis.from_url(redis_url, decode_responses=True)
            else:
                self.redis_client = redis.Redis(
                    host=os.getenv('REDIS_HOST', 'localhost'),
                    port=int(os.getenv('REDIS_PORT', 6379)),
                    db=int(os.getenv('REDIS_DB', 0)),
                    password=os.getenv('REDIS_PASSWORD') or None,
                    decode_responses=True
                )
            
            # Test connection
            self.redis_client.ping()
            self.using_redis = True
            logger.info("Redis connection established")
            
        except ImportError:
            logger.warning("Redis package not installed, using in-memory cache")
            self.redis_enabled = False
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}, using in-memory cache")
            self.redis_client = None
    
    def get(self, key: str) -> Optional[str]:
        """Get value from cache."""
        try:
            if self.using_redis and self.redis_client:
                return self.redis_client.get(key)
            else:
                return self.memory_cache.get(key)
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None
    
    def set(self, key: str, value: str, ex: Optional[int] = None) -> bool:
        """Set value in cache with optional expiration (seconds)."""
        try:
            if self.using_redis and self.redis_client:
                return self.redis_client.set(key, value, ex=ex)
            else:
                return self.memory_cache.set(key, value, ex=ex)
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            if self.using_redis and self.redis_client:
                return bool(self.redis_client.delete(key))
            else:
                return self.memory_cache.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        try:
            if self.using_redis and self.redis_client:
                return bool(self.redis_client.exists(key))
            else:
                return self.memory_cache.exists(key)
        except Exception as e:
            logger.error(f"Cache exists error for key {key}: {e}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache."""
        try:
            if self.using_redis and self.redis_client:
                return bool(self.redis_client.flushdb())
            else:
                return self.memory_cache.clear()
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False
    
    def keys(self, pattern: str = "*") -> list:
        """Get keys matching pattern."""
        try:
            if self.using_redis and self.redis_client:
                return self.redis_client.keys(pattern)
            else:
                return self.memory_cache.keys(pattern)
        except Exception as e:
            logger.error(f"Cache keys error: {e}")
            return []
    
    def get_json(self, key: str) -> Optional[Dict]:
        """Get JSON value from cache."""
        value = self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON in cache key {key}")
        return None
    
    def set_json(self, key: str, value: Dict, ex: Optional[int] = None) -> bool:
        """Set JSON value in cache."""
        try:
            json_str = json.dumps(value)
            return self.set(key, json_str, ex=ex)
        except (TypeError, ValueError) as e:
            logger.error(f"JSON serialization error for key {key}: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get cache status information."""
        status = {
            'redis_enabled': self.redis_enabled,
            'using_redis': self.using_redis,
            'cache_type': 'Redis' if self.using_redis else 'In-Memory',
            'connected': True
        }
        
        try:
            if self.using_redis and self.redis_client:
                info = self.redis_client.info()
                status.update({
                    'redis_version': info.get('redis_version'),
                    'used_memory': info.get('used_memory_human'),
                    'connected_clients': info.get('connected_clients'),
                })
            else:
                status.update({
                    'memory_cache_size': len(self.memory_cache._cache),
                    'max_size': self.memory_cache._max_size
                })
        except Exception as e:
            status['connected'] = False
            status['error'] = str(e)
        
        return status


# Global cache manager instance
cache_manager = CacheManager()


# Convenience functions
def get_cache(key: str) -> Optional[str]:
    """Get value from cache."""
    return cache_manager.get(key)


def set_cache(key: str, value: str, ex: Optional[int] = None) -> bool:
    """Set value in cache."""
    return cache_manager.set(key, value, ex=ex)


def delete_cache(key: str) -> bool:
    """Delete key from cache."""
    return cache_manager.delete(key)


def get_cache_json(key: str) -> Optional[Dict]:
    """Get JSON value from cache."""
    return cache_manager.get_json(key)


def set_cache_json(key: str, value: Dict, ex: Optional[int] = None) -> bool:
    """Set JSON value in cache."""
    return cache_manager.set_json(key, value, ex=ex)


def clear_cache() -> bool:
    """Clear all cache."""
    return cache_manager.clear()


def get_cache_status() -> Dict[str, Any]:
    """Get cache status."""
    return cache_manager.get_status()
