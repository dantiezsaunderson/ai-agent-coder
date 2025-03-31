"""
Script to deploy the multi-skill agent to Render
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
OWNER_ID = "usr-cvk082hr0fns739l4sq0"  # From knowledge module

def create_render_service():
    """Create a new web service on Render"""
    
    # API endpoint for creating services
    url = "https://api.render.com/v1/services"
    
    # Headers with API key
    headers = {
        "Authorization": f"Bearer {RENDER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Service configuration
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
                {"key": "PYTHON_VERSION", "value": "3.10.0"}
            ]
        }
    }
    
    # Make the API request
    try:
        response = requests.post(url, headers=headers, json=service_data)
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

def main():
    """Main function to deploy the service"""
    print("Deploying multi-skill agent to Render...")
    
    if not RENDER_API_KEY:
        print("Error: RENDER_API_KEY not found in environment variables")
        return
    
    if not GITHUB_REPO:
        print("Error: GITHUB_REPO not found in environment variables")
        return
    
    # Create the service
    service_info = create_render_service()
    
    if service_info:
        # Save service info to a file
        with open("render_service_info.json", "w") as f:
            json.dump(service_info, f, indent=2)
        
        print("Deployment initiated. Service information saved to render_service_info.json")
        print("Note: It may take a few minutes for the service to be fully deployed")
    else:
        print("Deployment failed")

if __name__ == "__main__":
    main()
