"""
Welcome message handler for the Movie Management Bot.
Handles /start and /intro commands with personalized welcome messages.
"""

import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

try:
    from config.admin_manager import is_admin, is_super_admin
except ImportError:
    # Fallback functions if admin manager not available
    async def is_admin(user_id): return False
    async def is_super_admin(user_id): return False

try:
    from config.channel_manager import get_active_channels_count
except ImportError:
    # Fallback function if channel manager not available
    async def get_active_channels_count(): return 0

try:
    from services.unsplash_service import get_welcome_poster_with_fallback
except ImportError:
    # Fallback function if unsplash service not available
    async def get_welcome_poster_with_fallback():
        return {
            'url': 'https://images.unsplash.com/photo-1489599904472-af35ff2c7c3f?w=400',
            'description': 'Movie theater'
        }

try:
    from utils.message_formatter import format_welcome_message
except ImportError:
    # Fallback function if message formatter not available
    def format_welcome_message(*args, **kwargs):
        return "🎬 Welcome to Cognito Movie Bot!"

try:
    from utils.keyboard_builder import build_welcome_keyboard
except ImportError:
    # Fallback function if keyboard builder not available
    def build_welcome_keyboard(is_admin=False):
        return None

logger = logging.getLogger(__name__)


class WelcomeHandler:
    """Handles welcome messages and user onboarding."""
    
    def __init__(self):
        self.welcome_messages = {}  # Track sent welcome messages for auto-deletion
    
    async def handle_start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command with personalized welcome message."""
        try:
            user = update.effective_user
            chat = update.effective_chat
            
            if not user:
                return
            
            logger.info(f"User {user.id} ({user.username}) started the bot")
            
            # Check if user is admin
            user_is_admin = await is_admin(user.id)
            user_is_super_admin = await is_super_admin(user.id)
            
            # Get channel count for admin welcome
            channel_count = await get_active_channels_count() if user_is_admin else 0
            
            # Get random movie poster
            poster_data = await get_welcome_poster_with_fallback()
            
            # Format welcome message based on user type
            welcome_text = await self._format_welcome_message(
                user, user_is_admin, user_is_super_admin, channel_count
            )
            
            # Build keyboard based on user type
            keyboard = self._build_welcome_keyboard(user_is_admin)
            
            # Send welcome message with poster
            message = await context.bot.send_photo(
                chat_id=chat.id,
                photo=poster_data['url'],
                caption=welcome_text,
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=keyboard
            )
            
            # Schedule message deletion after 1 hour (3600 seconds)
            context.job_queue.run_once(
                self._delete_welcome_message,
                3600,  # 1 hour
                data={'chat_id': chat.id, 'message_id': message.message_id},
                name=f"delete_welcome_{chat.id}_{message.message_id}"
            )
            
            # Track message for potential manual deletion
            self.welcome_messages[f"{chat.id}_{message.message_id}"] = {
                'chat_id': chat.id,
                'message_id': message.message_id,
                'user_id': user.id
            }
            
        except Exception as e:
            logger.error(f"Error handling start command: {e}")
            await update.message.reply_text(
                "🚫 Sorry, something went wrong. Please try again later.",
                parse_mode=ParseMode.MARKDOWN_V2
            )
    
    async def handle_intro_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /intro command - alias for /start."""
        await self.handle_start_command(update, context)
    
    async def _format_welcome_message(
        self, 
        user, 
        is_admin_user: bool, 
        is_super_admin_user: bool, 
        channel_count: int
    ) -> str:
        """Format welcome message based on user type and bot status."""
        
        # Escape special characters for MarkdownV2
        def escape_md(text: str) -> str:
            """Escape special characters for MarkdownV2."""
            special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
            for char in special_chars:
                text = text.replace(char, f'\\{char}')
            return text
        
        user_name = escape_md(user.first_name or "User")
        
        if is_admin_user:
            if channel_count == 0:
                # First-time admin setup
                return f"""🎬 *Welcome to Cognito, {user_name}\\!*

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
                # Existing admin
                return f"""🎬 *Welcome back, {user_name}\\!*

🎯 *Admin Dashboard Ready*

