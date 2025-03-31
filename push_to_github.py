"""
Script to push project to GitHub with updated approach
"""
import os
import subprocess
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# GitHub configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_REPO = os.getenv("GITHUB_REPO").split("/")[1] if "/" in os.getenv("GITHUB_REPO", "") else "ai-agent-coder"

def setup_git_and_push():
    """Set up Git and push project to GitHub"""
    try:
        print("Setting up Git and pushing project to GitHub...")
        
        # Reset any previous git operations
        if os.path.exists(".git"):
            print("Removing existing .git directory...")
            subprocess.run(["rm", "-rf", ".git"], check=True)
        
        # Initialize git
        subprocess.run(["git", "init"], check=True)
        
        # Configure git
        subprocess.run(["git", "config", "user.name", GITHUB_USERNAME], check=True)
        subprocess.run(["git", "config", "user.email", f"{GITHUB_USERNAME}@users.noreply.github.com"], check=True)
        
        # Create .gitignore file
        with open(".gitignore", "w") as f:
            f.write("__pycache__/\n*.py[cod]\n*$py.class\n.env\n*.log\n.DS_Store\ntarget_service_info.json\ntelegram_bot_info.json\n")
        
        # Add remote
        subprocess.run(["git", "remote", "add", "origin", f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"], check=True)
        
        # Create and switch to main branch
        subprocess.run(["git", "checkout", "-b", "main"], check=True)
        
        # Add all files
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit
        subprocess.run(["git", "commit", "-m", "Initial commit of multi-skill super-agent with sanitized credentials"], check=True)
        
        # Pull first to handle any existing content
        try:
            subprocess.run(["git", "pull", "--rebase", "origin", "main"], check=False)
        except:
            print("Pull failed, continuing with push...")
        
        # Force push to GitHub (use with caution, but needed in this case)
        subprocess.run(["git", "push", "-f", "origin", "main"], check=True)
        
        print(f"Project successfully pushed to GitHub: https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error in Git operations: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    """Main function to push project to GitHub"""
    print("Starting project push to GitHub...")
    
    # Verify environment variables
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN not found in environment variables")
        return
    
    if not GITHUB_USERNAME:
        print("Error: GITHUB_USERNAME not found in environment variables")
        return
    
    # Push project to GitHub
    if setup_git_and_push():
        print("\nGitHub repository setup completed successfully!")
        print(f"Repository URL: https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}")
        print("Next steps: Set up Render service with GitHub integration")
    else:
        print("\nFailed to push project to GitHub")

if __name__ == "__main__":
    main()
