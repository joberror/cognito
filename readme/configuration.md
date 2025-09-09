# Configuration Guide

This guide explains how to configure the Media Management Bot with all necessary environment variables and settings.

## Quick Setup

### Automated Setup

Run the interactive setup script:

```bash
python scripts/setup.py
```

### Manual Setup

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` with your configuration
3. Validate your configuration:
   ```bash
   python scripts/validate_config.py
   ```

## Required Configuration

### Telegram Bot Configuration

```env
# Get this from @BotFather on Telegram
BOT_TOKEN=your_telegram_bot_token

# Your bot's username (without @)
BOT_USERNAME=your_bot_username

# Admin user IDs (comma-separated)
ADMIN_USER_IDS=123456789,987654321

# Primary admin user ID
SUPER_ADMIN_ID=123456789
```

## Database Configuration (MongoDB Only)

### MongoDB Atlas (Recommended)

```env
# Single URI contains all connection details
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/media_bot
```

### Local MongoDB

```env
# For local MongoDB without authentication
MONGODB_URI=mongodb://localhost:27017/media_bot

# For local MongoDB with authentication
MONGODB_URI=mongodb://username:password@localhost:27017/media_bot
```

## External Services

### Redis (Caching)

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0
REDIS_URL=redis://localhost:6379/0
```

### Elasticsearch (Search)

```env
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_INDEX=media_files
ELASTICSEARCH_URL=http://localhost:9200
```

## Media Processing

### File Storage

```env
MEDIA_STORAGE_PATH=./data/media
TEMP_STORAGE_PATH=./data/temp
MAX_FILE_SIZE=2147483648  # 2GB in bytes
```

### Supported File Types

```env
ALLOWED_EXTENSIONS=mp4,mkv,avi,mov,wmv,flv,webm,m4v,3gp,mp3,flac,wav,aac,ogg,wma,m4a,jpg,jpeg,png,gif,bmp,webp,tiff,pdf,txt,doc,docx,zip,rar,7z
```

### FFmpeg Configuration

```env
FFMPEG_PATH=/usr/bin/ffmpeg
FFPROBE_PATH=/usr/bin/ffprobe
```

## Channel Management (Dynamic)

Channels are managed dynamically through bot commands:

```
/channel add @channel_name     # Add channel to monitoring
/channel remove @channel_name  # Remove channel from monitoring
/channel list                  # List all monitored channels
/channel info @channel_name    # Get channel information
```

Global channel processing settings:

```env
# Auto-indexing settings (applies to all channels)
AUTO_INDEX_NEW_FILES=true
INDEX_INTERVAL_HOURS=24
DUPLICATE_CHECK_ENABLED=true
```

## Security Settings

### Rate Limiting

```env
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW=60  # seconds
```

### User Management

```env
MAX_USERS_PER_CHANNEL=10000
USER_TIMEOUT_MINUTES=30
BAN_DURATION_HOURS=24
```

### Webhooks (Optional)

```env
ENABLE_WEBHOOK=false
WEBHOOK_URL=https://your-domain.com/webhook
WEBHOOK_SECRET=your_webhook_secret
```

## Logging Configuration

```env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_FILE_PATH=./logs/bot.log
LOG_MAX_SIZE=10485760  # 10MB
LOG_BACKUP_COUNT=5

# Feature-specific logging
LOG_MEDIA_PROCESSING=true
LOG_USER_ACTIONS=true
LOG_ADMIN_ACTIONS=true
LOG_SEARCH_QUERIES=true
```

## Monitoring & Analytics

### Prometheus Metrics

```env
PROMETHEUS_ENABLED=false
PROMETHEUS_PORT=8000
```

### Sentry Error Tracking

```env
SENTRY_DSN=your_sentry_dsn
SENTRY_ENVIRONMENT=development
```

### Statistics

```env
STATS_UPDATE_INTERVAL=3600  # 1 hour
KEEP_STATS_DAYS=30
```

## External APIs (Optional)

```env
# Movie database APIs
TMDB_API_KEY=your_tmdb_api_key
OMDB_API_KEY=your_omdb_api_key
```

## Support Links

```env
SUPPORT_LINK=https://t.me/your_support_channel
GROUP_LINK=https://t.me/your_group
HELP_LINK=https://your-help-documentation.com
DONATION_LINK=https://your-donation-link.com
```

## Development Settings

```env
ENVIRONMENT=development  # development, staging, production
DEBUG=true

# Testing
TEST_DATABASE_URL=sqlite:///./data/test.db
TEST_REDIS_URL=redis://localhost:6379/1

# Development tools
ENABLE_DEBUG_COMMANDS=true
MOCK_EXTERNAL_SERVICES=false
```

## Docker Configuration

For Docker deployment, use `.env.docker` with service names:

```env
# Use service names instead of localhost
REDIS_HOST=redis
POSTGRES_HOST=postgres
ELASTICSEARCH_HOST=elasticsearch

# Production settings
ENVIRONMENT=production
DEBUG=false
```

## Configuration Validation

Always validate your configuration before running:

```bash
python scripts/validate_config.py
```

This will check:

- ✅ Required environment variables
- ✅ File paths and permissions
- ✅ Database connectivity
- ✅ External service configuration
- ⚠️ Optional services and recommendations

## Environment Files

- `.env` - Local development configuration
- `.env.docker` - Docker deployment configuration
- `.env.example` - Example configuration template

## Security Best Practices

1. **Never commit sensitive data** to version control
2. **Use strong passwords** for database connections
3. **Enable rate limiting** in production
4. **Use HTTPS** for webhook URLs
5. **Regularly rotate** API keys and tokens
6. **Monitor logs** for suspicious activity

## Troubleshooting

### Common Issues

1. **Bot token invalid**: Check token from @BotFather
2. **Database connection failed**: Verify database credentials
3. **Permission denied**: Check file/directory permissions
4. **Service unavailable**: Ensure external services are running

### Getting Help

- Check the logs in `./logs/bot.log`
- Run configuration validation
- Review the troubleshooting section in the main README
