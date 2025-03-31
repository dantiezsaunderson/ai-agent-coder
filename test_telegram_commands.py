"""
Script to test Telegram bot commands directly
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram Bot configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def test_get_updates():
    """Test getUpdates method to see if the bot is receiving messages"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    try:
        print(f"Checking for recent messages using getUpdates...")
        response = requests.get(url)
        response.raise_for_status()
        
        updates = response.json()
        print(f"Response: {json.dumps(updates, indent=2)}")
        
        if updates["ok"] and updates["result"]:
            print(f"Found {len(updates['result'])} recent messages/commands")
            for update in updates["result"]:
                if "message" in update:
                    print(f"Message from {update['message'].get('from', {}).get('username', 'Unknown')}: {update['message'].get('text', 'No text')}")
        else:
            print("No recent messages found. This could be normal if no one has messaged the bot recently.")
        
        return updates
    
    except Exception as e:
        print(f"Error checking updates: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def test_send_message():
    """Test sending a message to verify the bot can send messages"""
    # This would normally require a chat_id, but we'll use a test message to the Telegram API
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getWebhookInfo"
    
    try:
        print(f"Checking webhook configuration...")
        response = requests.get(url)
        response.raise_for_status()
        
        webhook_info = response.json()
        print(f"Webhook info: {json.dumps(webhook_info, indent=2)}")
        
        return webhook_info
    
    except Exception as e:
        print(f"Error checking webhook: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def test_set_webhook():
    """Test setting a webhook for the bot to receive updates"""
    # We'll use the Render URL for the webhook
    render_url = "https://ai-agent-coder.onrender.com/webhook"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    
    data = {
        "url": render_url
    }
    
    try:
        print(f"Setting webhook to {render_url}...")
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        print(f"Result: {json.dumps(result, indent=2)}")
        
        return result
    
    except Exception as e:
        print(f"Error setting webhook: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def main():
    """Main function to test Telegram bot commands"""
    print("Testing Telegram bot commands directly...")
    
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    # Test getUpdates to see if the bot is receiving messages
    test_get_updates()
    
    # Test webhook configuration
    webhook_info = test_send_message()
    
    # If no webhook is set, try setting one
    if webhook_info and webhook_info["ok"] and not webhook_info["result"]["url"]:
        print("No webhook is currently set. Attempting to set a webhook...")
        test_set_webhook()
    
    print("\nTelegram bot testing completed.")
    print("If you're still experiencing issues, the problem might be with the deployed application.")
    print("Check if the application is running properly and if it's configured to handle Telegram webhook events.")

if __name__ == "__main__":
    main()
