"""
Keyboard builder utilities for creating inline keyboards.
"""

import os
from typing import List, Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def build_welcome_keyboard(is_admin: bool = False) -> InlineKeyboardMarkup:
    """
    Build welcome message keyboard based on user type.
    
    Args:
        is_admin: Whether the user is an admin
        
    Returns:
        InlineKeyboardMarkup for welcome message
    """
    if is_admin:
        # Admin keyboard - focus on management
        buttons = [
            [
                InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel"),
                InlineKeyboardButton("📊 Statistics", callback_data="bot_stats")
            ],
            [
                InlineKeyboardButton("📺 Manage Channels", callback_data="manage_channels"),
                InlineKeyboardButton("👥 Manage Users", callback_data="manage_users")
            ],
            [
                InlineKeyboardButton("🔍 Test Search", switch_inline_query_current_chat="test search")
            ]
        ]
    else:
        # Regular user keyboard - focus on usage and support
        support_link = os.getenv('SUPPORT_LINK', 'https://t.me/cognito_support')
        group_link = os.getenv('GROUP_LINK', 'https://t.me/cognito_group')
        
        buttons = [
            [
                InlineKeyboardButton("📚 Help & Tutorial", callback_data="help_tutorial"),
                InlineKeyboardButton("🔍 Search Tips", callback_data="search_tips")
            ],
            [
                InlineKeyboardButton("💬 Support Group", url=support_link),
                InlineKeyboardButton("📢 Updates Channel", url=group_link)
            ],
            [
                InlineKeyboardButton("🎬 Try Search", switch_inline_query_current_chat="popular movies")
            ]
        ]
    
    return InlineKeyboardMarkup(buttons)


def build_search_results_keyboard(
    results: List[dict], 
    current_page: int = 1, 
    total_pages: int = 1,
    query: str = ""
) -> InlineKeyboardMarkup:
    """
    Build keyboard for search results with download links and navigation.
    
    Args:
        results: List of movie results for current page
        current_page: Current page number
        total_pages: Total number of pages
        query: Original search query
        
    Returns:
        InlineKeyboardMarkup for search results
    """
    buttons = []
    
    # Download buttons for each result (max 5 per page)
    for i, movie in enumerate(results[:5], 1):
        file_id = movie.get('file_id', '')
        title = movie.get('title', f'Movie {i}')
        
        # Truncate title if too long for button
        if len(title) > 25:
            title = title[:22] + "..."
        
        buttons.append([
            InlineKeyboardButton(
                f"📥 {i}. {title}",
                callback_data=f"download_{file_id}"
            )
        ])
    
    # Navigation buttons if multiple pages
    if total_pages > 1:
        nav_buttons = []
        
        if current_page > 1:
            nav_buttons.append(
                InlineKeyboardButton("⬅️ Previous", callback_data=f"page_{current_page-1}_{query}")
            )
        
        nav_buttons.append(
            InlineKeyboardButton(f"{current_page}/{total_pages}", callback_data="page_info")
        )
        
        if current_page < total_pages:
            nav_buttons.append(
                InlineKeyboardButton("Next ➡️", callback_data=f"page_{current_page+1}_{query}")
            )
        
        buttons.append(nav_buttons)
    
    # Additional action buttons
    action_buttons = [
        InlineKeyboardButton("🔍 New Search", switch_inline_query_current_chat=""),
        InlineKeyboardButton("🎲 Random", callback_data="random_movie")
    ]
    buttons.append(action_buttons)
    
    return InlineKeyboardMarkup(buttons)


def build_movie_detail_keyboard(movie_data: dict) -> InlineKeyboardMarkup:
    """
    Build keyboard for individual movie details.
    
    Args:
        movie_data: Movie information dictionary
        
    Returns:
        InlineKeyboardMarkup for movie details
    """
    buttons = []
    
    # Main download button
    file_id = movie_data.get('file_id', '')
    if file_id:
        buttons.append([
            InlineKeyboardButton("📥 Download Movie", callback_data=f"download_{file_id}")
        ])
    
    # Additional info buttons
    info_buttons = []
    
    # IMDb link if available
    imdb_id = movie_data.get('imdb_id')
    if imdb_id:
        info_buttons.append(
            InlineKeyboardButton("🎬 IMDb", url=f"https://www.imdb.com/title/{imdb_id}/")
        )
    
    # TMDb link if available
    tmdb_id = movie_data.get('tmdb_id')
    if tmdb_id:
        info_buttons.append(
            InlineKeyboardButton("📊 TMDb", url=f"https://www.themoviedb.org/movie/{tmdb_id}")
        )
    
    if info_buttons:
        buttons.append(info_buttons)
    
    # Action buttons
    action_buttons = [
        InlineKeyboardButton("🔍 Similar Movies", callback_data=f"similar_{movie_data.get('genre', [''])[0]}"),
        InlineKeyboardButton("🎲 Random", callback_data="random_movie")
    ]
    buttons.append(action_buttons)
    
    # Back button
    buttons.append([
        InlineKeyboardButton("🔙 Back to Search", callback_data="back_to_search")
    ])
    
    return InlineKeyboardMarkup(buttons)


