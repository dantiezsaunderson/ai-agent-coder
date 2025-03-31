"""
Script to deploy the multi-skill agent to Render with more detailed error handling
"""
import requests
import json
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Render API configuration
RENDER_API_KEY = os.getenv("RENDER_API_KEY")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OWNER_ID = "usr-cvk082hr0fns739l4sq0"  # From knowledge module

def get_render_services():
    """Get list of existing Render services"""
    url = "https://api.render.com/v1/services"
    headers = {
        "Authorization": f"Bearer {RENDER_API_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting services: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def create_render_service():
    """Create a new web service on Render"""
    
    # API endpoint for creating services
    url = "https://api.render.com/v1/services"
    
    # Headers with API key
    headers = {
        "Authorization": f"Bearer {RENDER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Service configuration - more detailed for troubleshooting
    service_data = {
        "type": "web_service",  # Using web_service as per user preference
        "name": "multi-skill-agent",
        "ownerId": OWNER_ID,
        "repo": f"https://github.com/{GITHUB_REPO}",
        "branch": "main",
        "autoDeploy": "yes",
        "serviceDetails": {
            "env": "python",
            "buildCommand": "pip install -r requirements.txt",
            "startCommand": "python main.py",
            "envVars": [
                {"key": "PYTHON_VERSION", "value": "3.10.0"},
                {"key": "TELEGRAM_BOT_TOKEN", "value": os.getenv("TELEGRAM_BOT_TOKEN")},
                {"key": "OPENAI_API_KEY", "value": os.getenv("OPENAI_API_KEY")},
                {"key": "CLAUDE_API_KEY", "value": os.getenv("CLAUDE_API_KEY")},
                {"key": "DEEPSEEK_API_KEY", "value": os.getenv("DEEPSEEK_API_KEY")},
                {"key": "GITHUB_TOKEN", "value": os.getenv("GITHUB_TOKEN")},
                {"key": "GITHUB_REPO", "value": os.getenv("GITHUB_REPO")},
                {"key": "RENDER_API_KEY", "value": os.getenv("RENDER_API_KEY")},
                {"key": "RENDER_DEPLOY_HOOK", "value": os.getenv("RENDER_DEPLOY_HOOK")}
            ]
        }
    }
    
    # Print request details for debugging (without sensitive info)
    print(f"Sending request to: {url}")
    print(f"Service name: {service_data['name']}")
    print(f"Service type: {service_data['type']}")
    print(f"Owner ID: {service_data['ownerId']}")
    print(f"Repository: {service_data['repo']}")
    
    # Make the API request
    try:
        response = requests.post(url, headers=headers, json=service_data)
        
        # Print response status for debugging
        print(f"Response status code: {response.status_code}")
        
        # Try to parse response as JSON
        try:
            response_json = response.json()
            print(f"Response body: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Response body: {response.text}")
        
        response.raise_for_status()
        
        # Parse the response
        service_info = response.json()
        print(f"Service created successfully: {service_info['service']['name']}")
        print(f"Service URL: {service_info['service']['serviceDetails']['url']}")
        
        return service_info
    
    except requests.exceptions.RequestException as e:
        print(f"Error creating service: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None

def trigger_deploy_hook():
    """Trigger deployment using the deploy hook"""
    deploy_hook = os.getenv("RENDER_DEPLOY_HOOK")
    
    if not deploy_hook:
        print("Error: RENDER_DEPLOY_HOOK not found in environment variables")
        return False
    
    try:
        print(f"Triggering deploy hook...")
        response = requests.post(deploy_hook)
        response.raise_for_status()
        
        print(f"Deploy hook triggered successfully: {response.status_code}")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"Error triggering deploy hook: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return False

def main():
    """Main function to deploy the service"""
    print("Deploying multi-skill agent to Render...")
    
    if not RENDER_API_KEY:
        print("Error: RENDER_API_KEY not found in environment variables")
        return
    
    if not GITHUB_REPO:
        print("Error: GITHUB_REPO not found in environment variables")
        return
    
    # First, check existing services
    print("Checking existing services...")
    services = get_render_services()
    
    if services:
        print(f"Found {len(services)} existing services")
        
        # Check if our service already exists
        for service in services:
            if service.get('name') == 'multi-skill-agent':
                print(f"Service 'multi-skill-agent' already exists with ID: {service.get('id')}")
                print(f"Service URL: {service.get('serviceDetails', {}).get('url', 'Unknown')}")
                
                # Try to trigger deploy hook instead of creating new service
                print("Triggering deployment using deploy hook instead of creating new service...")
                if trigger_deploy_hook():
                    print("Deployment initiated via deploy hook")
                    print("Note: It may take a few minutes for the service to be fully deployed")
                    return
                else:
                    print("Failed to trigger deployment via deploy hook")
                    return
    
    # If we get here, try to create a new service
    print("Creating new service...")
    service_info = create_render_service()
    
    if service_info:
        # Save service info to a file
        with open("render_service_info.json", "w") as f:
            json.dump(service_info, f, indent=2)
        
        print("Deployment initiated. Service information saved to render_service_info.json")
        print("Note: It may take a few minutes for the service to be fully deployed")
    else:
        print("Deployment failed. Trying alternative approach with deploy hook...")
        if trigger_deploy_hook():
            print("Deployment initiated via deploy hook")
            print("Note: It may take a few minutes for the service to be fully deployed")
        else:
            print("All deployment attempts failed")

if __name__ == "__main__":
    main()
