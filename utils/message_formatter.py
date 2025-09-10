"""
Message formatting utilities for the Movie Management Bot.
"""

import re
from typing import Dict, Any, Optional
from datetime import datetime


def escape_markdown_v2(text: str) -> str:
    """
    Escape special characters for Telegram MarkdownV2 format.

    Args:
        text: Text to escape

    Returns:
        Escaped text safe for MarkdownV2
    """
    if not text:
        return ""

    # Characters that need escaping in MarkdownV2
    # Order matters - escape backslash first, then others
    escape_chars = [
        ('\\', '\\\\'),  # Backslash first
        ('_', '\\_'),
        ('*', '\\*'),
        ('[', '\\['),
        (']', '\\]'),
        ('(', '\\('),
        (')', '\\)'),
        ('~', '\\~'),
        ('`', '\\`'),
        ('>', '\\>'),
        ('#', '\\#'),
        ('+', '\\+'),
        ('-', '\\-'),
        ('=', '\\='),
        ('|', '\\|'),
        ('{', '\\{'),
        ('}', '\\}'),
        ('.', '\\.'),
        ('!', '\\!')
    ]

    for char, escaped in escape_chars:
        text = text.replace(char, escaped)

    return text


def format_welcome_message(
    user_name: str,
    is_admin: bool = False,
    is_super_admin: bool = False,
    channel_count: int = 0,
    movie_count: int = 0
) -> str:
    """
    Format welcome message based on user type and bot status.
    
    Args:
        user_name: User's first name
        is_admin: Whether user is an admin
        is_super_admin: Whether user is a super admin
        channel_count: Number of connected channels
        movie_count: Number of indexed movies
        
    Returns:
        Formatted welcome message
    """
    # Escape user name for MarkdownV2
    safe_name = escape_markdown_v2(user_name)
    
    if is_admin:
        if channel_count == 0:
            # First-time admin setup
            return f"""🎬 *Welcome to Cognito, {safe_name}\\!*

🎯 *You're an admin\\!* This seems to be your first time setting up the bot\\.

*🚀 Quick Setup Guide:*
1️⃣ Add me to your private movie channels
2️⃣ Give me admin rights in those channels  
3️⃣ Use `/channel add @your_channel` to start monitoring
4️⃣ I'll automatically index all movies for search

*🎬 What I Do:*
• 📊 *Auto\\-index* movies from your channels
• 🔍 *Smart search* with advanced filters
• 🎯 *Direct links* to movie files
• ⚙️ *Admin controls* for management

*Ready to connect your first channel?*
Use: `/channel add @your_movie_channel`

_This message will disappear in 1 hour\\._"""
        else:
            # Existing admin with channels
            return f"""🎬 *Welcome back, {safe_name}\\!*

🎯 *Admin Dashboard Ready*

*📊 Current Status:*
• 📺 *Channels:* {channel_count} connected
• 🎬 *Movies:* {movie_count:,} indexed
• 🔍 *Search:* Fully operational

*🛠️ Admin Commands:*
• `/admin panel` \\- Admin dashboard
• `/channel list` \\- View all channels
• `/stats` \\- Bot statistics
• `/users` \\- User management

*🎬 Your movie collection is ready for users\\!*

_This message will disappear in 1 hour\\._"""
    else:
        # Regular user
        return f"""🎬 *Welcome to Cognito, {safe_name}\\!*

🍿 *Your Personal Movie Search Engine*

*🎯 What I Do:*
• 🔍 *Search* thousands of movies instantly
• 🎬 *Find* movies by title, genre, year, quality
• 📱 *Get* direct download links
• ⭐ *Discover* new movies and classics

*🚀 How to Search:*
• `/search batman 2022` \\- Find Batman movies from 2022
• `/search action 1080p` \\- Find 1080p action movies
• `/search christopher nolan` \\- Find movies by director
• `/movie "The Dark Knight"` \\- Search exact title

*💡 Pro Tips:*
• Use quotes for exact titles
• Add year for popular movies
• Try different keywords if no results

*Ready to find your next movie?*
Try: `/search popular 2023`

_This message will disappear in 1 hour\\._"""


