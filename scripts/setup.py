#!/usr/bin/env python3
"""
Setup script for the Media Management Bot.
This script helps users configure their environment interactively.
"""

import os
import sys
import shutil
from pathlib import Path


def create_directories():
    """Create necessary directories."""
    directories = [
        'data',
        'data/media',
        'data/temp',
        'logs',
        'config',
        'monitoring',
        'monitoring/grafana',
        'monitoring/grafana/dashboards',
        'monitoring/grafana/datasources',
        'init-scripts',
        'scripts'
    ]
    
    print("📁 Creating necessary directories...")
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")


def setup_env_file():
    """Setup the .env file interactively."""
    print("\n🔧 Setting up environment configuration...")
    
    if os.path.exists('.env'):
        response = input("❓ .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("   ⏭️  Skipping .env setup")
            return
    
    print("\n📝 Please provide the following information:")
    
    # Bot configuration
    bot_token = input("🤖 Telegram Bot Token (from @BotFather): ").strip()
    if not bot_token:
        print("❌ Bot token is required!")
        return
    
    bot_username = input("👤 Bot Username (without @): ").strip()
    admin_ids = input("👑 Admin User IDs (comma-separated): ").strip()
    
    # MongoDB configuration
    print("\n🍃 MongoDB Configuration:")
    print("This bot uses MongoDB as the database.")
    print("You can use MongoDB Atlas (cloud) or a local MongoDB installation.")

    use_atlas = input("Use MongoDB Atlas (cloud)? (Y/n): ").strip().lower()

    if use_atlas != 'n':
        # MongoDB Atlas setup
        print("\n📋 For MongoDB Atlas:")
        print("1. Create account at https://cloud.mongodb.com")
        print("2. Create a cluster")
        print("3. Get your connection string")

        mongodb_uri = input("\nMongoDB Connection String (mongodb+srv://...): ").strip()
        if not mongodb_uri:
            mongodb_uri = "mongodb+srv://your_user:your_password@your_cluster.mongodb.net/media_bot"

        db_name = input("Database Name [media_bot]: ").strip() or "media_bot"

        db_config = f"""
# MongoDB Configuration (Atlas)
MONGODB_URI={mongodb_uri}
MONGODB_DB={db_name}
"""
    else:
        # Local MongoDB setup
        host = input("MongoDB Host [localhost]: ").strip() or "localhost"
        port = input("MongoDB Port [27017]: ").strip() or "27017"
        db_name = input("Database Name [media_bot]: ").strip() or "media_bot"

        auth_required = input("Authentication required? (y/N): ").strip().lower() == 'y'

        if auth_required:
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            mongodb_uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
        else:
            username = ""
            password = ""
            mongodb_uri = f"mongodb://{host}:{port}/{db_name}"

        db_config = f"""
# MongoDB Configuration (Local)
MONGODB_URI={mongodb_uri}
MONGODB_HOST={host}
MONGODB_PORT={port}
MONGODB_DB={db_name}
MONGODB_USER={username}
MONGODB_PASSWORD={password}
"""
    
    # Channels
    channels = input("\n📺 Default Channels (comma-separated, with @): ").strip()
    
    # Optional services
    print("\n🌐 Optional Services (press Enter to skip):")
    sentry_dsn = input("Sentry DSN: ").strip()
    tmdb_key = input("TMDB API Key: ").strip()
    
    # Write .env file
    env_content = f"""# =============================================================================
# TELEGRAM BOT CONFIGURATION
# =============================================================================

BOT_TOKEN={bot_token}
BOT_USERNAME={bot_username}
BOT_NAME=Media Management Bot
BOT_DESCRIPTION=A comprehensive media management bot for Telegram channels

# Admin Configuration
ADMIN_USER_IDS={admin_ids}
SUPER_ADMIN_ID={admin_ids.split(',')[0] if admin_ids else ''}
{db_config}
# =============================================================================
# REDIS CONFIGURATION
# =============================================================================

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
REDIS_URL=redis://localhost:6379/0

# =============================================================================
# ELASTICSEARCH CONFIGURATION
# =============================================================================

ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_INDEX=media_files
ELASTICSEARCH_URL=http://localhost:9200

# =============================================================================
# MEDIA PROCESSING CONFIGURATION
# =============================================================================

MEDIA_STORAGE_PATH=./data/media
TEMP_STORAGE_PATH=./data/temp
MAX_FILE_SIZE=2147483648
ALLOWED_EXTENSIONS=mp4,mkv,avi,mov,wmv,flv,webm,m4v,3gp,mp3,flac,wav,aac,ogg,wma,m4a,jpg,jpeg,png,gif,bmp,webp,tiff,pdf,txt,doc,docx,zip,rar,7z

# =============================================================================
# CHANNEL MANAGEMENT
# =============================================================================

DEFAULT_CHANNELS={channels}
MONITORED_CHANNELS={channels}
AUTO_INDEX_NEW_FILES=true
INDEX_INTERVAL_HOURS=24
DUPLICATE_CHECK_ENABLED=true

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_FILE_PATH=./logs/bot.log
LOG_MAX_SIZE=10485760
LOG_BACKUP_COUNT=5

# =============================================================================
# SECURITY CONFIGURATION
# =============================================================================

RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW=60

# =============================================================================
# EXTERNAL SERVICES
# =============================================================================

SUPPORT_LINK=https://t.me/your_support_channel
GROUP_LINK=https://t.me/your_group
HELP_LINK=https://your-help-documentation.com
DONATION_LINK=https://your-donation-link.com

{f'SENTRY_DSN={sentry_dsn}' if sentry_dsn else '# SENTRY_DSN='}
{f'TMDB_API_KEY={tmdb_key}' if tmdb_key else '# TMDB_API_KEY='}

# =============================================================================
# DEVELOPMENT CONFIGURATION
# =============================================================================

ENVIRONMENT=development
DEBUG=true
ENABLE_DEBUG_COMMANDS=true
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")


def setup_docker_env():
    """Setup Docker environment file."""
    if not os.path.exists('.env'):
        print("❌ Please setup .env file first!")
        return
    
    print("\n🐳 Setting up Docker environment...")
    
    # Copy .env to .env.docker and modify for Docker
    shutil.copy('.env', '.env.docker')
    
    # Read and modify for Docker
    with open('.env.docker', 'r') as f:
        content = f.read()
    
    # Replace localhost with service names for Docker
    content = content.replace('localhost', 'host.docker.internal')
    content = content.replace('REDIS_HOST=host.docker.internal', 'REDIS_HOST=redis')
    content = content.replace('ELASTICSEARCH_HOST=host.docker.internal', 'ELASTICSEARCH_HOST=elasticsearch')
    content = content.replace('DATABASE_TYPE=postgresql', 'DATABASE_TYPE=postgresql')
    content = content.replace('POSTGRES_HOST=host.docker.internal', 'POSTGRES_HOST=postgres')
    content = content.replace('ENVIRONMENT=development', 'ENVIRONMENT=production')
    content = content.replace('DEBUG=true', 'DEBUG=false')
    
    with open('.env.docker', 'w') as f:
        f.write(content)
    
    print("✅ .env.docker file created successfully!")


def main():
    """Main setup function."""
    print("🚀 Media Management Bot Setup")
    print("=" * 40)
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_env_file()
    setup_docker_env()
    
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Review and customize your .env file")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Validate configuration: python scripts/validate_config.py")
    print("4. Run the bot: python bot.py")
    print("5. Or use Docker: docker-compose up -d")
    
    print("\n📚 For more information, check the readme files in the readme/ folder")


if __name__ == "__main__":
    main()
