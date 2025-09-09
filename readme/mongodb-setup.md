# MongoDB Setup Guide

This guide explains how to configure the Media Management Bot to use MongoDB as the primary database.

## Quick Setup

### Option 1: Interactive Setup

```bash
python scripts/setup_mongodb.py
```

### Option 2: Manual Configuration

Edit your `.env` file with your MongoDB details:

```env
DATABASE_TYPE=mongodb
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/media_bot
```

## MongoDB Atlas (Cloud) Setup

### 1. Create MongoDB Atlas Account

1. Visit [MongoDB Atlas](https://cloud.mongodb.com)
2. Sign up for a free account
3. Create a new project

### 2. Create a Cluster

1. Click "Build a Database"
2. Choose "Shared" (free tier)
3. Select your preferred cloud provider and region
4. Name your cluster (e.g., "media-bot-cluster")
5. Click "Create Cluster"

### 3. Configure Database Access

1. Go to "Database Access" in the left sidebar
2. Click "Add New Database User"
3. Choose "Password" authentication
4. Create username and password
5. Set database user privileges to "Read and write to any database"
6. Click "Add User"

### 4. Configure Network Access

1. Go to "Network Access" in the left sidebar
2. Click "Add IP Address"
3. Choose "Allow Access from Anywhere" (0.0.0.0/0) for development
4. For production, add your server's specific IP address
5. Click "Confirm"

### 5. Get Connection String

1. Go to "Database" in the left sidebar
2. Click "Connect" on your cluster
3. Choose "Connect your application"
4. Select "Python" and version "3.6 or later"
5. Copy the connection string
6. Replace `<password>` with your database user password
7. Replace `<dbname>` with `media_bot`

Example connection string:

```
mongodb+srv://myuser:mypassword@cluster0.abc123.mongodb.net/media_bot?retryWrites=true&w=majority
```

## Environment Configuration

### Required Environment Variables

```env
# MongoDB Configuration (only one variable needed)
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/media_bot
```

### Example .env Configuration

```env
# =============================================================================
# TELEGRAM BOT CONFIGURATION
# =============================================================================
BOT_TOKEN=your_telegram_bot_token
BOT_USERNAME=Cognito
ADMIN_USER_IDS=123456789

# =============================================================================
# DATABASE CONFIGURATION (MongoDB Only)
# =============================================================================
# MongoDB Connection URI (contains all connection details)
MONGODB_URI=mongodb+srv://myuser:mypass@cluster0.abc123.mongodb.net/media_bot

# =============================================================================
# MEDIA PROCESSING CONFIGURATION
# =============================================================================
MEDIA_STORAGE_PATH=./data/media
TEMP_STORAGE_PATH=./data/temp
MAX_FILE_SIZE=2147483648
ALLOWED_EXTENSIONS=mp4,mkv,avi,mov,wmv,flv,webm,m4v

# ... other configurations
```

## Local MongoDB Setup

If you prefer to run MongoDB locally:

### 1. Install MongoDB

```bash
# Ubuntu/Debian
sudo apt-get install mongodb

# macOS with Homebrew
brew install mongodb-community

# Windows
# Download from https://www.mongodb.com/try/download/community
```

### 2. Start MongoDB Service

```bash
# Ubuntu/Debian
sudo systemctl start mongodb

# macOS
brew services start mongodb-community

# Windows
# MongoDB runs as a Windows service
```

### 3. Configure Environment

```env
# For local MongoDB
MONGODB_URI=mongodb://localhost:27017/media_bot
```

## Database Initialization

### Automatic Initialization

The bot will automatically create collections and indexes on first run.

### Manual Initialization

```bash
# Initialize database structure
make db-init

# Or run directly
python -c "from config.mongodb import initialize_mongodb; initialize_mongodb()"
```

### Using MongoDB Shell

You can also run the initialization script directly:

```bash
mongosh "mongodb+srv://cluster.mongodb.net/media_bot" --username myuser init-scripts/mongodb-init.js
```

## Testing Connection

### Using Make Command

```bash
make db-test
```

### Using Python Script

```bash
python -c "from config.mongodb import test_mongodb_connection; import json; print(json.dumps(test_mongodb_connection(), indent=2))"
```

### Using Validation Script

```bash
python scripts/validate_config.py
```

## Database Collections

The bot creates the following collections:

### users

- Stores Telegram user information
- Indexes: user_id (unique), username, is_admin

### channels

- Stores monitored channel information
- Indexes: channel_id (unique), channel_username, is_active

### media_files

- Stores media file metadata
- Indexes: file_id (unique), channel_id, file_type, file_name (text)

### search_index

- Stores search terms for quick lookup
- Indexes: file_id, search_terms, full_text (text)

### bot_stats

- Stores bot statistics and metrics
- Indexes: stat_type, timestamp

## Docker Configuration

The docker-compose.yml has been updated to use your online MongoDB instead of a local container:

```yaml
services:
  bot:
    build: .
    container_name: media_bot
    restart: unless-stopped
    env_file:
      - .env.docker
    depends_on:
      - redis
      - elasticsearch
    # Note: No postgres dependency - using online MongoDB
```

## Troubleshooting

### Common Issues

1. **Connection Timeout**

   - Check network connectivity
   - Verify IP whitelist in Atlas
   - Ensure correct connection string

2. **Authentication Failed**

   - Verify username and password
   - Check database user permissions
   - Ensure user has access to the database

3. **Database Not Found**

   - MongoDB creates databases automatically
   - Ensure database name is correct in connection string

4. **SSL/TLS Errors**
   - Atlas requires SSL connections
   - Use `mongodb+srv://` for Atlas connections
   - For local MongoDB, use `mongodb://`

### Debug Connection

```python
from config.mongodb import test_mongodb_connection
result = test_mongodb_connection()
print(result)
```

### View Logs

```bash
# View bot logs
tail -f logs/bot.log

# View MongoDB connection logs
grep -i mongodb logs/bot.log
```

## Security Best Practices

1. **Use Strong Passwords**

   - Generate complex passwords for database users
   - Rotate passwords regularly

2. **Network Security**

   - Whitelist specific IP addresses in production
   - Use VPN for additional security

3. **Database Permissions**

   - Create dedicated database users
   - Grant minimal required permissions
   - Avoid using admin users for applications

4. **Connection Security**
   - Always use SSL/TLS connections
   - Keep connection strings secure
   - Never commit credentials to version control

## Performance Optimization

### Indexes

The bot automatically creates optimized indexes for:

- User lookups
- Channel queries
- Media file searches
- Statistics aggregation

### Connection Pooling

MongoDB driver automatically handles connection pooling with:

- Maximum pool size: 50 connections
- Connection timeout: 10 seconds
- Socket timeout: 20 seconds

### Query Optimization

- Use compound indexes for multi-field queries
- Implement pagination for large result sets
- Cache frequently accessed data in Redis

## Monitoring

### MongoDB Atlas Monitoring

- Built-in performance monitoring
- Real-time metrics and alerts
- Query performance insights

### Application Monitoring

- Connection status in bot logs
- Database operation metrics
- Error tracking with Sentry

## Backup and Recovery

### MongoDB Atlas Backups

- Automatic continuous backups
- Point-in-time recovery
- Cross-region backup replication

### Manual Backups

```bash
# Export specific collection
mongoexport --uri="mongodb+srv://user:pass@cluster.net/media_bot" --collection=media_files --out=media_files.json

# Import collection
mongoimport --uri="mongodb+srv://user:pass@cluster.net/media_bot" --collection=media_files --file=media_files.json
```

## Migration from Other Databases

If migrating from SQLite or PostgreSQL:

1. **Export existing data**
2. **Transform data format** (if needed)
3. **Import to MongoDB** using mongoimport
4. **Update configuration** to use MongoDB
5. **Test thoroughly** before production deployment

## Next Steps

1. **Configure your MongoDB connection** in `.env`
2. **Test the connection**: `make db-test`
3. **Initialize the database**: `make db-init`
4. **Validate configuration**: `make validate`
5. **Start the bot**: `make run`

For additional help, check the main configuration guide or deployment documentation.
