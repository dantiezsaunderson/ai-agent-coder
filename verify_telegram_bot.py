"""
Script to verify Telegram bot functionality with the new token
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def verify_bot_info():
    """Verify the bot information using the Telegram API"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    
    try:
        print(f"Verifying bot information using token: {TELEGRAM_BOT_TOKEN}")
        response = requests.get(url)
        response.raise_for_status()
        
        bot_info = response.json()
        print(f"Bot verification successful!")
        print(f"Bot username: @{bot_info['result']['username']}")
        print(f"Bot name: {bot_info['result']['first_name']}")
        print(f"Bot ID: {bot_info['result']['id']}")
        
        # Save bot info to a file
        with open("telegram_bot_info.json", "w") as f:
            json.dump(bot_info, f, indent=2)
        
        print("Bot information saved to telegram_bot_info.json")
        return bot_info
    
    except Exception as e:
        print(f"Error verifying bot: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def set_bot_commands():
    """Set the bot commands using the Telegram API"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setMyCommands"
    
    commands = [
        {"command": "start", "description": "Start the bot and get welcome message"},
        {"command": "help", "description": "Show available commands and usage"},
        {"command": "code", "description": "Generate Python code based on your description"},
        {"command": "image", "description": "Generate an image based on your description"},
        {"command": "research", "description": "Research a topic on the web and provide a summary"}
    ]
    
    try:
        print("Setting bot commands...")
        response = requests.post(url, json={"commands": commands})
        response.raise_for_status()
        
        result = response.json()
        if result["ok"]:
            print("Bot commands set successfully!")
        else:
            print(f"Failed to set bot commands: {result['description']}")
        
        return result
    
    except Exception as e:
        print(f"Error setting bot commands: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def main():
    """Main function to verify bot functionality"""
    print("Verifying Telegram bot functionality...")
    
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    # Verify bot information
    bot_info = verify_bot_info()
    
    if bot_info:
        # Set bot commands
        set_bot_commands()
        
        print("\nTelegram bot verification completed successfully.")
        print("The bot is properly configured with the new token.")
        print("Next steps: Push changes to GitHub and redeploy the application.")
    else:
        print("\nTelegram bot verification failed.")
        print("Please check the token and try again.")

if __name__ == "__main__":
    main()
