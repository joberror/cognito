#!/usr/bin/env python3
"""
MongoDB setup script for the Media Management Bot.
This script helps configure MongoDB connection and initialize the database.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def setup_mongodb_env():
    """Setup MongoDB environment variables interactively."""
    print("🍃 MongoDB Configuration Setup")
    print("=" * 40)
    
    print("\nChoose your MongoDB setup:")
    print("1. MongoDB Atlas (Cloud) - Recommended")
    print("2. Local MongoDB installation")
    print("3. Custom MongoDB URI")
    
    choice = input("\nSelect option (1-3) [1]: ").strip() or "1"
    
    if choice == "1":
        setup_mongodb_atlas()
    elif choice == "2":
        setup_local_mongodb()
    elif choice == "3":
        setup_custom_mongodb()
    else:
        print("❌ Invalid choice")
        return


def setup_mongodb_atlas():
    """Setup MongoDB Atlas configuration."""
    print("\n🌐 MongoDB Atlas Setup")
    print("-" * 30)
    
    print("\n📋 You'll need:")
    print("1. MongoDB Atlas account (free at https://cloud.mongodb.com)")
    print("2. A cluster created")
    print("3. Database user credentials")
    print("4. Connection string")
    
    proceed = input("\nDo you have these ready? (y/N): ").strip().lower()
    if proceed != 'y':
        print("\n📖 Please visit https://cloud.mongodb.com to set up your Atlas cluster first.")
        return
    
    print("\n🔗 Enter your MongoDB Atlas connection details:")
    
    # Get connection string
    connection_string = input("MongoDB Connection String (mongodb+srv://...): ").strip()
    if not connection_string.startswith('mongodb+srv://'):
        print("❌ Atlas connection strings should start with 'mongodb+srv://'")
        return
    
    # Extract details from connection string if possible
    try:
        # Basic parsing to extract database name
        if '/' in connection_string:
            db_name = connection_string.split('/')[-1].split('?')[0]
            if not db_name:
                db_name = 'media_bot'
        else:
            db_name = 'media_bot'
    except:
        db_name = 'media_bot'
    
    db_name = input(f"Database name [{db_name}]: ").strip() or db_name
    
    # Update .env file
    update_env_file({
        'MONGODB_URI': connection_string
    })
    
    print("✅ MongoDB Atlas configuration saved!")


def setup_local_mongodb():
    """Setup local MongoDB configuration."""
    print("\n🏠 Local MongoDB Setup")
    print("-" * 25)
    
    host = input("MongoDB Host [localhost]: ").strip() or "localhost"
    port = input("MongoDB Port [27017]: ").strip() or "27017"
    db_name = input("Database Name [media_bot]: ").strip() or "media_bot"
    
    auth_required = input("Does your MongoDB require authentication? (y/N): ").strip().lower() == 'y'
    
    if auth_required:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        connection_string = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
    else:
        username = ""
        password = ""
        connection_string = f"mongodb://{host}:{port}/{db_name}"
    
    # Update .env file
    update_env_file({
        'MONGODB_URI': connection_string
    })
    
    print("✅ Local MongoDB configuration saved!")


def setup_custom_mongodb():
    """Setup custom MongoDB URI."""
    print("\n⚙️  Custom MongoDB Setup")
    print("-" * 25)
    
    connection_string = input("Enter your MongoDB URI: ").strip()
    if not connection_string:
        print("❌ Connection string is required")
        return
    
    db_name = input("Database Name [media_bot]: ").strip() or "media_bot"
    
    # Update .env file
    update_env_file({
        'MONGODB_URI': connection_string
    })
    
    print("✅ Custom MongoDB configuration saved!")


def update_env_file(config_vars):
    """Update .env file with MongoDB configuration."""
    env_file = '.env'

    # Read existing .env file
    env_content = {}
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_content[key] = value

    # Update with new values
    env_content.update(config_vars)

    # Write back to .env file
    with open(env_file, 'w') as f:
        f.write("# =============================================================================\n")
        f.write("# TELEGRAM BOT CONFIGURATION\n")
        f.write("# =============================================================================\n\n")

        # Write bot configuration first
        bot_vars = ['BOT_TOKEN', 'BOT_USERNAME', 'BOT_NAME', 'BOT_DESCRIPTION', 'ADMIN_USER_IDS', 'SUPER_ADMIN_ID']
        for var in bot_vars:
            if var in env_content:
                f.write(f"{var}={env_content[var]}\n")

        f.write("\n# =============================================================================\n")
        f.write("# DATABASE CONFIGURATION (MongoDB Only)\n")
        f.write("# =============================================================================\n\n")
        f.write("# MongoDB Connection URI (contains all connection details)\n")

        # Write only MongoDB URI
        if 'MONGODB_URI' in env_content:
            f.write(f"MONGODB_URI={env_content['MONGODB_URI']}\n")

        # Write other configurations
        f.write("\n# =============================================================================\n")
        f.write("# OTHER CONFIGURATIONS\n")
        f.write("# =============================================================================\n\n")

        skip_vars = bot_vars + ['MONGODB_URI']
        for key, value in env_content.items():
            if key not in skip_vars:
                f.write(f"{key}={value}\n")


def test_mongodb_connection():
    """Test MongoDB connection."""
    print("\n🔍 Testing MongoDB connection...")
    
    try:
        from config.mongodb import test_mongodb_connection
        
        result = test_mongodb_connection()
        
        if result['connected']:
            print("✅ MongoDB connection successful!")
            print(f"   Database: {result['database_name']}")
            if 'server_version' in result:
                print(f"   Server version: {result['server_version']}")
            if result['collections']:
                print(f"   Collections: {', '.join(result['collections'])}")
            return True
        else:
            print(f"❌ MongoDB connection failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False


def initialize_mongodb():
    """Initialize MongoDB database with collections and indexes."""
    print("\n🏗️  Initializing MongoDB database...")
    
    try:
        from config.mongodb import initialize_mongodb
        
        if initialize_mongodb():
            print("✅ MongoDB database initialized successfully!")
            print("   Collections and indexes created")
            return True
        else:
            print("❌ Failed to initialize MongoDB database")
            return False
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False


def main():
    """Main setup function."""
    print("🍃 MongoDB Setup for Media Management Bot")
    print("=" * 50)
    
    # Setup MongoDB configuration
    setup_mongodb_env()
    
    # Test connection
    if test_mongodb_connection():
        # Initialize database
        initialize_mongodb()
        
        print("\n🎉 MongoDB setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Configure your bot token and admin IDs in .env")
        print("2. Run: python scripts/validate_config.py")
        print("3. Start the bot: python bot.py")
    else:
        print("\n❌ MongoDB setup failed. Please check your configuration.")
        print("💡 Tips:")
        print("- Verify your connection string")
        print("- Check network connectivity")
        print("- Ensure database user has proper permissions")


if __name__ == "__main__":
    main()
