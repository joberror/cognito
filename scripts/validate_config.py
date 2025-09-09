#!/usr/bin/env python3
"""
Configuration validation script for the Media Management Bot.
This script validates all environment variables and configuration settings.
"""

import os
import sys
import pathlib
from typing import List, Dict, Any
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config.settings import settings
except ImportError:
    print("Error: Could not import settings. Make sure config/settings.py exists.")
    sys.exit(1)


def validate_required_env_vars() -> List[str]:
    """Validate required environment variables."""
    errors = []
    
    required_vars = {
        'BOT_TOKEN': 'Telegram bot token from @BotFather',
        'TELEGRAM_API_ID': 'Telegram API ID from https://my.telegram.org/apps',
        'TELEGRAM_API_HASH': 'Telegram API Hash from https://my.telegram.org/apps',
        'SUPER_ADMIN_ID': 'Super admin user ID (bootstrap admin)',
    }

    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value or value in ['YOUR_TELEGRAM_BOT_TOKEN', 'your_bot_token', 'your_api_id', 'your_api_hash']:
            errors.append(f"❌ {var} is required: {description}")
        else:
            print(f"✅ {var} is configured")

    # Note about dynamic management
    print("ℹ️  Channels and admins are managed dynamically through bot commands")

    return errors


def validate_paths() -> List[str]:
    """Validate file paths and create directories if needed."""
    errors = []
    
    paths_to_check = [
        ('MEDIA_STORAGE_PATH', './data/media'),
        ('TEMP_STORAGE_PATH', './data/temp'),
        ('LOG_FILE_PATH', './logs/bot.log'),
    ]
    
    for env_var, default_path in paths_to_check:
        path = os.getenv(env_var, default_path)
        
        if env_var == 'LOG_FILE_PATH':
            # For log file, check the directory
            path = os.path.dirname(path)
        
        try:
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            print(f"✅ {env_var}: {path} (created/exists)")
        except Exception as e:
            errors.append(f"❌ Cannot create directory for {env_var} ({path}): {e}")
    
    return errors


def validate_database_config() -> List[str]:
    """Validate MongoDB database configuration."""
    errors = []

    print("🍃 Validating MongoDB configuration...")

    # Check MongoDB URI
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri:
        errors.append("❌ MONGODB_URI is required")
    elif mongodb_uri in ['mongodb+srv://your_mongodb_user:your_mongodb_password@your-online-mongodb-host/media_bot', 'your_mongodb_uri']:
        errors.append("❌ MONGODB_URI needs to be configured with your actual MongoDB connection string")
    else:
        print(f"✅ MONGODB_URI is configured")

        # Validate URI format
        if not (mongodb_uri.startswith('mongodb://') or mongodb_uri.startswith('mongodb+srv://')):
            errors.append("❌ MONGODB_URI must start with 'mongodb://' or 'mongodb+srv://'")

    # Test MongoDB connection
    if not errors:  # Only test if URI is configured
        try:
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from config.mongodb import test_mongodb_connection

            connection_test = test_mongodb_connection()
            if connection_test['connected']:
                print(f"✅ MongoDB connection successful")
                print(f"   Database: {connection_test['database_name']}")
                if 'server_version' in connection_test:
                    print(f"   Server version: {connection_test['server_version']}")
                if connection_test.get('collections'):
                    print(f"   Collections: {len(connection_test['collections'])}")
            else:
                errors.append(f"❌ MongoDB connection failed: {connection_test.get('error', 'Unknown error')}")
        except Exception as e:
            errors.append(f"❌ Cannot test MongoDB connection: {e}")

    return errors


def validate_external_services() -> List[str]:
    """Validate external service configurations."""
    warnings = []

    # Redis configuration (optional)
    redis_enabled = os.getenv('REDIS_ENABLED', 'true').lower() == 'true'
    if redis_enabled:
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = os.getenv('REDIS_PORT', '6379')
        print(f"✅ Redis enabled: {redis_host}:{redis_port}")

        # Test Redis connection if enabled
        try:
            import redis
            redis_url = os.getenv('REDIS_URL')
            if redis_url:
                client = redis.from_url(redis_url)
            else:
                client = redis.Redis(host=redis_host, port=int(redis_port))
            client.ping()
            print(f"✅ Redis connection successful")
        except ImportError:
            warnings.append("⚠️  Redis package not installed, will use in-memory cache")
        except Exception as e:
            warnings.append(f"⚠️  Redis connection failed: {e}, will use in-memory cache")
    else:
        print("ℹ️  Redis disabled - using in-memory cache (good for free hosting)")

    # Elasticsearch configuration (optional)
    es_enabled = os.getenv('ELASTICSEARCH_ENABLED', 'true').lower() == 'true'
    if es_enabled:
        es_host = os.getenv('ELASTICSEARCH_HOST', 'localhost')
        es_port = os.getenv('ELASTICSEARCH_PORT', '9200')
        print(f"ℹ️  Elasticsearch enabled: {es_host}:{es_port}")
    else:
        print("ℹ️  Elasticsearch disabled - using MongoDB text search")

    # Optional services
    optional_services = {
        'SENTRY_DSN': 'Sentry error tracking',
        'TMDB_API_KEY': 'TMDB API for movie information',
        'OMDB_API_KEY': 'OMDB API for movie information',
    }

    for var, description in optional_services.items():
        if os.getenv(var):
            print(f"✅ {var} is configured ({description})")
        else:
            warnings.append(f"⚠️  {var} not configured ({description})")

    return warnings