*📊 Current Status:*
• 📺 *Channels:* {channel_count} connected
• 🎬 *Movies:* Auto\\-indexing active
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
            return f"""🎬 *Welcome to Cognito, {user_name}\\!*

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
    
    def _build_welcome_keyboard(self, is_admin_user: bool) -> InlineKeyboardMarkup:
        """Build welcome message keyboard based on user type."""
        buttons = []
        
        if not is_admin_user:
            # Non-admin users get support/info buttons
            buttons = [
                [
                    InlineKeyboardButton("📚 Help & Tutorial", callback_data="help_tutorial"),
                    InlineKeyboardButton("🔍 Search Tips", callback_data="search_tips")
                ],
                [
                    InlineKeyboardButton("💬 Support Group", url="https://t.me/cognito_support"),
                    InlineKeyboardButton("📢 Updates Channel", url="https://t.me/cognito_updates")
                ],
                [
                    InlineKeyboardButton("🎬 Try Search", switch_inline_query_current_chat="popular movies")
                ]
            ]
        else:
            # Admin users get admin-focused buttons
            buttons = [
                [
                    InlineKeyboardButton("⚙️ Admin Panel", callback_data="admin_panel"),
                    InlineKeyboardButton("📊 Statistics", callback_data="bot_stats")
                ],
                [
                    InlineKeyboardButton("📺 Manage Channels", callback_data="manage_channels"),
                    InlineKeyboardButton("👥 Manage Users", callback_data="manage_users")
                ]
            ]
        
        return InlineKeyboardMarkup(buttons)
    
    async def _delete_welcome_message(self, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Delete welcome message after 1 hour."""
        try:
            job_data = context.job.data
            chat_id = job_data['chat_id']
            message_id = job_data['message_id']
            
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            
            # Remove from tracking
            message_key = f"{chat_id}_{message_id}"
            if message_key in self.welcome_messages:
                del self.welcome_messages[message_key]
            
            logger.info(f"Deleted welcome message {message_id} from chat {chat_id}")
            
        except Exception as e:
            logger.error(f"Error deleting welcome message: {e}")
    
    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle callback queries from welcome message buttons."""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        user = update.effective_user
        
        if callback_data == "help_tutorial":
            await self._send_help_tutorial(query, context)
        elif callback_data == "search_tips":
            await self._send_search_tips(query, context)
        elif callback_data == "admin_panel":
            await self._send_admin_panel(query, context)
        elif callback_data == "bot_stats":
            await self._send_bot_stats(query, context)
        elif callback_data == "manage_channels":
            await self._send_channel_management(query, context)
        elif callback_data == "manage_users":
            await self._send_user_management(query, context)
    
    async def _send_help_tutorial(self, query, context):
        """Send help tutorial message."""
        help_text = """📚 *How to Use Cognito*

*🔍 Basic Search:*
• `/search <movie name>` \\- Search by title
• `/search <genre>` \\- Search by genre
• `/search <director>` \\- Search by director

*🎯 Advanced Search:*
• `/search batman 2022` \\- Title \\+ year
• `/search action 1080p` \\- Genre \\+ quality
• `/movie "exact title"` \\- Exact match

*💡 Tips:*
• Be specific for better results
• Try different keywords
• Use quotes for exact titles
• Include year for popular movies

*🎬 Ready to search?*"""
        
        await query.edit_message_text(
            text=help_text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back to Welcome", callback_data="back_to_welcome")
            ]])
        )
    
    async def _send_search_tips(self, query, context):
        """Send search tips message."""
        tips_text = """🔍 *Pro Search Tips*

*🎯 For Best Results:*
• Use specific movie titles
• Include release year
• Try director names
• Use genre keywords

*🎬 Examples:*
• `batman 2022` \\- Recent Batman movies
• `nolan sci\\-fi` \\- Nolan sci\\-fi movies
• `marvel 4k` \\- 4K Marvel movies
• `comedy 2023` \\- Recent comedies

*🚀 Advanced Queries:*
• `title:batman AND year:2022`
• `genre:action AND quality:1080p`
• `director:nolan OR director:tarantino`

*Ready to become a search pro?*"""
        
        await query.edit_message_text(
            text=tips_text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back to Welcome", callback_data="back_to_welcome")
            ]])
        )


# Global handler instance
welcome_handler = WelcomeHandler()
