"""
Config module for loading environment variables and configuration settings.
"""
import os
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# AI Model API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

# Render Deployment
RENDER_DEPLOY_HOOK = os.getenv("RENDER_DEPLOY_HOOK")
RENDER_API_KEY = os.getenv("RENDER_API_KEY")

# Cryptocurrency API Keys
ETHEREUM_API_KEY = os.getenv("ETHEREUM_API_KEY")
SOLANA_API_KEY = os.getenv("SOLANA_API_KEY")

# Image Generation API Keys
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
MIDJOURNEY_API_KEY = os.getenv("MIDJOURNEY_API_KEY")

# Redis Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./multi_skill_agent.db")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Web Dashboard Configuration
DASHBOARD_ENABLED = os.getenv("DASHBOARD_ENABLED", "false").lower() == "true"
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", 8000))
DASHBOARD_USERNAME = os.getenv("DASHBOARD_USERNAME", "admin")
DASHBOARD_PASSWORD = os.getenv("DASHBOARD_PASSWORD", "change_this_password")

# Configure logger
logger.remove()
logger.add(
    "logs/multi_skill_agent.log",
    rotation="10 MB",
    retention="1 week",
    level=LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
logger.add(
    lambda msg: print(msg),
    level=LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# Validate required configuration
def validate_config():
    """Validate that all required configuration variables are set."""
    required_vars = [
        ("TELEGRAM_BOT_TOKEN", TELEGRAM_BOT_TOKEN),
        ("OPENAI_API_KEY", OPENAI_API_KEY),
    ]
    
    missing_vars = [var_name for var_name, var_value in required_vars if not var_value]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables in your .env file")
        return False
    
    return True

# Get Render owner ID
RENDER_OWNER_ID = "usr-cvk082hr0fns739l4sq0"
