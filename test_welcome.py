#!/usr/bin/env python3
"""
Test script for the welcome feature.
"""

import asyncio
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_unsplash_service():
    """Test the Unsplash service."""
    try:
        from services.unsplash_service import get_welcome_poster_with_fallback
        
        logger.info("Testing Unsplash service...")
        poster = await get_welcome_poster_with_fallback()
        
        if poster:
            logger.info(f"✅ Poster fetched: {poster['description']}")
            logger.info(f"   URL: {poster['url']}")
            return True
        else:
            logger.error("❌ Failed to fetch poster")
            return False
            
    except Exception as e:
        logger.error(f"❌ Unsplash service error: {e}")
        return False


async def test_message_formatter():
    """Test the message formatter."""
    try:
        from utils.message_formatter import format_welcome_message, escape_markdown_v2
        
        logger.info("Testing message formatter...")
        
        # Test escape function
        test_text = "Hello! This is a test with special chars: _*[]()~`>#+-=|{}.!"
        escaped = escape_markdown_v2(test_text)
        logger.info(f"✅ Text escaped successfully")
        
        # Test welcome message formatting
        welcome_msg = format_welcome_message("TestUser", is_admin=False)
        logger.info(f"✅ Welcome message formatted successfully")
        logger.info(f"   Length: {len(welcome_msg)} characters")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Message formatter error: {e}")
        return False


async def test_keyboard_builder():
    """Test the keyboard builder."""
    try:
        from utils.keyboard_builder import build_welcome_keyboard
        
        logger.info("Testing keyboard builder...")
        
        # Test user keyboard
        user_keyboard = build_welcome_keyboard(is_admin=False)
        logger.info(f"✅ User keyboard built successfully")
        
        # Test admin keyboard
        admin_keyboard = build_welcome_keyboard(is_admin=True)
        logger.info(f"✅ Admin keyboard built successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Keyboard builder error: {e}")
        return False


async def test_welcome_handler():
    """Test the welcome handler."""
    try:
        from handlers.user.welcome_handler import welcome_handler
        
        logger.info("Testing welcome handler...")
        logger.info(f"✅ Welcome handler imported successfully")
        logger.info(f"   Handler type: {type(welcome_handler)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Welcome handler error: {e}")
        return False


async def run_all_tests():
    """Run all welcome feature tests."""
    logger.info("🚀 Starting welcome feature tests...")
    
    tests = [
        ("Unsplash Service", test_unsplash_service),
        ("Message Formatter", test_message_formatter),
        ("Keyboard Builder", test_keyboard_builder),
        ("Welcome Handler", test_welcome_handler),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running {test_name} test...")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n📊 Test Results Summary:")
    logger.info("=" * 40)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {test_name}")
        if result:
            passed += 1
    
    logger.info("=" * 40)
    logger.info(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Welcome feature is ready!")
        return True
    else:
        logger.error(f"💥 {total - passed} tests failed. Please fix issues before proceeding.")
        return False


if __name__ == "__main__":
    asyncio.run(run_all_tests())
