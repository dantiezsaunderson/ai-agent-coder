"""
Script to check deployment status on Render
"""
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Render API configuration
RENDER_API_KEY = os.getenv("RENDER_API_KEY")

def check_services():
    """Check existing Render services"""
    url = "https://api.render.com/v1/services"
    headers = {
        "Authorization": f"Bearer {RENDER_API_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        services = response.json()
        
        print(f"Found {len(services)} services")
        print("Looking for multi-skill-agent or ai-agent-coder service...")
        
        found = False
        for service in services:
            service_info = service['service']
            service_name = service_info['name']
            service_url = service_info['serviceDetails'].get('url', 'N/A')
            
            print(f"Service name: {service_name}, URL: {service_url}")
            
            if service_name in ['multi-skill-agent', 'ai-agent-coder']:
                found = True
                print(f"\nFound target service: {service_name}")
                print(f"Service URL: {service_url}")
                print(f"Dashboard URL: {service_info['dashboardUrl']}")
                print(f"Service type: {service_info['type']}")
                print(f"Status: {'Deployed' if service_info['suspended'] != 'suspended' else 'Suspended'}")
                
                # Save service info to a file
                with open("target_service_info.json", "w") as f:
                    json.dump(service_info, f, indent=2)
                
                print("Service information saved to target_service_info.json")
        
        if not found:
            print("\nTarget service not found in the list of services.")
            print("The deploy hook may have triggered a deployment to an existing service with a different name.")
            print("Please check your Render dashboard at https://dashboard.render.com/ for the latest deployments.")
        
        return services
    
    except Exception as e:
        print(f"Error checking services: {e}")
        return None

if __name__ == "__main__":
    print("Checking deployment status on Render...")
    services = check_services()
