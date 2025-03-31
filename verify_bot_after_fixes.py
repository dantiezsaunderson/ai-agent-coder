"""
Script to verify Telegram bot functionality after webhook setup
"""
import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def check_webhook_status():
    """Check if the webhook is properly configured"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getWebhookInfo"
    
    try:
        print("Checking webhook status...")
        response = requests.get(url)
        response.raise_for_status()
        
        webhook_info = response.json()
        print(f"Webhook info: {json.dumps(webhook_info, indent=2)}")
        
        if webhook_info["ok"] and webhook_info["result"]["url"]:
            print(f"Webhook is set to: {webhook_info['result']['url']}")
            print(f"Pending updates: {webhook_info['result']['pending_update_count']}")
            return True
        else:
            print("Webhook is not properly configured")
            return False
    
    except Exception as e:
        print(f"Error checking webhook status: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return False

def check_render_service():
    """Check if the Render service is running"""
    url = "https://ai-agent-coder.onrender.com"
    
    try:
        print(f"Checking if Render service is accessible at {url}...")
        response = requests.get(url, timeout=10)
        print(f"Status code: {response.status_code}")
        
        if response.status_code < 500:  # Accept any non-server error response
            print("Render service is accessible")
            return True
        else:
            print("Render service returned a server error")
            return False
    
    except requests.exceptions.RequestException as e:
        print(f"Error accessing Render service: {e}")
        return False

def send_test_message():
    """Send a test message to verify the bot can send messages"""
    # This would normally require a chat_id from a real user
    # For testing purposes, we'll just check if the API is responsive
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"
    
    try:
        print("Verifying bot API access...")
        response = requests.get(url)
        response.raise_for_status()
        
        bot_info = response.json()
        print(f"Bot API is accessible. Bot username: @{bot_info['result']['username']}")
        return True
    
    except Exception as e:
        print(f"Error accessing bot API: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return False

def main():
    """Main function to verify bot functionality after fixes"""
    print("Verifying Telegram bot functionality after webhook setup...")
    
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    # Check webhook status
    webhook_ok = check_webhook_status()
    
    # Check Render service
    render_ok = check_render_service()
    
    # Check bot API access
    api_ok = send_test_message()
    
    # Overall status
    if webhook_ok and render_ok and api_ok:
        print("\nAll checks passed! The Telegram bot should be functioning properly.")
        print("If the bot is still not responding, it may take a few more minutes for the deployment to complete.")
        print("You can also check the logs on Render to see if there are any errors in processing webhook events.")
    else:
        print("\nSome checks failed. The Telegram bot may not be functioning properly.")
        if not webhook_ok:
            print("- The webhook is not properly configured")
        if not render_ok:
            print("- The Render service is not accessible")
        if not api_ok:
            print("- The bot API is not accessible")

if __name__ == "__main__":
    main()
