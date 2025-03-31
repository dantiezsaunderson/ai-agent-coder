"""
Test script for Telegram Bot Interface

This script tests the functionality of the Telegram bot interface.
"""
import asyncio
import sys
import os
from unittest.mock import AsyncMock, patch
from loguru import logger

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.interface.telegram_bot import TelegramInterface
from telegram import Update
from telegram.ext import ContextTypes

async def test_telegram_commands():
    """Test the Telegram bot command handlers"""
    logger.info("Testing Telegram Bot Command Handlers...")
    
    # Create mock objects
    mock_update = AsyncMock(spec=Update)
    mock_update.effective_user.first_name = "Test User"
    mock_update.message.reply_text = AsyncMock()
    
    mock_context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    
    # Create the Telegram interface with a mocked router
    with patch('src.orchestration.router.AgentRouter') as MockRouter:
        # Configure the mock router
        mock_router = MockRouter.return_value
        mock_router.route_to_code_agent = AsyncMock(return_value="def test_function():\n    return 'Hello, World!'")
        mock_router.route_to_image_agent = AsyncMock(return_value="https://example.com/image.jpg")
        mock_router.route_to_research_agent = AsyncMock(return_value="Research results about the topic.")
        
        # Create the Telegram interface
        telegram_bot = TelegramInterface()
        telegram_bot.router = mock_router
        
        # Test /start command
        logger.info("Testing /start command...")
        await telegram_bot.start_command(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once()
        mock_update.message.reply_text.reset_mock()
        
        # Test /help command
        logger.info("Testing /help command...")
        await telegram_bot.help_command(mock_update, mock_context)
        mock_update.message.reply_text.assert_called_once()
        mock_update.message.reply_text.reset_mock()
        
        # Test /code command
        logger.info("Testing /code command...")
        mock_context.args = ["create", "a", "test", "function"]
        await telegram_bot.code_command(mock_update, mock_context)
        mock_router.route_to_code_agent.assert_called_once()
        mock_update.message.reply_text.assert_called()
        mock_update.message.reply_text.reset_mock()
        mock_router.route_to_code_agent.reset_mock()
        
        # Test /image command
        logger.info("Testing /image command...")
        mock_context.args = ["a", "test", "image"]
        await telegram_bot.image_command(mock_update, mock_context)
        mock_router.route_to_image_agent.assert_called_once()
        mock_update.message.reply_text.assert_called()
        mock_update.message.reply_text.reset_mock()
        mock_router.route_to_image_agent.reset_mock()
        
        # Test /research command
        logger.info("Testing /research command...")
        mock_context.args = ["test", "topic"]
        await telegram_bot.research_command(mock_update, mock_context)
        mock_router.route_to_research_agent.assert_called_once()
        mock_update.message.reply_text.assert_called()
        mock_update.message.reply_text.reset_mock()
        mock_router.route_to_research_agent.reset_mock()
        
        # Test message handling
        logger.info("Testing message handling...")
        mock_update.message.text = "Generate code for a sorting algorithm"
        await telegram_bot.handle_message(mock_update, mock_context)
        mock_update.message.reply_text.assert_called()
        
        logger.info("Telegram Bot Command Handlers tests completed successfully")
        return True

async def run_tests():
    """Run all Telegram bot interface tests"""
    logger.info("Starting tests for Telegram Bot Interface...")
    
    # Create test results directory
    os.makedirs("tests/results", exist_ok=True)
    
    # Run tests
    telegram_test_result = await test_telegram_commands()
    
    # Save test results
    with open("tests/results/telegram_test_results.txt", "w") as f:
        f.write("# Telegram Bot Interface Test Results\n\n")
        f.write(f"Command Handlers Test: {'Passed' if telegram_test_result else 'Failed'}\n\n")
    
    logger.info("Telegram Bot Interface tests completed. Results saved to tests/results/telegram_test_results.txt")

if __name__ == "__main__":
    asyncio.run(run_tests())
