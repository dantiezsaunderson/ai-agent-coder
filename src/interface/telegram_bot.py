"""
Telegram Bot Interface for Multi-Skill Super-Agent

This module handles the Telegram bot interface for the multi-skill agent,
including command handling and message routing.
"""
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from loguru import logger

from ..utils.config import TELEGRAM_BOT_TOKEN
from ..orchestration.router import AgentRouter

class TelegramInterface:
    """Telegram Bot Interface for the Multi-Skill Super-Agent"""
    
    def __init__(self):
        """Initialize the Telegram bot interface"""
        self.application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        self.router = AgentRouter()
        self._register_handlers()
        logger.info("Telegram bot interface initialized")
    
    def _register_handlers(self):
        """Register command and message handlers"""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("code", self.code_command))
        self.application.add_handler(CommandHandler("image", self.image_command))
        self.application.add_handler(CommandHandler("research", self.research_command))
        
        # Message handler for non-command messages
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command"""
        user = update.effective_user
        welcome_message = (
            f"👋 Hello {user.first_name}!\n\n"
            f"I'm your Multi-Skill Super-Agent, ready to assist you with various tasks.\n\n"
            f"Here are the commands you can use:\n"
            f"• /help - Show available commands and usage\n"
            f"• /code - Generate Python code\n"
            f"• /image - Generate images\n"
            f"• /research - Research topics on the web\n\n"
            f"You can also just send me a message, and I'll try to help!"
        )
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /help command"""
        help_message = (
            "🤖 *Multi-Skill Super-Agent Help*\n\n"
            "*Available Commands:*\n\n"
            "*/code* <description>\n"
            "Generate Python code based on your description.\n"
            "Example: `/code create a function to calculate fibonacci numbers`\n\n"
            "*/image* <description>\n"
            "Generate an image based on your description.\n"
            "Example: `/image a futuristic city with flying cars`\n\n"
            "*/research* <topic>\n"
            "Research a topic on the web and provide a summary.\n"
            "Example: `/research latest developments in quantum computing`\n\n"
            "*General Usage:*\n"
            "You can also send me any message, and I'll try to understand and help you with your request."
        )
        await update.message.reply_text(help_message, parse_mode="Markdown")
    
    async def code_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /code command"""
        if not context.args:
            await update.message.reply_text(
                "Please provide a description of the code you want me to generate.\n"
                "Example: `/code create a function to calculate fibonacci numbers`"
            )
            return
        
        query = " ".join(context.args)
        await update.message.reply_text(f"Generating code for: {query}\nThis may take a moment...")
        
        try:
            # Route to code generation agent
            result = await self.router.route_to_code_agent(query)
            await update.message.reply_text(f"```python\n{result}\n```", parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Error in code generation: {str(e)}")
            await update.message.reply_text(f"Sorry, I encountered an error while generating code: {str(e)}")
    
    async def image_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /image command"""
        if not context.args:
            await update.message.reply_text(
                "Please provide a description of the image you want me to generate.\n"
                "Example: `/image a futuristic city with flying cars`"
            )
            return
        
        query = " ".join(context.args)
        await update.message.reply_text(f"Generating image for: {query}\nThis may take a moment...")
        
        try:
            # Route to image generation agent
            result = await self.router.route_to_image_agent(query)
            # In a real implementation, this would return an image URL or file
            await update.message.reply_text(f"Image generation result: {result}")
        except Exception as e:
            logger.error(f"Error in image generation: {str(e)}")
            await update.message.reply_text(f"Sorry, I encountered an error while generating the image: {str(e)}")
    
    async def research_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /research command"""
        if not context.args:
            await update.message.reply_text(
                "Please provide a topic you want me to research.\n"
                "Example: `/research latest developments in quantum computing`"
            )
            return
        
        query = " ".join(context.args)
        await update.message.reply_text(f"Researching: {query}\nThis may take a moment...")
        
        try:
            # Route to research agent
            result = await self.router.route_to_research_agent(query)
            await update.message.reply_text(result)
        except Exception as e:
            logger.error(f"Error in research: {str(e)}")
            await update.message.reply_text(f"Sorry, I encountered an error while researching: {str(e)}")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle non-command messages"""
        message_text = update.message.text
        
        # Simple intent detection
        if "code" in message_text.lower() or "program" in message_text.lower() or "script" in message_text.lower():
            await self.code_command(update, context.args=[message_text])
        elif "image" in message_text.lower() or "picture" in message_text.lower() or "draw" in message_text.lower():
            await self.image_command(update, context.args=[message_text])
        elif "research" in message_text.lower() or "find" in message_text.lower() or "search" in message_text.lower():
            await self.research_command(update, context.args=[message_text])
        else:
            # General message handling
            await update.message.reply_text(
                "I'm not sure how to help with that specific request. "
                "Try using one of my commands: /help, /code, /image, or /research."
            )
    
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors in the telegram bot"""
        logger.error(f"Exception while handling an update: {context.error}")
        if update and isinstance(update, Update) and update.effective_message:
            await update.effective_message.reply_text(
                "Sorry, I encountered an error while processing your request. Please try again later."
            )
    
    def run(self):
        """Run the Telegram bot"""
        logger.info("Starting Telegram bot")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
