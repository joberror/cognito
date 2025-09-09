# Movie Bot Configuration Guide

Your Media Management Bot is now **optimized specifically for movie files**! Here's what has been configured for the best movie management experience.

## 🎬 **Movie File Extensions (Prioritized)**

### **Primary Formats** (Best Quality/Compatibility)
```env
ALLOWED_EXTENSIONS=mp4,mkv,avi,mov,m4v,wmv,webm,flv,3gp,mpg,mpeg,ts,m2ts
```

| Extension | Quality | Compatibility | Use Case |
|-----------|---------|---------------|----------|
| **mp4** | ✅ Excellent | ✅ Universal | **Best choice** - works everywhere |
| **mkv** | ✅ Excellent | ⚠️ Good | High quality, supports multiple audio/subs |
| **avi** | ⚠️ Good | ✅ Universal | Older format, widely supported |
| **mov** | ✅ Excellent | ⚠️ Apple-focused | High quality, Apple ecosystem |
| **m4v** | ✅ Excellent | ✅ Good | iTunes/Apple format |
| **wmv** | ⚠️ Good | ⚠️ Windows | Microsoft format |
| **webm** | ✅ Good | ✅ Web | Web-optimized, smaller files |
| **flv** | ⚠️ Fair | ⚠️ Limited | Flash video (legacy) |

### **Additional Formats** (Extended Support)
- **3gp** - Mobile/older phones
- **mpg/mpeg** - Standard MPEG format
- **ts/m2ts** - Transport stream (Blu-ray rips)

## 📊 **Movie-Optimized Settings**

### **File Size Limits**
```env
# Development/Local
MAX_FILE_SIZE=5368709120  # 5GB (full movies)

# Render.com Free Tier
MAX_FILE_SIZE=1073741824  # 1GB (trailers/samples)
```

### **Storage Paths**
```env
MEDIA_STORAGE_PATH=./data/movies  # Organized for movies
TEMP_STORAGE_PATH=./data/temp     # Temporary processing
```

### **Movie Thumbnails**
```env
GENERATE_THUMBNAILS=true
THUMBNAIL_SIZE=400,600      # Movie poster aspect ratio (2:3)
THUMBNAIL_QUALITY=90        # High quality for movie posters
```

### **Preview Generation**
```env
GENERATE_PREVIEWS=true      # 30-second movie previews
PREVIEW_DURATION=30         # Preview length in seconds
PREVIEW_QUALITY=720p        # Good quality previews
```

## 🔍 **Movie-Specific Search Features**

### **Enhanced Search Fields**
Your bot now searches across movie-specific metadata:

```python
# Movie metadata fields automatically indexed:
- title, original_title
- description, plot, synopsis  
- genre, genres
- director, directors
- cast, actors
- year, release_date
- country, language, languages
- quality, resolution (720p, 1080p, 4K)
- codec, audio_codec
- imdb_id, tmdb_id
- rating, duration
- channel_name, tags, keywords
```

### **Smart Search Examples**
```python
# Users can search with natural language:
"action movies 2023"           → Finds action movies from 2023
"christopher nolan 1080p"      → Finds Nolan movies in 1080p
"sci-fi thriller"              → Finds sci-fi thriller movies
"tom hanks comedy"             → Finds Tom Hanks comedies
"4k marvel"                    → Finds 4K Marvel movies
```

### **Advanced Query Syntax**
```python
# Power users can use advanced queries:
"title:batman AND year:2022"           # Batman movies from 2022
"genre:action AND quality:1080p"       # 1080p action movies  
"director:nolan OR director:tarantino"  # Movies by specific directors
"rating:[8.0 TO 10.0]"                 # High-rated movies
"duration:[90min TO 180min]"           # Movies 1.5-3 hours long
```

## 🎯 **Movie Search Ranking**

### **Intelligent Ranking System**
Results are automatically ranked by:

1. **Exact Title Match** (+30% score boost)
2. **Video Quality** 
   - 4K/UHD: +20% boost
   - 1080p/Full HD: +10% boost
3. **File Format Preference**
   - MP4: +10% boost (best compatibility)
   - MKV: +5% boost (high quality)
4. **Relevance Score** (base Whoosh scoring)

