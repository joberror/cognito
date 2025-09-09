#!/usr/bin/env python3
"""
Show setup summary for the Media Management Bot.
This script displays what has been configured and next steps.
"""

import os
from pathlib import Path


def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} (missing)")
        return False


def show_directory_structure():
    """Show the created directory structure."""
    print("📁 Directory Structure:")
    directories = [
        "config/",
        "data/",
        "data/media/",
        "data/temp/",
        "logs/",
        "monitoring/",
        "monitoring/grafana/",
        "init-scripts/",
        "scripts/",
        "readme/"
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"   ✅ {directory}")
        else:
            print(f"   ❌ {directory}")


def show_configuration_files():
    """Show configuration files status."""
    print("\n⚙️  Configuration Files:")
    
    config_files = [
        (".env", "Main environment file"),
        (".env.docker", "Docker environment file"),
        (".env.example", "Example environment file"),
        ("config/settings.py", "Settings configuration"),
        ("docker-compose.yml", "Docker Compose configuration"),
        ("Dockerfile", "Docker build configuration"),
        ("Makefile", "Build and deployment commands"),
    ]
    
    for filepath, description in config_files:
        check_file_exists(filepath, description)


def show_scripts():
    """Show available scripts."""
    print("\n🔧 Available Scripts:")
    
    scripts = [
        ("scripts/setup.py", "Interactive setup script"),
        ("scripts/validate_config.py", "Configuration validation"),
        ("scripts/show_setup.py", "This summary script"),
    ]
    
    for filepath, description in scripts:
        check_file_exists(filepath, description)


def show_monitoring_files():
    """Show monitoring configuration files."""
    print("\n📊 Monitoring Configuration:")
    
    monitoring_files = [
        ("monitoring/prometheus.yml", "Prometheus configuration"),
        ("monitoring/grafana/datasources/prometheus.yml", "Grafana data source"),
        ("monitoring/grafana/dashboards/dashboard.yml", "Grafana dashboard config"),
    ]
    
    for filepath, description in monitoring_files:
        check_file_exists(filepath, description)


def show_database_files():
    """Show database initialization files."""
    print("\n🗄️  Database Configuration:")
    
    db_files = [
        ("init-scripts/01-init-database.sql", "Database initialization script"),
    ]
    
    for filepath, description in db_files:
        check_file_exists(filepath, description)


def show_readme_files():
    """Show documentation files."""
    print("\n📚 Documentation:")
    
    readme_files = [
        ("readme/intro.md", "Project introduction"),
        ("readme/scope.md", "Project scope"),
        ("readme/features.md", "Features list"),
        ("readme/commands.md", "Bot commands"),
        ("readme/configuration.md", "Configuration guide"),
        ("readme/deployment.md", "Deployment guide"),
    ]
    
    for filepath, description in readme_files:
        check_file_exists(filepath, description)


def show_next_steps():
    """Show next steps for the user."""
    print("\n🚀 Next Steps:")
    print("=" * 50)
    
    if not os.path.exists('.env') or os.path.getsize('.env') < 100:
        print("1. 🔧 Configure your environment:")
        print("   python scripts/setup.py")
        print("   # OR manually edit .env file")
        print()
    
    print("2. 📦 Install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    
    print("3. ✅ Validate configuration:")
    print("   python scripts/validate_config.py")
    print()
    
    print("4. 🤖 Run the bot:")
    print("   python bot.py")
    print("   # OR use Docker:")
    print("   docker-compose up -d")
    print()
    
    print("5. 📊 Optional - Enable monitoring:")
    print("   docker-compose --profile monitoring up -d")
    print()
    
    print("💡 Quick commands:")
    print("   make help          - Show all available commands")
    print("   make quickstart    - Complete setup in one command")
    print("   make validate      - Validate configuration")
    print("   make run           - Run the bot")
    print("   make docker-up     - Start with Docker")


def show_environment_variables():
    """Show key environment variables that need to be set."""
    print("\n🔑 Key Environment Variables to Configure:")
    print("=" * 50)
    
    required_vars = [
        ("BOT_TOKEN", "Get from @BotFather on Telegram"),
        ("TELEGRAM_API_ID", "Get from https://my.telegram.org/apps"),
        ("TELEGRAM_API_HASH", "Get from https://my.telegram.org/apps"),
        ("SUPER_ADMIN_ID", "Your Telegram user ID (bootstrap admin)"),
    ]
    
    optional_vars = [
        ("MONGODB_URI", "MongoDB connection string"),
        ("REDIS_HOST", "Redis server for caching"),
        ("ELASTICSEARCH_HOST", "Elasticsearch for search"),
        ("SENTRY_DSN", "Error tracking with Sentry"),
        ("TMDB_API_KEY", "Movie database API"),
    ]
    
    print("Required:")
    for var, description in required_vars:
        value = os.getenv(var, "NOT_SET")
        status = "✅" if value and value != "NOT_SET" and value != "YOUR_TELEGRAM_BOT_TOKEN" else "❌"
        print(f"   {status} {var}: {description}")

    print("\nOptional:")
    for var, description in optional_vars:
        value = os.getenv(var, "NOT_SET")
        status = "✅" if value and value != "NOT_SET" else "⚪"
        print(f"   {status} {var}: {description}")

    print("\nDynamic Management:")
    print("   🔧 Admins: Managed through bot commands (/admin promote, /admin demote)")
    print("   📺 Channels: Managed through bot commands (/channel add, /channel remove)")


def main():
    """Main function to show setup summary."""
    print("🎯 Media Management Bot - Setup Summary")
    print("=" * 60)
    
    show_directory_structure()
    show_configuration_files()
    show_scripts()
    show_monitoring_files()
    show_database_files()
    show_readme_files()
    show_environment_variables()
    show_next_steps()
    
    print("\n" + "=" * 60)
    print("✨ Setup complete! Your bot environment is ready.")
    print("📖 Check readme/configuration.md for detailed configuration guide")
    print("🚀 Check readme/deployment.md for deployment options")


if __name__ == "__main__":
    main()
