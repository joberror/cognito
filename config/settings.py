"""
Configuration settings for the Media Management Bot.
This module handles all configuration loading and validation.
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class DatabaseSettings(BaseSettings):
    """MongoDB database configuration settings."""

    # MongoDB connection URI (contains all connection details)
    mongodb_uri: str = "mongodb+srv://your_mongodb_user:your_mongodb_password@your-online-mongodb-host/media_bot"

    class Config:
        env_prefix = ""


class RedisSettings(BaseSettings):
    """Redis configuration settings."""
    
    host: str = "localhost"
    port: int = 6379
    password: str = ""
    db: int = 0
    url: str = "redis://localhost:6379/0"
    
    class Config:
        env_prefix = "REDIS_"


class ElasticsearchSettings(BaseSettings):
    """Elasticsearch configuration settings."""
    
    host: str = "localhost"
    port: int = 9200
    index: str = "media_files"
    username: str = ""
    password: str = ""
    url: str = "http://localhost:9200"
    
    class Config:
        env_prefix = "ELASTICSEARCH_"


class MediaSettings(BaseSettings):
    """Media processing configuration settings."""
    
    storage_path: str = "./data/media"
    temp_storage_path: str = "./data/temp"
    max_file_size: int = 2147483648  # 2GB
    allowed_extensions: str = "mp4,mkv,avi,mov,wmv,flv,webm,m4v,3gp,mp3,flac,wav,aac,ogg,wma,m4a,jpg,jpeg,png,gif,bmp,webp,tiff,pdf,txt,doc,docx,zip,rar,7z"
    
    # FFmpeg
    ffmpeg_path: str = "/usr/bin/ffmpeg"
    ffprobe_path: str = "/usr/bin/ffprobe"
    
    # Image processing
    max_image_size: int = 10485760  # 10MB
    thumbnail_size: str = "300,300"
    image_quality: int = 85
    
    @validator('allowed_extensions')
    def parse_extensions(cls, v):
        return [ext.strip() for ext in v.split(',')]
    
    @validator('thumbnail_size')
    def parse_thumbnail_size(cls, v):
        return tuple(map(int, v.split(',')))
    
    class Config:
        env_prefix = "MEDIA_"


class BotSettings(BaseSettings):
    """Telegram bot configuration settings."""

    token: str
    username: str = ""
    name: str = "Media Management Bot"
    description: str = "A comprehensive media management bot for Telegram channels"

    # Super Admin configuration (bootstrap admin)
    super_admin_id: Optional[int] = None

    class Config:
        env_prefix = "BOT_"


class TelegramAPISettings(BaseSettings):
    """Telegram API configuration settings."""

    api_id: Optional[int] = None
    api_hash: Optional[str] = None

    class Config:
        env_prefix = "TELEGRAM_"


class ChannelSettings(BaseSettings):
    """Channel processing configuration settings."""

    # Global channel processing settings
    auto_index_new_files: bool = True
    index_interval_hours: int = 24
    duplicate_check_enabled: bool = True

    class Config:
        env_prefix = ""


class SearchSettings(BaseSettings):
    """Search configuration settings."""
    
    results_limit: int = 50
    fuzzy_threshold: float = 0.8
    cache_ttl: int = 3600  # 1 hour
    
    # Indexing
    auto_index_on_startup: bool = False
    index_batch_size: int = 100
    index_timeout_seconds: int = 300
    
    class Config:
        env_prefix = "SEARCH_"


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""
    
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "./logs/bot.log"
    max_size: int = 10485760  # 10MB
    backup_count: int = 5
    
    # Feature-specific logging
    media_processing: bool = True
    user_actions: bool = True
    admin_actions: bool = True
    search_queries: bool = True
    
    class Config:
        env_prefix = "LOG_"


class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    
    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 30
    rate_limit_window: int = 60  # seconds
    
    # User management
    max_users_per_channel: int = 10000
    user_timeout_minutes: int = 30
    ban_duration_hours: int = 24
    
    # Webhook
    enable_webhook: bool = False
    webhook_url: str = ""
    webhook_secret: str = ""
    
    class Config:
        env_prefix = ""


class MonitoringSettings(BaseSettings):
    """Monitoring and analytics configuration settings."""
    
    # Prometheus
    prometheus_enabled: bool = False
    prometheus_port: int = 8000
    
    # Sentry
    sentry_dsn: str = ""
    sentry_environment: str = "development"
    
    # Statistics
    stats_update_interval: int = 3600  # 1 hour
    keep_stats_days: int = 30
    
    class Config:
        env_prefix = ""


class ExternalServicesSettings(BaseSettings):
    """External services configuration settings."""
    
    # Support links
    support_link: str = ""
    group_link: str = ""
    help_link: str = ""
    donation_link: str = ""
    
    # API keys
    tmdb_api_key: str = ""
    omdb_api_key: str = ""
    
    class Config:
        env_prefix = ""


class DevelopmentSettings(BaseSettings):
    """Development configuration settings."""
    
    environment: str = "development"
    debug: bool = True
    
    # Testing
    test_database_url: str = "sqlite:///./data/test.db"
    test_redis_url: str = "redis://localhost:6379/1"
    
    # Development tools
    enable_debug_commands: bool = True
    mock_external_services: bool = False
    
    class Config:
        env_prefix = ""


class Settings:
    """Main settings class that combines all configuration sections."""
    
    def __init__(self):
        self.bot = BotSettings()
        self.telegram_api = TelegramAPISettings()
        self.database = DatabaseSettings()
        self.redis = RedisSettings()
        self.elasticsearch = ElasticsearchSettings()
        self.media = MediaSettings()
        self.channels = ChannelSettings()
        self.search = SearchSettings()
        self.logging = LoggingSettings()
        self.security = SecuritySettings()
        self.monitoring = MonitoringSettings()
        self.external = ExternalServicesSettings()
        self.development = DevelopmentSettings()
    
    def validate(self) -> List[str]:
        """Validate all settings and return list of errors."""
        errors = []
        
        if not self.bot.token or self.bot.token == "YOUR_TELEGRAM_BOT_TOKEN":
            errors.append("BOT_TOKEN is required and must be set to a valid token")
        
        if not self.bot.admin_user_ids:
            errors.append("ADMIN_USER_IDS should be configured for proper bot administration")
        
        # Validate paths exist or can be created
        import pathlib
        for path in [self.media.storage_path, self.media.temp_storage_path]:
            try:
                pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create directory {path}: {e}")
        
        return errors


# Global settings instance
settings = Settings()
