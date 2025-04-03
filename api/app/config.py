import os
import logging
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG_NAME = os.getenv("ORG_NAME", "stormyy00")
REPO_NAME = os.getenv("REPO_NAME", "email-automation")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def repo():
    if not GITHUB_TOKEN:
        logging.error("❌ GITHUB_TOKEN is missing! Set it as an environment variable.")
        raise RuntimeError("GITHUB_TOKEN is missing")

    try:
        github = Github(GITHUB_TOKEN)
        repo = github.get_repo(f"{ORG_NAME}/{REPO_NAME}")
        logging.info(f"✅ Connected to GitHub repo: {ORG_NAME}/{REPO_NAME}")
    except Exception as e:
        logging.error(f"❌ Failed to connect to GitHub: {e}")
        raise RuntimeError(f"GitHub connection failed: {e}") 
    return repo