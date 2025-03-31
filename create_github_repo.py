"""
Script to create GitHub repository and push project code
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

def create_github_repository():
    """Create a new GitHub repository"""
    url = "https://api.github.com/user/repos"
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "name": GITHUB_REPO,
        "description": "Multi-skill super-agent with Telegram bot interface",
        "private": False,
        "has_issues": True,
        "has_projects": True,
        "has_wiki": True
    }
    
    try:
        print(f"Creating GitHub repository: {GITHUB_REPO}...")
        response = requests.post(url, headers=headers, json=data)
        
        # If repository already exists, this will fail but we can continue
        if response.status_code == 201:
            print(f"Repository created successfully: {GITHUB_USERNAME}/{GITHUB_REPO}")
            repo_info = response.json()
            print(f"Repository URL: {repo_info['html_url']}")
            return repo_info
        elif response.status_code == 422 and "already exists" in response.text:
            print(f"Repository {GITHUB_USERNAME}/{GITHUB_REPO} already exists, continuing with push...")
            return {"html_url": f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}"}
        else:
            print(f"Failed to create repository: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    
    except Exception as e:
        print(f"Error creating repository: {e}")
        return None

def setup_git_and_push():
    """Set up Git and push project to GitHub"""
    try:
        print("Setting up Git and pushing project to GitHub...")
        
        # Initialize git if not already initialized
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
        
        # Configure git
        subprocess.run(["git", "config", "user.name", GITHUB_USERNAME], check=True)
        subprocess.run(["git", "config", "user.email", f"{GITHUB_USERNAME}@users.noreply.github.com"], check=True)
        
        # Create .gitignore file
        with open(".gitignore", "w") as f:
            f.write("__pycache__/\n*.py[cod]\n*$py.class\n.env\n*.log\n.DS_Store\n")
        
        # Add remote if it doesn't exist
        try:
            subprocess.run(["git", "remote", "add", "origin", f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"], check=True)
        except subprocess.CalledProcessError:
            # Remote might already exist, try setting the URL instead
            subprocess.run(["git", "remote", "set-url", "origin", f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git"], check=True)
        
        # Add all files
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit
        subprocess.run(["git", "commit", "-m", "Initial commit of multi-skill super-agent"], check=True)
        
        # Push to GitHub
        subprocess.run(["git", "push", "-u", "origin", "master"], check=True)
        
        print(f"Project successfully pushed to GitHub: https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error in Git operations: {e}")
        
        # Try with main branch if master failed
        if "master" in str(e):
            try:
                print("Trying with 'main' branch instead of 'master'...")
                subprocess.run(["git", "branch", "-M", "main"], check=True)
                subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
                print(f"Project successfully pushed to GitHub using 'main' branch: https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}")
                return True
            except subprocess.CalledProcessError as e2:
                print(f"Error pushing with 'main' branch: {e2}")
                return False
        return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    """Main function to create GitHub repository and push project"""
    print("Starting GitHub repository creation and project push...")
    
    # Verify environment variables
    if not GITHUB_TOKEN:
        print("Error: GITHUB_TOKEN not found in environment variables")
        return
    
    if not GITHUB_USERNAME:
        print("Error: GITHUB_USERNAME not found in environment variables")
        return
    
    # Create GitHub repository
    repo_info = create_github_repository()
    
    if repo_info:
        # Push project to GitHub
        if setup_git_and_push():
            print("\nGitHub repository setup completed successfully!")
            print(f"Repository URL: {repo_info['html_url']}")
            print("Next steps: Set up Render service with GitHub integration")
        else:
            print("\nFailed to push project to GitHub")
    else:
        print("\nFailed to create GitHub repository")

if __name__ == "__main__":
    main()
