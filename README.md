# 🎬 Cognito - Movie Management Bot

A powerful Telegram bot that creates a Netflix-like search experience for private movie channels.

## 🎯 **What It Does**

Cognito automatically indexes movie files from private Telegram channels and provides users with intelligent search functionality and direct download links.

### **Key Features**
- 🔗 **Channel Management** - Connect to multiple private movie channels
- 📊 **Auto-Indexing** - Automatically scan and index new movie uploads
- 🎬 **Rich Metadata** - Extract movie details (title, year, quality, genre, cast, etc.)
- 🔍 **Smart Search** - Advanced search with fuzzy matching and intelligent ranking
- 📱 **User-Friendly** - Simple commands with beautiful formatted results
- ⚙️ **Admin Controls** - Comprehensive admin panel for management

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.9+
- MongoDB Atlas account (free tier)
- Telegram Bot Token (from @BotFather)
- Telegram API credentials (from https://my.telegram.org/apps)

### **Installation**
```bash
# Clone the repository
git clone https://github.com/yourusername/cognito.git
cd cognito

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run the bot
python bot.py
```

### **Configuration**
Edit `.env` file with your credentials:
```env
# Telegram Configuration
BOT_TOKEN=your_telegram_bot_token
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
SUPER_ADMIN_ID=your_telegram_user_id

# Database
MONGODB_URI=your_mongodb_connection_string

# Search Engine
SEARCH_ENGINE=whoosh  # Recommended for better search features
```

## 📚 **Documentation**

### **User Guide**
- [User Guide](readme/USER_GUIDE.md) - How to use the bot
- [Search Options](readme/search-options.md) - Search engine comparison
- [Movie Configuration](readme/MOVIE_BOT_CONFIGURATION.md) - Movie-specific settings

### **Setup & Deployment**
- [Configuration Guide](readme/configuration.md) - Detailed configuration
- [MongoDB Setup](readme/mongodb-setup.md) - Database setup
- [Telegram API Setup](readme/telegram-api-setup.md) - API credentials
- [Render Deployment](readme/render-deployment.md) - Free hosting deployment

### **Development**
- [Bot Workflow](BOT_WORKFLOW_OVERVIEW.md) - System architecture
- [Feature Development Plan](readme/FEATURE_DEVELOPMENT_PLAN.md) - Development roadmap
- [Features Overview](readme/features.md) - All planned features

## 🎬 **How It Works**

### **For Users**
```
1. Search: /search batman 2022
2. Get Results: Movie details with download links
3. Click Link: Direct access to movie file
4. Download: From original Telegram channel
```

### **For Admins**
```
1. Add Channels: /channel add @movie_channel
2. Auto-Index: Bot scans and indexes movies
3. Manage Users: Promote/demote admins
4. Monitor: View statistics and system health
```

## 🔍 **Search Examples**

### **Basic Search**
```
/search batman 2022
/search action movies
/search christopher nolan
```

### **Advanced Search**
```
/search title:batman AND year:2022
/search genre:action AND quality:1080p
/search director:nolan OR director:tarantino
```

## 🏗️ **Architecture**

```
Telegram Channels → Bot (Python) → MongoDB → Whoosh Search → Users
     ↓                ↓              ↓           ↓           ↓
Private Movie    Auto-Index    Rich Metadata  Fast Search  Download Links
   Channels      + Monitor     + Curation     + Ranking    + Direct Access
```

### **Tech Stack**
- **Backend**: Python 3.9+ with asyncio
- **Bot Framework**: python-telegram-bot + Telethon
- **Database**: MongoDB Atlas (free tier compatible)
- **Search Engine**: Whoosh (file-based, free)
- **Hosting**: Render.com (free tier compatible)
- **Environment**: Docker support included

## 🌟 **Features**

### **Current Features**
- ✅ Environment configuration system
- ✅ MongoDB integration with auto-setup
- ✅ Dynamic admin management
- ✅ Dynamic channel management
- ✅ Whoosh search engine integration
- ✅ Movie-optimized file handling
- ✅ Free hosting optimization

### **Planned Features** (Development Branches)
- 🔄 Welcome system (`feature/welcome`)
- 🔄 Channel management (`feature/channel-management`)
- 🔄 Auto-indexing (`feature/auto-indexing`)
- 🔄 Metadata extraction (`feature/metadata-extraction`)
- 🔄 Search engine (`feature/search-engine`)
- 🔄 User interface (`feature/user-interface`)
- 🔄 Admin panel (`feature/admin-panel`)

## 🚀 **Deployment**

### **Free Hosting (Render.com)**
```bash
# Use optimized configuration
cp .env.render .env

# Deploy to Render.com
# See readme/render-deployment.md for details
```

### **Docker**
```bash
# Build and run with Docker
docker-compose up -d
```

### **Local Development**
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python bot.py
```

## 🤝 **Contributing**

### **Development Workflow**
1. Create feature branch: `git checkout -b feature/your-feature`
2. Develop and test your feature
3. Create pull request to main branch
4. Code review and merge

### **Branch Strategy**
- `main` - Production-ready code
- `feature/*` - Individual feature development
- Each feature developed independently and merged when complete

## 📊 **Project Status**

### **Current Phase**: Foundation Setup ✅
- [x] Environment configuration
- [x] Database setup
- [x] Search engine integration
- [x] Admin/channel management systems
- [x] Movie-specific optimizations

### **Next Phase**: Core Features 🔄
- [ ] Welcome system
- [ ] Channel management UI
- [ ] Auto-indexing system
- [ ] Metadata extraction
- [ ] Search functionality

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Support**

- 📖 **Documentation**: Check the `readme/` directory
- 🐛 **Issues**: Create an issue on GitHub
- 💬 **Discussions**: Use GitHub Discussions
- 📧 **Contact**: [Your contact information]

## 🙏 **Acknowledgments**

- Telegram Bot API and MTProto API
- MongoDB Atlas for free database hosting
- Whoosh for excellent search capabilities
- Render.com for free hosting platform
- All contributors and users

---

**Made with ❤️ for movie enthusiasts who want better organization of their Telegram movie collections!** 🍿🎬
