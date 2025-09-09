
import os
import logging
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update, context):
    """Handle /start command"""
    await update.message.reply_text("Welcome to the Media Management Bot!")

def main():
    """Start the bot"""
    if BOT_TOKEN is None:
        print("Error: BOT_TOKEN not found in .env file")
        return
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    
    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()