def build_admin_panel_keyboard() -> InlineKeyboardMarkup:
    """Build admin panel main keyboard."""
    buttons = [
        [
            InlineKeyboardButton("📺 Channels", callback_data="admin_channels"),
            InlineKeyboardButton("👥 Users", callback_data="admin_users")
        ],
        [
            InlineKeyboardButton("📊 Statistics", callback_data="admin_stats"),
            InlineKeyboardButton("🔧 Settings", callback_data="admin_settings")
        ],
        [
            InlineKeyboardButton("🗄️ Database", callback_data="admin_database"),
            InlineKeyboardButton("📝 Logs", callback_data="admin_logs")
        ],
        [
            InlineKeyboardButton("🔙 Back to Welcome", callback_data="back_to_welcome")
        ]
    ]
    
    return InlineKeyboardMarkup(buttons)


def build_channel_management_keyboard(channels: List[dict]) -> InlineKeyboardMarkup:
    """
    Build keyboard for channel management.
    
    Args:
        channels: List of channel information
        
    Returns:
        InlineKeyboardMarkup for channel management
    """
    buttons = []
    
    # Channel list (max 5 per page)
    for channel in channels[:5]:
        channel_name = channel.get('channel_name', 'Unknown')
        channel_id = channel.get('channel_id', '')
        is_active = channel.get('is_active', False)
        
        status_emoji = "✅" if is_active else "❌"
        
        buttons.append([
            InlineKeyboardButton(
                f"{status_emoji} {channel_name}",
                callback_data=f"channel_info_{channel_id}"
            )
        ])
    
    # Management buttons
    management_buttons = [
        InlineKeyboardButton("➕ Add Channel", callback_data="add_channel"),
        InlineKeyboardButton("🔄 Refresh", callback_data="refresh_channels")
    ]
    buttons.append(management_buttons)
    
    # Back button
    buttons.append([
        InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_panel")
    ])
    
    return InlineKeyboardMarkup(buttons)


def build_user_management_keyboard(users: List[dict]) -> InlineKeyboardMarkup:
    """
    Build keyboard for user management.
    
    Args:
        users: List of user information
        
    Returns:
        InlineKeyboardMarkup for user management
    """
    buttons = []
    
    # User list (max 5 per page)
    for user in users[:5]:
        username = user.get('username', f"User {user.get('user_id', 'Unknown')}")
        user_id = user.get('user_id', '')
        is_admin = user.get('is_admin', False)
        
        status_emoji = "👑" if is_admin else "👤"
        
        buttons.append([
            InlineKeyboardButton(
                f"{status_emoji} {username}",
                callback_data=f"user_info_{user_id}"
            )
        ])
    
    # Management buttons
    management_buttons = [
        InlineKeyboardButton("👑 Promote User", callback_data="promote_user"),
        InlineKeyboardButton("👤 Demote User", callback_data="demote_user")
    ]
    buttons.append(management_buttons)
    
    # Back button
    buttons.append([
        InlineKeyboardButton("🔙 Back to Admin", callback_data="admin_panel")
    ])
    
    return InlineKeyboardMarkup(buttons)


def build_confirmation_keyboard(action: str, item_id: str = "") -> InlineKeyboardMarkup:
    """
    Build confirmation keyboard for destructive actions.
    
    Args:
        action: Action to confirm
        item_id: ID of item being acted upon
        
    Returns:
        InlineKeyboardMarkup for confirmation
    """
    buttons = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_{action}_{item_id}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{action}")
        ]
    ]
    
    return InlineKeyboardMarkup(buttons)


def build_help_keyboard() -> InlineKeyboardMarkup:
    """Build help message keyboard."""
    buttons = [
        [
            InlineKeyboardButton("🔍 Search Guide", callback_data="help_search"),
            InlineKeyboardButton("💡 Pro Tips", callback_data="help_tips")
        ],
        [
            InlineKeyboardButton("🎬 Try Search", switch_inline_query_current_chat="batman"),
            InlineKeyboardButton("🎲 Random Movie", callback_data="random_movie")
        ],
        [
            InlineKeyboardButton("🔙 Back to Welcome", callback_data="back_to_welcome")
        ]
    ]
    
    return InlineKeyboardMarkup(buttons)


def build_back_keyboard(callback_data: str = "back_to_welcome") -> InlineKeyboardMarkup:
    """
    Build simple back button keyboard.
    
    Args:
        callback_data: Callback data for back button
        
    Returns:
        InlineKeyboardMarkup with back button
    """
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🔙 Back", callback_data=callback_data)
    ]])