def validate_security_settings() -> List[str]:
    """Validate security-related settings."""
    warnings = []
    
    # Check if webhook is enabled
    if os.getenv('ENABLE_WEBHOOK', 'false').lower() == 'true':
        webhook_url = os.getenv('WEBHOOK_URL')
        webhook_secret = os.getenv('WEBHOOK_SECRET')
        
        if not webhook_url:
            warnings.append("⚠️  WEBHOOK_URL is required when ENABLE_WEBHOOK is true")
        if not webhook_secret:
            warnings.append("⚠️  WEBHOOK_SECRET is recommended when using webhooks")
    
    # Check rate limiting
    rate_limit = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    if rate_limit:
        print("✅ Rate limiting is enabled")
    else:
        warnings.append("⚠️  Rate limiting is disabled - consider enabling for production")
    
    return warnings


def validate_monitoring_config() -> List[str]:
    """Validate monitoring configuration."""
    info = []
    
    # Prometheus
    if os.getenv('PROMETHEUS_ENABLED', 'false').lower() == 'true':
        prometheus_port = os.getenv('PROMETHEUS_PORT', '8000')
        info.append(f"✅ Prometheus metrics enabled on port {prometheus_port}")
    else:
        info.append("ℹ️  Prometheus metrics disabled")
    
    # Sentry
    if os.getenv('SENTRY_DSN'):
        sentry_env = os.getenv('SENTRY_ENVIRONMENT', 'development')
        info.append(f"✅ Sentry error tracking enabled (environment: {sentry_env})")
    else:
        info.append("ℹ️  Sentry error tracking not configured")
    
    return info


def main():
    """Main validation function."""
    print("🔍 Validating Media Management Bot Configuration...")
    print("=" * 60)
    
    # Load environment variables
    env_files = ['.env', '.env.docker']
    for env_file in env_files:
        if os.path.exists(env_file):
            load_dotenv(env_file)
            print(f"📁 Loaded environment from {env_file}")
    
    print()
    
    # Run all validations
    all_errors = []
    all_warnings = []
    all_info = []
    
    print("🔧 Validating required environment variables...")
    all_errors.extend(validate_required_env_vars())
    print()
    
    print("📁 Validating file paths...")
    all_errors.extend(validate_paths())
    print()
    
    print("🗄️  Validating database configuration...")
    all_errors.extend(validate_database_config())
    print()
    
    print("🌐 Validating external services...")
    all_warnings.extend(validate_external_services())
    print()
    
    print("🔒 Validating security settings...")
    all_warnings.extend(validate_security_settings())
    print()
    
    print("📊 Validating monitoring configuration...")
    all_info.extend(validate_monitoring_config())
    print()
    
    # Use settings validation
    print("⚙️  Running comprehensive settings validation...")
    settings_errors = settings.validate()
    all_errors.extend(settings_errors)
    print()
    
    # Print summary
    print("=" * 60)
    print("📋 VALIDATION SUMMARY")
    print("=" * 60)
    
    if all_errors:
        print("❌ ERRORS (must be fixed):")
        for error in all_errors:
            print(f"   {error}")
        print()
    
    if all_warnings:
        print("⚠️  WARNINGS (recommended to fix):")
        for warning in all_warnings:
            print(f"   {warning}")
        print()
    
    if all_info:
        print("ℹ️  INFORMATION:")
        for info in all_info:
            print(f"   {info}")
        print()
    
    if not all_errors:
        print("✅ Configuration validation passed!")
        print("🚀 Your bot is ready to run!")
        return 0
    else:
        print("❌ Configuration validation failed!")
        print("🔧 Please fix the errors above before running the bot.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
