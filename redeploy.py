"""
Script to update GitHub repository and trigger redeployment
"""
import os
import requests
import json
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
RENDER_DEPLOY_HOOK = os.getenv("RENDER_DEPLOY_HOOK")

def push_changes_to_github():
    """Push the updated token to GitHub repository"""
    try:
        print("Pushing changes to GitHub repository...")
        
        # Initialize git if not already initialized
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", f"https://{GITHUB_TOKEN}@github.com/{GITHUB_REPO}.git"], check=True)
        
        # Configure git
        subprocess.run(["git", "config", "user.name", "Deployment Bot"], check=True)
        subprocess.run(["git", "config", "user.email", "deployment@example.com"], check=True)
        
        # Add changes
        subprocess.run(["git", "add", ".env.template"], check=True)
        
        # Commit changes
        subprocess.run(["git", "commit", "-m", "Update Telegram bot token"], check=True)
        
        # Push changes
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
        
        print("Changes pushed to GitHub successfully!")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error pushing changes to GitHub: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def trigger_redeployment():
    """Trigger redeployment using the Render deploy hook"""
    try:
        print("Triggering redeployment on Render...")
        
        response = requests.post(RENDER_DEPLOY_HOOK)
        response.raise_for_status()
        
        print(f"Redeployment triggered successfully! Status code: {response.status_code}")
        return True
    
    except Exception as e:
        print(f"Error triggering redeployment: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return False

def main():
    """Main function to update GitHub and trigger redeployment"""
    print("Starting redeployment process...")
    
    # Verify environment variables
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN not found in environment variables")
        return
    
    if not GITHUB_REPO:
        print("Error: GITHUB_REPO not found in environment variables")
        return
    
    if not RENDER_DEPLOY_HOOK:
        print("Error: RENDER_DEPLOY_HOOK not found in environment variables")
        return
    
    # Push changes to GitHub
    if push_changes_to_github():
        # Trigger redeployment
        if trigger_redeployment():
            print("\nRedeployment process completed successfully!")
            print("The application should be updated with the new Telegram bot token shortly.")
            print("You can verify the deployment status on the Render dashboard.")
        else:
            print("\nFailed to trigger redeployment.")
            print("Please check the Render deploy hook and try again.")
    else:
        print("\nFailed to push changes to GitHub.")
        print("Attempting to trigger redeployment directly...")
        
        # Try to trigger redeployment directly
        if trigger_redeployment():
            print("\nRedeployment triggered successfully despite GitHub push failure.")
            print("The application should be updated with the new Telegram bot token shortly.")
        else:
            print("\nAll redeployment attempts failed.")
            print("Please check your GitHub and Render configurations.")

if __name__ == "__main__":
    main()
