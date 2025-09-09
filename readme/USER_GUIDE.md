# Movie Management Bot - User Guide

## 🎬 **What This Bot Does**

This bot helps you **find and access movies** from connected private Telegram channels. Think of it as a **search engine for movie collections** across multiple channels.

## 🚀 **Getting Started**

### **Step 1: Start the Bot**
```
/start
```
The bot will welcome you and explain how to use it.

### **Step 2: Search for Movies**
```
/search batman 2022
```
The bot will show you all Batman movies from 2022 with download links.

### **Step 3: Download Movies**
Click the download link in the search results to access the movie file directly from the original channel.

## 🔍 **How to Search**

### **Basic Search**
```
/search <movie name>
/search batman
/search avengers
/search john wick
```

### **Search with Year**
```
/search batman 2022
/search marvel 2023
/search nolan 2020
```

### **Search with Quality**
```
/search batman 1080p
/search avengers 4k
/search comedy 720p
```

### **Search by Genre**
```
/search action movies
/search horror 2023
/search comedy tom hanks
```

### **Search by Director**
```
/search christopher nolan
/search tarantino movies
/search marvel russo brothers
```

## 🎯 **Advanced Search**

### **Exact Title Search**
```
/movie "The Dark Knight"
/movie "Avengers: Endgame"
```

### **Multiple Keywords**
```
/search action sci-fi 2023
/search comedy romance 1080p
/search horror thriller recent
```

### **Advanced Query Syntax** (Power Users)
```
/search title:batman AND year:2022
/search genre:action AND quality:1080p
/search director:nolan OR director:tarantino
/search year:[2020 TO 2023] AND genre:sci-fi
/search rating:>8.0 AND quality:4k
```

## 📋 **All Available Commands**

### **Search Commands**
```
/search <query>     - Search for movies
/find <query>       - Same as search
/movie <title>      - Search for specific movie title
/random             - Get a random movie recommendation
/popular            - Show most popular/downloaded movies
/recent             - Show recently added movies
```

### **Information Commands**
```
/start              - Welcome message and instructions
/help               - Show all available commands
/about              - Information about the bot
/stats              - Show bot statistics (total movies, etc.)
```

## 🎬 **Understanding Search Results**

### **Result Format**
```
🎬 **The Batman (2022)**
📊 **Quality:** 1080p BluRay x264
📁 **Size:** 2.1 GB | ⏱️ **Duration:** 2h 56m
🎭 **Genre:** Action, Crime, Drama
🎬 **Director:** Matt Reeves
⭐ **Rating:** 7.8/10 (IMDb)
🗣️ **Language:** English
📺 **Source:** @premium_movies_hd

🔗 **[📥 Download Movie]** ← Click this link
```

### **What Each Field Means**
- **🎬 Title & Year** - Movie name and release year
- **📊 Quality** - Video resolution and source (BluRay, WEB-DL, etc.)
- **📁 Size & Duration** - File size and movie length
- **🎭 Genre** - Movie categories
- **🎬 Director** - Movie director(s)
- **⭐ Rating** - IMDb or other ratings
- **🗣️ Language** - Audio language
- **📺 Source** - Which channel has this movie
- **🔗 Download Link** - Direct link to the movie file

## 📱 **How Download Links Work**

### **Step-by-Step Process**
```
1. You search: /search batman 2022
2. Bot shows results with download links
3. You click: [📥 Download Movie]
4. Telegram opens the original channel message
5. You download the movie file directly
```

### **Important Notes**
- ✅ **Direct Access** - Links go directly to original files
- ✅ **No Proxy** - Bot doesn't store or proxy files
- ✅ **Original Quality** - Files are exactly as uploaded
- ✅ **Fast Downloads** - Direct Telegram download speeds

## 🎯 **Search Tips & Tricks**

### **For Best Results**
```
✅ Use specific movie titles: "The Dark Knight" vs "batman"
✅ Include year for popular titles: "batman 2022"
✅ Add quality if you prefer: "batman 1080p"
✅ Try different keywords: "dark knight" vs "batman"
```

### **If You Can't Find a Movie**
```
1. Try different spellings: "grey" vs "gray"
2. Try original title: "Le Fabuleux Destin d'Amélie"
3. Try director name: "christopher nolan"
4. Try genre + year: "sci-fi 2023"
5. Ask admin to check if movie exists in channels
```

### **Handling Typos**
The bot is smart about typos:
```
"funy cats" → finds "funny cats"
"moive" → finds "movie"
"avanger" → finds "avengers"
```

## 📊 **Movie Categories**

### **By Quality**
- **4K/UHD** - Ultra high definition (3840×2160)
- **1080p** - Full HD (1920×1080)
- **720p** - HD (1280×720)
- **480p** - Standard definition

### **By Source**
- **BluRay** - Highest quality, from Blu-ray disc
- **WEB-DL** - Downloaded from streaming service
- **WEBRip** - Recorded from streaming service
- **DVDRip** - From DVD disc
- **CAM** - Recorded in theater (lowest quality)

### **By Format**
- **MP4** - Most compatible, works everywhere
- **MKV** - High quality, multiple audio/subtitle tracks
- **AVI** - Older format, widely supported

## 🔒 **Privacy & Security**

### **What the Bot Does**
- ✅ **Searches** movie database for you
- ✅ **Provides links** to original files
- ✅ **Tracks** search statistics (anonymous)

### **What the Bot Doesn't Do**
- ❌ **Store movies** - Files stay in original channels
- ❌ **Copy files** - Direct links only
- ❌ **Track downloads** - Your privacy is protected
- ❌ **Share data** - No personal information collected

## 🆘 **Troubleshooting**

### **Common Issues**

**"No results found"**
```
- Try different keywords
- Check spelling
- Try searching by director or genre
- Movie might not be in connected channels
```

**"Link doesn't work"**
```
- Movie might have been deleted from channel
- You might not have access to that channel
- Try searching for alternative versions
```

**"Bot is slow"**
```
- High traffic periods may cause delays
- Try again in a few minutes
- Use more specific search terms
```

**"Can't download file"**
```
- Check your internet connection
- Make sure you have enough storage space
- File might be temporarily unavailable
```

### **Getting Help**
```
/help           - Show all commands
/about          - Bot information
Contact admin   - For technical issues
```

## 🎉 **Pro Tips**

### **Power User Features**
```
1. Use quotes for exact titles: /movie "The Matrix"
2. Combine filters: /search action 1080p 2023
3. Use advanced syntax: title:batman AND year:2022
4. Bookmark favorite searches
5. Check /recent for new additions
```

### **Best Practices**
```
✅ Be specific in your searches
✅ Include year for popular movies
✅ Try multiple search terms
✅ Use /random to discover new movies
✅ Check /popular for trending content
```

## 📈 **Bot Statistics**

The bot tracks (anonymously):
- Total movies in database
- Most popular searches
- Recently added content
- Search success rates

Use `/stats` to see current numbers!

## 🎬 **Enjoy Your Movie Experience!**

This bot makes finding and accessing movies from Telegram channels as easy as searching Netflix. Happy movie hunting! 🍿

---

**Need help?** Use `/help` command or contact the bot administrator.
**Found a bug?** Report it to the admin for quick fixes.
**Have suggestions?** Admins welcome feedback for improvements!