### **Example Search Results**
```
Query: "batman 1080p"

Results (ranked):
1. "The Batman (2022) 1080p BluRay.mp4" (Score: 0.95)
   ↳ Exact title + 1080p + MP4 format
2. "Batman Begins 1080p.mkv" (Score: 0.87)  
   ↳ Title match + 1080p + MKV format
3. "Batman vs Superman 720p.mp4" (Score: 0.72)
   ↳ Title match + lower quality
```

## 🔧 **Movie Metadata Extraction**

### **Automatic Information Extraction**
```env
EXTRACT_MOVIE_INFO=true     # Extract movie details
EXTRACT_SUBTITLES=true      # Extract subtitle tracks
DETECT_LANGUAGE=true        # Detect audio languages
EXTRACT_CHAPTERS=true       # Extract chapter information
```

### **Extracted Information**
- **Video**: Resolution, codec, bitrate, frame rate
- **Audio**: Codec, channels, language, bitrate
- **Subtitles**: Languages, format (SRT, ASS, etc.)
- **Chapters**: Chapter titles and timestamps
- **Duration**: Exact runtime
- **File Info**: Size, creation date, format

## 🎬 **Movie-Specific Bot Commands**

### **Search Commands**
```
/search batman 2022          # Search for Batman movies from 2022
/find action 1080p           # Find 1080p action movies
/movie "the dark knight"     # Search for specific movie title
/quality 4k                  # Find all 4K movies
/genre comedy                # Find comedy movies
/director nolan              # Find movies by director
```

### **Filter Commands**
```
/filter year:2023            # Movies from 2023
/filter quality:1080p        # 1080p movies only
/filter genre:action         # Action movies only
/filter duration:>120min     # Movies longer than 2 hours
/filter rating:>8.0          # Highly rated movies
```

## 📱 **Free Tier Optimizations**

### **Render.com Specific Settings**
```env
# Optimized for free hosting
MAX_FILE_SIZE=1073741824     # 1GB limit (trailers/samples)
THUMBNAIL_SIZE=300,450       # Smaller thumbnails
GENERATE_PREVIEWS=false      # Disabled to save resources
SEARCH_RESULTS_LIMIT=25      # Fewer results (movies are larger)
```

### **Storage Strategy**
- **Full Movies**: Store links/references only
- **Trailers/Samples**: Can store actual files (under 1GB)
- **Thumbnails**: Generated and cached
- **Metadata**: Stored in MongoDB

## 🎯 **Movie Collection Management**

### **Organization Features**
- **By Genre**: Action, Comedy, Drama, Horror, etc.
- **By Year**: 2023, 2022, 2021, etc.
- **By Quality**: 4K, 1080p, 720p, etc.
- **By Director**: Nolan, Tarantino, Spielberg, etc.
- **By Rating**: IMDb/TMDb ratings
- **By Language**: English, Spanish, French, etc.

### **Collection Statistics**
```python
# Bot can provide statistics:
- Total movies: 1,247
- By quality: 4K (156), 1080p (892), 720p (199)
- By genre: Action (234), Comedy (189), Drama (156)
- By year: 2023 (45), 2022 (78), 2021 (92)
- Total size: 2.4TB
- Average rating: 7.2/10
```

## ✅ **Summary of Movie Optimizations**

### **What's Changed for Movies:**
1. ✅ **File Extensions** - Prioritized movie formats
2. ✅ **File Size** - Increased to 5GB for full movies
3. ✅ **Thumbnails** - Movie poster aspect ratio (2:3)
4. ✅ **Search** - Movie-specific fields and ranking
5. ✅ **Metadata** - Extract movie information automatically
6. ✅ **Storage** - Organized movie directory structure
7. ✅ **Previews** - Generate 30-second movie previews

### **Your Bot Now Excels At:**
- 🎬 **Movie Discovery** - Find movies by title, genre, director, year
- 🔍 **Smart Search** - Handles typos, synonyms, and natural language
- 📊 **Quality Filtering** - Search by resolution and format
- 🎯 **Intelligent Ranking** - Best matches first
- 📱 **Free Hosting** - Optimized for Render.com free tier

**Your movie management bot is now perfectly configured for handling movie collections!** 🍿🎬
