"""
Main application entry point for Multi-Skill Super-Agent
"""
import asyncio
import os
from loguru import logger

from src.interface.telegram_bot import TelegramInterface
from src.persistence.database import DatabaseManager
from src.utils.config import validate_config

def setup_directories():
    """Create necessary directories if they don't exist"""
    os.makedirs("logs", exist_ok=True)
    logger.info("Directories setup complete")

def main():
    """Main entry point for the application"""
    # Setup directories
    setup_directories()
    
    # Validate configuration
    if not validate_config():
        logger.error("Configuration validation failed. Exiting.")
        return
    
    # Initialize database
    db_manager = DatabaseManager()
    logger.info("Database initialized")
    
    # Initialize and run Telegram bot
    telegram_bot = TelegramInterface()
    logger.info("Starting Telegram bot...")
    telegram_bot.run()

if __name__ == "__main__":
    main()
