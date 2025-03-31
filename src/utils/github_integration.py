"""
GitHub Integration for Multi-Skill Super-Agent

This module handles GitHub operations like commits, pushes, and repository management.
"""
import os
import requests
from loguru import logger

from ..utils.config import GITHUB_TOKEN, GITHUB_REPO

class GitHubIntegration:
    """GitHub integration for code management and deployment"""
    
    def __init__(self):
        """Initialize the GitHub integration"""
        self.token = GITHUB_TOKEN
        self.repo = GITHUB_REPO
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
        logger.info("GitHub integration initialized")
    
    async def create_file(self, path: str, content: str, message: str = "Add file via API") -> dict:
        """
        Create a file in the repository
        
        Args:
            path: Path to the file in the repository
            content: Content of the file
            message: Commit message
            
        Returns:
            Response from GitHub API
        """
        try:
            url = f"{self.api_base}/repos/{self.repo}/contents/{path}"
            
            # Convert content to base64
            import base64
            content_bytes = content.encode("utf-8")
            content_base64 = base64.b64encode(content_bytes).decode("utf-8")
            
            data = {
                "message": message,
                "content": content_base64
            }
            
            response = requests.put(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            logger.info(f"Created file {path} in repository {self.repo}")
            return response.json()
        
        except Exception as e:
            logger.error(f"Error creating file in GitHub: {str(e)}")
            raise
    
    async def update_file(self, path: str, content: str, message: str = "Update file via API") -> dict:
        """
        Update a file in the repository
        
        Args:
            path: Path to the file in the repository
            content: New content of the file
            message: Commit message
            
        Returns:
            Response from GitHub API
        """
        try:
            # First, get the current file to get its SHA
            url = f"{self.api_base}/repos/{self.repo}/contents/{path}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            sha = response.json()["sha"]
            
            # Convert content to base64
            import base64
            content_bytes = content.encode("utf-8")
            content_base64 = base64.b64encode(content_bytes).decode("utf-8")
            
            data = {
                "message": message,
                "content": content_base64,
                "sha": sha
            }
            
            response = requests.put(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            logger.info(f"Updated file {path} in repository {self.repo}")
            return response.json()
        
        except Exception as e:
            logger.error(f"Error updating file in GitHub: {str(e)}")
            raise
    
    async def create_or_update_file(self, path: str, content: str, message: str = "Update file via API") -> dict:
        """
        Create or update a file in the repository
        
        Args:
            path: Path to the file in the repository
            content: Content of the file
            message: Commit message
            
        Returns:
            Response from GitHub API
        """
        try:
            # Check if file exists
            url = f"{self.api_base}/repos/{self.repo}/contents/{path}"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                # File exists, update it
                return await self.update_file(path, content, message)
            else:
                # File doesn't exist, create it
                return await self.create_file(path, content, message)
        
        except Exception as e:
            logger.error(f"Error creating or updating file in GitHub: {str(e)}")
            raise
    
    async def create_pull_request(self, title: str, body: str, head: str, base: str = "main") -> dict:
        """
        Create a pull request
        
        Args:
            title: Title of the pull request
            body: Body of the pull request
            head: Head branch
            base: Base branch
            
        Returns:
            Response from GitHub API
        """
        try:
            url = f"{self.api_base}/repos/{self.repo}/pulls"
            
            data = {
                "title": title,
                "body": body,
                "head": head,
                "base": base
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            logger.info(f"Created pull request: {title}")
            return response.json()
        
        except Exception as e:
            logger.error(f"Error creating pull request: {str(e)}")
            raise
    
    async def create_branch(self, branch_name: str, source_branch: str = "main") -> dict:
        """
        Create a new branch
        
        Args:
            branch_name: Name of the new branch
            source_branch: Source branch to create from
            
        Returns:
            Response from GitHub API
        """
        try:
            # Get the SHA of the latest commit on the source branch
            url = f"{self.api_base}/repos/{self.repo}/git/refs/heads/{source_branch}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            sha = response.json()["object"]["sha"]
            
            # Create the new branch
            url = f"{self.api_base}/repos/{self.repo}/git/refs"
            
            data = {
                "ref": f"refs/heads/{branch_name}",
                "sha": sha
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            
            logger.info(f"Created branch {branch_name} from {source_branch}")
            return response.json()
        
        except Exception as e:
            logger.error(f"Error creating branch: {str(e)}")
            raise
    
    async def push_project(self, local_dir: str, target_dir: str = "", message: str = "Push project via API") -> list:
        """
        Push a local project directory to the repository
        
        Args:
            local_dir: Local directory to push
            target_dir: Target directory in the repository
            message: Commit message
            
        Returns:
            List of responses from GitHub API
        """
        try:
            responses = []
            
            # Walk through the local directory
            for root, dirs, files in os.walk(local_dir):
                for file in files:
                    # Skip .git files and directories
                    if ".git" in root or file.startswith(".git"):
                        continue
                    
                    # Get the relative path
                    rel_path = os.path.relpath(os.path.join(root, file), local_dir)
                    
                    # Combine with target directory if specified
                    if target_dir:
                        repo_path = os.path.join(target_dir, rel_path)
                    else:
                        repo_path = rel_path
                    
                    # Normalize path separators for GitHub
                    repo_path = repo_path.replace("\\", "/")
                    
                    # Read the file content
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Create or update the file in the repository
                    response = await self.create_or_update_file(
                        path=repo_path,
                        content=content,
                        message=f"{message}: {repo_path}"
                    )
                    
                    responses.append(response)
            
            logger.info(f"Pushed project from {local_dir} to {target_dir or 'repository root'}")
            return responses
        
        except Exception as e:
            logger.error(f"Error pushing project to GitHub: {str(e)}")
            raise
