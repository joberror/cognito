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
            try:
                message = await context.bot.send_photo(
                    chat_id=chat.id,
                    photo=poster_data['url'],
                    caption=welcome_text,
                    parse_mode=ParseMode.HTML,  # Use HTML instead of MarkdownV2
                    reply_markup=keyboard
                )
            except Exception as photo_error:
                logger.warning(f"Failed to send photo, sending text message instead: {photo_error}")
                # Fallback to text message without photo
                message = await context.bot.send_message(
                    chat_id=chat.id,
                    text=f"🎬 <b>Movie Poster</b>\n\n{welcome_text}",
                    parse_mode=ParseMode.HTML,  # Use HTML instead of MarkdownV2
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

        # Escape special characters for HTML
        def escape_html(text: str) -> str:
            """Escape special characters for HTML."""
            return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        user_name = escape_html(user.first_name or "User")
        
        if is_admin_user:
            if channel_count == 0:
                # First-time admin setup
                return f"""🎬 <b>Welcome to Cognito, {user_name}!</b>

🎯 <b>You're an admin!</b> This seems to be your first time setting up the bot.

<b>🚀 Quick Setup Guide:</b>
1️⃣ Add me to your private movie channels
2️⃣ Give me admin rights in those channels
3️⃣ Use <code>/channel add @your_channel</code> to start monitoring
4️⃣ I'll automatically index all movies for search

<b>🎬 What I Do:</b>
• 📊 <b>Auto-index</b> movies from your channels
• 🔍 <b>Smart search</b> with advanced filters
• 🎯 <b>Direct links</b> to movie files
• ⚙️ <b>Admin controls</b> for management

<b>Ready to connect your first channel?</b>
Use: <code>/channel add @your_movie_channel</code>

<i>This message will disappear in 1 hour.</i>"""
            else:
                # Existing admin
                return f"""🎬 <b>Welcome back, {user_name}!</b>

🎯 <b>Admin Dashboard Ready</b>

<b>📊 Current Status:</b>
• 📺 <b>Channels:</b> {channel_count} connected
• 🎬 <b>Movies:</b> Auto-indexing active
• 🔍 <b>Search:</b> Fully operational

<b>🛠️ Admin Commands:</b>
• <code>/admin panel</code> - Admin dashboard
• <code>/channel list</code> - View all channels
• <code>/stats</code> - Bot statistics
• <code>/users</code> - User management

<b>🎬 Your movie collection is ready for users!</b>

<i>This message will disappear in 1 hour.</i>"""
        else:
            # Regular user
            return f"""🎬 <b>Welcome to Cognito, {user_name}!</b>

🍿 <b>Your Personal Movie Search Engine</b>

<b>🎯 What I Do:</b>
• 🔍 <b>Search</b> thousands of movies instantly
• 🎬 <b>Find</b> movies by title, genre, year, quality
• 📱 <b>Get</b> direct download links
• ⭐ <b>Discover</b> new movies and classics

<b>🚀 How to Search:</b>
• <code>/search batman 2022</code> - Find Batman movies from 2022
• <code>/search action 1080p</code> - Find 1080p action movies
• <code>/search christopher nolan</code> - Find movies by director
• <code>/movie "The Dark Knight"</code> - Search exact title

<b>💡 Pro Tips:</b>
• Use quotes for exact titles
• Add year for popular movies
• Try different keywords if no results

<b>Ready to find your next movie?</b>
Try: <code>/search popular 2023</code>

<i>This message will disappear in 1 hour.</i>"""
    
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
        help_text = """📚 <b>How to Use Cognito</b>

<b>🔍 Basic Search:</b>
• <code>/search &lt;movie name&gt;</code> - Search by title
• <code>/search &lt;genre&gt;</code> - Search by genre
• <code>/search &lt;director&gt;</code> - Search by director

<b>🎯 Advanced Search:</b>
• <code>/search batman 2022</code> - Title + year
• <code>/search action 1080p</code> - Genre + quality
• <code>/movie "exact title"</code> - Exact match

<b>💡 Tips:</b>
• Be specific for better results
• Try different keywords
• Use quotes for exact titles
• Include year for popular movies

<b>🎬 Ready to search?</b>"""

        await query.edit_message_text(
            text=help_text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back to Welcome", callback_data="back_to_welcome")
            ]])
        )
    
    async def _send_search_tips(self, query, context):
        """Send search tips message."""
        tips_text = """🔍 <b>Pro Search Tips</b>

<b>🎯 For Best Results:</b>
• Use specific movie titles
• Include release year
• Try director names
• Use genre keywords

<b>🎬 Examples:</b>
• <code>batman 2022</code> - Recent Batman movies
• <code>nolan sci-fi</code> - Nolan sci-fi movies
• <code>marvel 4k</code> - 4K Marvel movies
• <code>comedy 2023</code> - Recent comedies

<b>🚀 Advanced Queries:</b>
• <code>title:batman AND year:2022</code>
• <code>genre:action AND quality:1080p</code>
• <code>director:nolan OR director:tarantino</code>

<b>Ready to become a search pro?</b>"""

        await query.edit_message_text(
            text=tips_text,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back to Welcome", callback_data="back_to_welcome")
            ]])
        )


# Global handler instance
welcome_handler = WelcomeHandler()
