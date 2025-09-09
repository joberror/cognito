# Render.com Free Tier Deployment Guide

This guide explains how to deploy your Media Management Bot on Render.com's free tier with optimized configurations.

## 🆓 Render.com Free Tier Limitations

### ✅ What's Included (FREE)
- **Web Services** - 750 hours/month (sleeps after 15min inactivity)
- **Static Sites** - Unlimited
- **Bandwidth** - 100GB/month
- **Build Minutes** - 500 minutes/month

### ❌ What's NOT Included (Paid Only)
- **Redis** - Requires paid plan ($7+/month)
- **PostgreSQL** - Free for 90 days, then deleted
- **Background Workers** - Paid feature
- **Always-On Services** - Paid feature

## 🛠️ Free Tier Solution Architecture

### Database: MongoDB Atlas (Free)
- **✅ 512MB storage** - Perfect for bot data
- **✅ Always available** - No sleep/deletion
- **✅ Global clusters** - Good performance

### Caching: In-Memory (No Redis)
- **✅ Built-in fallback** - Works without Redis
- **⚠️ Limited capacity** - 1000 items max
- **⚠️ Resets on restart** - Cache lost when service sleeps

### Search: MongoDB Text Search (No Elasticsearch)
- **✅ Built-in MongoDB** - No additional service needed
- **⚠️ Basic functionality** - Less advanced than Elasticsearch
- **✅ Free tier compatible** - No resource overhead

## 🚀 Deployment Steps

### 1. Prepare Your Repository

#### Update Environment Configuration
```bash
# Copy Render-optimized configuration
cp .env.render .env

# Edit with your actual values
nano .env
```

#### Key Settings for Render.com
```env
# Disable Redis (not available on free tier)
REDIS_ENABLED=false

# Use MongoDB Atlas (free tier)
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/cognito

# Enable webhooks (recommended for Render)
ENABLE_WEBHOOK=true
WEBHOOK_URL=https://your-app-name.onrender.com/webhook

# Optimize for free tier resources
MAX_FILE_SIZE=52428800  # 50MB instead of 2GB
SEARCH_RESULTS_LIMIT=25  # Reduced for performance
```

### 2. Create Render.com Service

