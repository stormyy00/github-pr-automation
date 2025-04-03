from .discord import send_discord_notification
import logging
import os
from app.config import repo

ORG_NAME = os.getenv("ORG_NAME", "stormyy00")
REPO_NAME = os.getenv("REPO_NAME", "email-automation")

# Function to auto-merge PR if it passes certain criteria
def auto_merge_pr(pr_number, review_content):
    try:
        pr = repo().get_pull(pr_number)
        
        # Check if PR is mergeable
        if not pr.mergeable:
            message = f"PR #{pr_number} has merge conflicts and cannot be auto-merged."
            logging.warning(f"⚠️ {message}")
            
            # Send Discord notification
            send_discord_notification(
                title=f"⚠️ PR Merge Failed: #{pr_number} - {pr.title}",
                description=message,
                color=0xFFAA00  # Amber
            )
            
            return False, message
        
        # Check for required approvals
        reviews = pr.get_reviews()
        approval_count = sum(1 for review in reviews if review.state == "APPROVED")
        
        if approval_count < 1:  # Require at least one human approval
            message = f"PR #{pr_number} doesn't have required human approvals."
            logging.warning(f"⚠️ {message}")
            
            # Send Discord notification
            send_discord_notification(
                title=f"⚠️ PR Merge Blocked: #{pr_number} - {pr.title}",
                description=message,
                color=0xFFAA00  # Amber
            )
            
            return False, message
        
        # If the AI review contains negative feedback, don't auto-merge
        if any(term in review_content.lower() for term in ["error", "issue", "unsafe", "not recommended", "don't merge"]):
            message = f"AI review flagged potential issues in PR #{pr_number}."
            logging.warning(f"⚠️ {message}")
            
            # Send Discord notification
            send_discord_notification(
                title=f"⚠️ PR Merge Blocked: #{pr_number} - {pr.title}",
                description=message,
                color=0xFFAA00,  # Amber
                fields=[
                    {"name": "AI Review", "value": review_content[:1000] + ("..." if len(review_content) > 1000 else "")}
                ]
            )
            
            return False, message
        
        # Execute merge
        merge_result = pr.merge(
            commit_title=f"Auto-merge PR #{pr_number}: {pr.title}",
            commit_message=f"Automatically merged via PR automation tool.\n\nAI Review:\n{review_content}",
            merge_method="squash"
        )
        
        if merge_result.merged:
            message = f"PR #{pr_number} was automatically merged."
            logging.info(f"✅ {message}")
            
            # Send Discord notification
            send_discord_notification(
                title=f"✅ PR Merged: #{pr_number} - {pr.title}",
                description=f"PR was automatically merged based on AI review",
                color=0x00FF00,  # Green
                fields=[
                    {"name": "Repository", "value": f"{ORG_NAME}/{REPO_NAME}", "inline": True},
                    {"name": "Author", "value": pr.user.login, "inline": True},
                    {"name": "AI Review", "value": review_content[:2000] + ("..." if len(review_content) > 2000 else "")}
                ]
            )
            
            return True, message
        else:
            message = f"Failed to auto-merge PR #{pr_number}: {merge_result.message}"
            logging.warning(f"⚠️ {message}")
            
            # Send Discord notification
            send_discord_notification(
                title=f"❌ PR Merge Failed: #{pr_number} - {pr.title}",
                description=message,
                color=0xFF0000  # Red
            )
            
            return False, message
            
    except Exception as e:
        message = f"Error during auto-merge of PR #{pr_number}: {e}"
        logging.error(f"❌ {message}")
        
        # Send Discord notification
        send_discord_notification(
            title=f"❌ PR Merge Error: #{pr_number}",
            description=message,
            color=0xFF0000  # Red
        )
        
        return False, message