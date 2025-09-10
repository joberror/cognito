
#!/usr/bin/env python3
"""
Cognito - Movie Management Bot
A Telegram bot for managing and searching movie files from private channels.
"""

import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

# Import handlers
from handlers.user.welcome_handler import welcome_handler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


class CognitoBot:
    """Main bot class for Cognito Movie Management Bot."""

    def __init__(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        self.application = None

        if not self.bot_token:
            raise ValueError("BOT_TOKEN not found in environment variables")

    async def setup_handlers(self):
        """Set up all command and callback handlers."""
        logger.info("Setting up bot handlers...")

        # Welcome commands
        self.application.add_handler(CommandHandler("start", welcome_handler.handle_start_command))
        self.application.add_handler(CommandHandler("intro", welcome_handler.handle_intro_command))

        # Callback query handler for inline keyboards
        self.application.add_handler(CallbackQueryHandler(welcome_handler.handle_callback_query))

        # Error handler
        self.application.add_error_handler(self.error_handler)

        logger.info("Bot handlers setup complete")

    async def error_handler(self, update: Update, context) -> None:
        """Handle errors that occur during bot operation."""
        logger.error(f"Exception while handling an update: {context.error}")

        # Try to send error message to user if possible
        if update and update.effective_chat:
            try:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="🚫 Sorry, something went wrong. Please try again later."
                )
            except Exception as e:
                logger.error(f"Failed to send error message to user: {e}")

    async def post_init(self, application):
        """Post initialization hook."""
        logger.info("Bot initialization complete")
        logger.info(f"Bot username: @{application.bot.username}")

    def start_bot(self):
        """Start the bot."""
        logger.info("Starting Cognito Movie Management Bot...")

        # Create application
        self.application = Application.builder().token(self.bot_token).build()

        # Set up handlers (sync version)
        self.setup_handlers_sync()

        # Set post init hook
        self.application.post_init = self.post_init

        # Start the bot
        logger.info("Bot is starting...")
        self.application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )

    def setup_handlers_sync(self):
        """Set up all command and callback handlers (sync version)."""
        logger.info("Setting up bot handlers...")

        # Welcome commands
        self.application.add_handler(CommandHandler("start", welcome_handler.handle_start_command))
        self.application.add_handler(CommandHandler("intro", welcome_handler.handle_intro_command))

        # Callback query handler for inline keyboards
        self.application.add_handler(CallbackQueryHandler(welcome_handler.handle_callback_query))

        # Error handler
        self.application.add_error_handler(self.error_handler)

        logger.info("Bot handlers setup complete")


def main():
    """Main function to start the bot."""
    try:
        bot = CognitoBot()
        bot.start_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == '__main__':
    main()