1. **Sign up** at [render.com](https://render.com)
2. **Connect GitHub** repository
3. **Create Web Service**:
   - **Name**: `your-bot-name`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`

### 3. Configure Environment Variables

In Render.com dashboard, add these environment variables:

```env
BOT_TOKEN=your_telegram_bot_token
SUPER_ADMIN_ID=your_telegram_user_id
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/cognito
REDIS_ENABLED=false
WEBHOOK_URL=https://your-app-name.onrender.com/webhook
WEBHOOK_SECRET=your_webhook_secret
ENVIRONMENT=production
DEBUG=false
```

### 4. Set Up MongoDB Atlas

1. **Create Account** at [mongodb.com/atlas](https://www.mongodb.com/atlas)
2. **Create Free Cluster** (M0 Sandbox - 512MB)
3. **Configure Network Access** - Allow all IPs (0.0.0.0/0)
4. **Create Database User** with read/write permissions
5. **Get Connection String** and add to `MONGODB_URI`

### 5. Configure Telegram Webhook

After deployment, set up the webhook:

```bash
# Replace with your actual bot token and Render URL
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-app-name.onrender.com/webhook"}'
```

## ⚡ Performance Optimizations for Free Tier

### 1. **Reduced Resource Usage**
```env
# Smaller file size limits
MAX_FILE_SIZE=52428800  # 50MB instead of 2GB
MAX_IMAGE_SIZE=5242880  # 5MB instead of 10MB

# Smaller search results
SEARCH_RESULTS_LIMIT=25  # Instead of 50

# Less frequent operations
INDEX_INTERVAL_HOURS=24
STATS_UPDATE_INTERVAL=7200  # 2 hours
```

### 2. **Memory Optimization**
```env
# Reduced cache size
SEARCH_CACHE_TTL=1800  # 30 minutes instead of 1 hour

# Smaller batches
INDEX_BATCH_SIZE=50  # Instead of 100

# Less logging
LOG_USER_ACTIONS=false
LOG_SEARCH_QUERIES=false
```

### 3. **Service Sleep Handling**
```python
# Bot will automatically handle service sleep/wake
# Webhook ensures instant wake-up on new messages
# In-memory cache will rebuild after wake-up
```

## 🔧 Free Tier Limitations & Workarounds

### 1. **Service Sleep (15min inactivity)**
- **Problem**: Service sleeps after 15 minutes of no requests
- **Solution**: Webhooks wake service instantly on new messages
- **Impact**: First message after sleep may be slower (~10-30 seconds)

### 2. **No Redis Caching**
- **Problem**: No persistent caching between restarts
- **Solution**: In-memory cache with MongoDB fallback
- **Impact**: Slower search/repeated queries, cache rebuilds after sleep

### 3. **Limited Storage**
- **Problem**: No persistent file storage
- **Solution**: Use `/tmp` for temporary files, MongoDB for metadata
- **Impact**: Files not permanently stored on server

### 4. **Memory Constraints**
- **Problem**: Limited RAM on free tier
- **Solution**: Reduced batch sizes, smaller cache, optimized queries
- **Impact**: Slower processing of large operations

## 📊 Expected Performance

### ✅ **What Works Well**
- Basic bot commands (instant)
- Database operations (fast with MongoDB Atlas)
- Small file processing (<50MB)
- Admin/channel management
- Search functionality (basic)

### ⚠️ **What's Slower**
- First request after sleep (10-30 seconds)
- Large file processing
- Complex search queries
- Cache rebuilding after restart

### ❌ **What Doesn't Work**
- Files >50MB (size limit)
- Advanced Elasticsearch features
- Persistent file storage
- Background tasks while sleeping

## 🔍 Monitoring & Troubleshooting

### Check Service Status
```bash
# View logs in Render dashboard
# Monitor service health
# Check webhook status
```

### Common Issues

1. **Service Won't Start**
   - Check environment variables
   - Verify MongoDB connection
   - Review build logs

2. **Bot Not Responding**
   - Check webhook configuration
   - Verify bot token
   - Check service logs

3. **Database Errors**
   - Verify MongoDB Atlas connection
   - Check network access settings
   - Confirm user permissions

## 💰 Cost Comparison

### Free Tier (Render + MongoDB Atlas)
- **Cost**: $0/month
- **Limitations**: Service sleep, no Redis, basic features
- **Good for**: Development, small bots, testing

### Paid Tier (Render + Redis)
- **Cost**: ~$7-15/month
- **Benefits**: Always-on, Redis caching, better performance
- **Good for**: Production bots, high usage

## 🚀 Upgrade Path

When ready to upgrade:

1. **Enable Redis** ($7/month)
   ```env
   REDIS_ENABLED=true
   ```

2. **Upgrade to Starter Plan** ($7/month)
   - No service sleep
   - Better performance
   - More resources

3. **Add Elasticsearch** (if needed)
   - Better search functionality
   - Advanced indexing

## ✅ Deployment Checklist

- [ ] MongoDB Atlas cluster created and configured
- [ ] Environment variables set in Render dashboard
- [ ] Repository connected to Render
- [ ] Service deployed successfully
- [ ] Webhook configured with Telegram
- [ ] Bot responding to messages
- [ ] Database connection working
- [ ] Admin commands functional

## 🎯 Summary

**Render.com free tier is perfect for:**
- ✅ Development and testing
- ✅ Small to medium bots
- ✅ Learning and experimentation
- ✅ MVP deployment

**Consider paid tier for:**
- ⚡ High-traffic bots
- ⚡ Always-on requirements
- ⚡ Advanced caching needs
- ⚡ Production workloads

Your bot will work great on the free tier with the optimized configuration! 🎉
