"""
Unsplash API service for fetching random movie posters for welcome messages.
"""

import os
import logging
import asyncio
import aiohttp
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class UnsplashService:
    """Service for fetching random movie posters from Unsplash API."""
    
    def __init__(self):
        self.access_key = os.getenv('UNSPLASH_ACCESS_KEY')
        self.secret_key = os.getenv('UNSPLASH_SECRET_KEY')
        self.base_url = "https://api.unsplash.com"
        self.cache = {}  # Simple in-memory cache
        self.cache_duration = timedelta(hours=24)  # 24-hour cache as specified
        
        if not self.access_key:
            logger.warning("Unsplash access key not configured. Welcome messages will not have posters.")
    
    async def get_random_movie_poster(self) -> Optional[Dict[str, Any]]:
        """
        Get a random movie poster from Unsplash.
        Returns cached result if available and not expired.
        """
        try:
            # Check cache first
            cache_key = "random_movie_poster"
            if self._is_cached_valid(cache_key):
                logger.info("Using cached movie poster")
                return self.cache[cache_key]['data']
            
            # Fetch new poster if not cached or expired
            poster_data = await self._fetch_random_poster()
            
            if poster_data:
                # Cache the result
                self.cache[cache_key] = {
                    'data': poster_data,
                    'timestamp': datetime.utcnow()
                }
                logger.info("Fetched and cached new movie poster")
                return poster_data
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching movie poster: {e}")
            return None
    
    async def _fetch_random_poster(self) -> Optional[Dict[str, Any]]:
        """Fetch a random movie-related image from Unsplash."""
        if not self.access_key:
            return None
        
        try:
            # Movie-related search terms for better poster results
            search_terms = [
                "movie poster", "cinema", "film", "movie theater", 
                "hollywood", "movie reel", "film strip", "blockbuster",
                "movie night", "entertainment", "drama", "action movie"
            ]
            
            # Use a random search term for variety
            import random
            query = random.choice(search_terms)
            
            url = f"{self.base_url}/photos/random"
            params = {
                'client_id': self.access_key,
                'query': query,
                'orientation': 'portrait',  # Better for movie posters
                'content_filter': 'high',   # High quality images
                'count': 1
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Handle both single image and array response
                        if isinstance(data, list) and len(data) > 0:
                            image_data = data[0]
                        elif isinstance(data, dict):
                            image_data = data
                        else:
                            return None
                        
                        return {
                            'url': image_data['urls']['regular'],
                            'thumb_url': image_data['urls']['thumb'],
                            'description': image_data.get('alt_description', 'Movie poster'),
                            'photographer': image_data['user']['name'],
                            'photographer_url': image_data['user']['links']['html'],
                            'unsplash_url': image_data['links']['html']
                        }
                    else:
                        logger.error(f"Unsplash API error: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error fetching from Unsplash API: {e}")
            return None
    
    def _is_cached_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid (within 24 hours)."""
        if cache_key not in self.cache:
            return False
        
        cached_time = self.cache[cache_key]['timestamp']
        return datetime.utcnow() - cached_time < self.cache_duration
    
    def clear_cache(self):
        """Clear the poster cache (useful for testing or manual refresh)."""
        self.cache.clear()
        logger.info("Unsplash poster cache cleared")
    
    def get_cache_status(self) -> Dict[str, Any]:
        """Get cache status for debugging."""
        cache_key = "random_movie_poster"
        if cache_key in self.cache:
            cached_time = self.cache[cache_key]['timestamp']
            age = datetime.utcnow() - cached_time
            return {
                'cached': True,
                'age_hours': age.total_seconds() / 3600,
                'expires_in_hours': (self.cache_duration - age).total_seconds() / 3600,
                'valid': self._is_cached_valid(cache_key)
            }
        return {'cached': False}


# Global service instance
unsplash_service = UnsplashService()


# Convenience function
async def get_welcome_poster() -> Optional[Dict[str, Any]]:
    """Get a random movie poster for welcome messages."""
    return await unsplash_service.get_random_movie_poster()


# Fallback poster data if Unsplash is not available
FALLBACK_POSTER = {
    'url': 'https://images.unsplash.com/photo-1489599904472-af35ff2c7c3f?w=400',
    'thumb_url': 'https://images.unsplash.com/photo-1489599904472-af35ff2c7c3f?w=200',
    'description': 'Movie theater with red seats',
    'photographer': 'Unsplash',
    'photographer_url': 'https://unsplash.com',
    'unsplash_url': 'https://unsplash.com/photos/movie-theater'
}


async def get_welcome_poster_with_fallback() -> Dict[str, Any]:
    """Get welcome poster with fallback if API fails."""
    poster = await get_welcome_poster()
    return poster if poster else FALLBACK_POSTER
