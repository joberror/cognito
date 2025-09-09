# Telegram API Setup Guide

This guide explains how to get and configure your Telegram API credentials (API_ID and API_HASH) for advanced bot features.

## 🤔 Do You Need API_ID and API_HASH?

### ✅ **You NEED them for:**
- **Channel Monitoring** - Automatically detect new files in channels
- **User Client Operations** - Act as a user (not just bot)
- **Advanced Media Handling** - Download large files, access restricted content
- **Channel Management** - Join/leave channels programmatically
- **Message History** - Access old messages in channels
- **User Information** - Get detailed user/channel info
- **File Downloads** - Download files larger than bot API limits

### ⚠️ **You DON'T need them for:**
- Basic bot commands (`/start`, `/help`, etc.)
- Responding to direct messages
- Simple file uploads/downloads (under 50MB)
- Basic admin commands
- Database operations

## 🔑 Getting Your API Credentials

### Step 1: Visit Telegram's Developer Portal
1. Go to **https://my.telegram.org/apps**
2. Log in with your Telegram account (phone number + verification code)

### Step 2: Create a New Application
1. Click **"Create application"**
2. Fill in the form:
   - **App title**: `Media Management Bot` (or your preferred name)
   - **Short name**: `media_bot` (or your preferred short name)
   - **URL**: Leave empty or add your website
   - **Platform**: Choose **"Desktop"**
   - **Description**: `Telegram media management bot`

### Step 3: Get Your Credentials
After creating the app, you'll see:
- **API ID**: A number (e.g., `1234567`)
- **API Hash**: A string (e.g., `abcdef1234567890abcdef1234567890`)

### Step 4: Add to Your Environment
```env
# Add these to your .env file
TELEGRAM_API_ID=1234567
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
```

## 🛡️ Security Considerations

### ⚠️ **IMPORTANT SECURITY NOTES:**
1. **Keep credentials SECRET** - Never share or commit to public repos
2. **API_HASH is sensitive** - Treat it like a password
3. **One app per bot** - Don't reuse credentials across projects
4. **Monitor usage** - Telegram has rate limits and abuse detection

### 🔒 **Best Practices:**
- Use environment variables (never hardcode)
- Use different credentials for development/production
- Regularly rotate credentials if compromised
- Monitor API usage in Telegram's developer portal

## 🔧 Configuration Examples

### Development Environment
```env
# .env (development)
TELEGRAM_API_ID=1234567
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
BOT_TOKEN=your_dev_bot_token
```

### Production Environment
```env
# .env.render (production)
TELEGRAM_API_ID=7654321
TELEGRAM_API_HASH=fedcba0987654321fedcba0987654321
BOT_TOKEN=your_prod_bot_token
```

### Docker Environment
```env
# .env.docker
TELEGRAM_API_ID=1234567
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
```

## 🚀 Using API Credentials in Your Bot

### Basic Client Setup
```python
from telethon import TelegramClient
import os

# Get credentials from environment
api_id = int(os.getenv('TELEGRAM_API_ID'))
api_hash = os.getenv('TELEGRAM_API_HASH')

# Create client
client = TelegramClient('bot_session', api_id, api_hash)

async def main():
    await client.start(bot_token=os.getenv('BOT_TOKEN'))
    # Your bot logic here
    
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

### Channel Monitoring Example
```python
from telethon import events

@client.on(events.NewMessage(chats=['@your_channel']))
async def handle_new_file(event):
    if event.media:
        # Process new media file
        print(f"New file in channel: {event.file.name}")
        # Add to database, process, etc.
```

## 📚 Libraries That Use API Credentials

### Telethon (Recommended)
```python
# Install: pip install telethon
from telethon import TelegramClient

client = TelegramClient('session', api_id, api_hash)
```

### Pyrogram (Alternative)
```python
# Install: pip install pyrogram
from pyrogram import Client

client = Client('session', api_id, api_hash)
```

## 🔍 Troubleshooting

### Common Issues

1. **"Invalid API_ID or API_HASH"**
   - Double-check credentials from my.telegram.org
   - Ensure API_ID is an integer, API_HASH is a string
   - Check for extra spaces or quotes

2. **"Phone number required"**
   - You're using user client methods
   - Use bot token for bot operations
   - Some features require user authentication

3. **"Rate limit exceeded"**
   - Telegram has strict rate limits
   - Implement proper delays between requests
   - Use bot API when possible (higher limits)

4. **"Session file errors"**
   - Delete old session files
   - Use unique session names
   - Check file permissions

### Debug Configuration
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# This will show detailed API calls and responses
```

## 🎯 Feature Comparison

| Feature | Bot API Only | Bot API + User Client |
|---------|-------------|----------------------|
| Basic Commands | ✅ Full support | ✅ Full support |
| File Downloads | ⚠️ 50MB limit | ✅ No limit |
| Channel Monitoring | ❌ Manual only | ✅ Automatic |
| Message History | ❌ Recent only | ✅ Full history |
| User Information | ⚠️ Basic info | ✅ Detailed info |
| Channel Management | ⚠️ Limited | ✅ Full control |

## 📋 Setup Checklist

- [ ] Visit https://my.telegram.org/apps
- [ ] Create new application
- [ ] Copy API_ID and API_HASH
- [ ] Add to .env file
- [ ] Install telethon or pyrogram
- [ ] Test connection
- [ ] Implement channel monitoring
- [ ] Set up proper error handling

## 🔄 Migration Guide

### If You Don't Have API Credentials Yet
1. Your bot will work with basic features
2. Channel monitoring will be manual
3. File size limits apply
4. Add credentials when ready for advanced features

### Adding API Credentials to Existing Bot
1. Get credentials from my.telegram.org
2. Add to environment variables
3. Install telethon/pyrogram
4. Update bot code to use client
5. Test thoroughly

## 🌐 Deployment Considerations

### Render.com
```env
# Add to Render environment variables
TELEGRAM_API_ID=1234567
TELEGRAM_API_HASH=your_api_hash
```

### Docker
```dockerfile
# Session files will be stored in container
# Consider using volumes for persistence
VOLUME ["/app/sessions"]
```

### Security in Production
- Use secrets management (not plain env vars)
- Rotate credentials regularly
- Monitor API usage
- Implement proper logging

## ✅ Summary

**API_ID and API_HASH are essential for:**
- 🔄 **Automatic channel monitoring**
- 📁 **Large file handling**
- 👥 **Advanced user operations**
- 📊 **Comprehensive media management**

**Without them, your bot will:**
- ✅ Handle basic commands
- ✅ Process direct uploads
- ❌ Miss automatic channel monitoring
- ❌ Have file size limitations

**Get them from: https://my.telegram.org/apps** 🚀