def format_movie_result(movie_data: Dict[str, Any]) -> str:
    """
    Format a single movie search result.
    
    Args:
        movie_data: Movie information dictionary
        
    Returns:
        Formatted movie result text
    """
    title = escape_markdown_v2(movie_data.get('title', 'Unknown Title'))
    year = movie_data.get('year', 'Unknown')
    quality = escape_markdown_v2(movie_data.get('quality', 'Unknown'))
    size = movie_data.get('file_size', 0)
    duration = movie_data.get('duration', 0)
    genre = movie_data.get('genre', [])
    director = escape_markdown_v2(movie_data.get('director', 'Unknown'))
    rating = movie_data.get('rating', 0)
    language = escape_markdown_v2(movie_data.get('language', 'Unknown'))
    channel = escape_markdown_v2(movie_data.get('channel_name', 'Unknown'))
    
    # Format file size
    if size > 1024**3:  # GB
        size_str = f"{size / (1024**3):.1f} GB"
    elif size > 1024**2:  # MB
        size_str = f"{size / (1024**2):.0f} MB"
    else:
        size_str = f"{size / 1024:.0f} KB"
    
    # Format duration
    if duration > 0:
        hours = duration // 60
        minutes = duration % 60
        if hours > 0:
            duration_str = f"{hours}h {minutes}m"
        else:
            duration_str = f"{minutes}m"
    else:
        duration_str = "Unknown"
    
    # Format genre
    if isinstance(genre, list) and genre:
        genre_str = ", ".join([escape_markdown_v2(g) for g in genre[:3]])  # Max 3 genres
    else:
        genre_str = "Unknown"
    
    # Format rating
    rating_str = f"{rating}/10" if rating > 0 else "N/A"
    
    return f"""🎬 *{title}* \\({year}\\)
📊 *Quality:* {quality}
📁 *Size:* {escape_markdown_v2(size_str)} \\| ⏱️ *Duration:* {escape_markdown_v2(duration_str)}
🎭 *Genre:* {genre_str}
🎬 *Director:* {director}
⭐ *Rating:* {escape_markdown_v2(rating_str)}
🗣️ *Language:* {language}
📺 *Source:* {channel}"""


def format_search_results(results: list, query: str, total_found: int = None) -> str:
    """
    Format multiple search results.
    
    Args:
        results: List of movie results
        query: Original search query
        total_found: Total number of results found
        
    Returns:
        Formatted search results text
    """
    if not results:
        safe_query = escape_markdown_v2(query)
        return f"""🔍 *Search Results for:* "{safe_query}"

❌ *No movies found*

*💡 Try:*
• Different keywords
• Check spelling
• Use director or actor names
• Try genre \\+ year \\(e\\.g\\., "action 2023"\\)

*🎬 Popular searches:*
• `/search batman`
• `/search marvel 2023`
• `/search christopher nolan`"""
    
    safe_query = escape_markdown_v2(query)
    result_count = len(results)
    
    if total_found and total_found > result_count:
        header = f"🔍 *Search Results for:* \"{safe_query}\"\n\n📊 *Showing {result_count} of {total_found} results*\n\n"
    else:
        header = f"🔍 *Search Results for:* \"{safe_query}\"\n\n📊 *Found {result_count} result{'s' if result_count != 1 else ''}*\n\n"
    
    # Format each result
    formatted_results = []
    for i, movie in enumerate(results[:5], 1):  # Limit to 5 results per message
        result_text = format_movie_result(movie)
        formatted_results.append(f"*{i}\\.*\n{result_text}")
    
    return header + "\n\n".join(formatted_results)


def format_help_message() -> str:
    """Format help message with all available commands."""
    return """📚 *Cognito Help Guide*

*🔍 Search Commands:*
• `/search <query>` \\- Search for movies
• `/find <query>` \\- Same as search
• `/movie <title>` \\- Search specific title
• `/random` \\- Get random movie
• `/popular` \\- Popular movies
• `/recent` \\- Recently added

*🎯 Search Examples:*
• `/search batman 2022`
• `/search action 1080p`
• `/search christopher nolan`
• `/movie "The Dark Knight"`

*💡 Advanced Search:*
• `title:batman AND year:2022`
• `genre:action AND quality:1080p`
• `director:nolan OR director:tarantino`

*ℹ️ Info Commands:*
• `/start` \\- Welcome message
• `/help` \\- This help message
• `/about` \\- About the bot

*🎬 Ready to find your next movie?*"""


def format_about_message() -> str:
    """Format about message with bot information."""
    return """🎬 *About Cognito*

*🤖 What I Am:*
A powerful movie search bot that helps you find and access movies from connected Telegram channels\\.

*🎯 What I Do:*
• 📊 Index movies from private channels
• 🔍 Provide smart search functionality  
• 🎬 Give direct access to movie files
• ⚡ Update automatically with new content

*🛠️ Built With:*
• Python & Telegram Bot API
• MongoDB for data storage
• Whoosh for fast search
• Unsplash for beautiful posters

*📊 Current Stats:*
• 🎬 Movies indexed: Loading\\.\\.\\.
• 📺 Channels connected: Loading\\.\\.\\.
• 👥 Active users: Loading\\.\\.\\.

*💝 Made with love for movie enthusiasts\\!*

_Version 1\\.0 \\- Built by the Cognito Team_"""


def format_error_message(error_type: str = "general") -> str:
    """
    Format error messages for different scenarios.
    
    Args:
        error_type: Type of error (general, search, network, etc.)
        
    Returns:
        Formatted error message
    """
    error_messages = {
        "general": "🚫 *Oops\\! Something went wrong\\.*\n\nPlease try again in a moment\\.",
        "search": "🔍 *Search Error*\n\nCouldn't perform search right now\\. Please try again\\.",
        "network": "🌐 *Connection Error*\n\nNetwork issue detected\\. Please check your connection\\.",
        "not_found": "❌ *Not Found*\n\nThe requested item couldn't be found\\.",
        "permission": "🔒 *Permission Denied*\n\nYou don't have permission for this action\\.",
        "rate_limit": "⏱️ *Too Many Requests*\n\nPlease wait a moment before trying again\\."
    }
    
    return error_messages.get(error_type, error_messages["general"])
