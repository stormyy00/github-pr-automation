from .discord import send_discord_notification
import logging
import os
from app.config import repo

ORG_NAME = os.getenv("ORG_NAME", "stormyy00")
REPO_NAME = os.getenv("REPO_NAME", "email-automation")

# Function to auto-merge PR if it passes certain criteria
def auto_merge_pr(pr_number, review_content):
    try:
        pr = repo.get_pull(pr_number)
        
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
        
        # Check if all required checks/workflows have passed
        commit = repo.get_commit(pr.head.sha)
        combined_status = commit.get_combined_status()
        
        # Check commit status
        if combined_status.state != "success":
            message = f"PR #{pr_number} has failing status checks ({combined_status.state})."
            logging.warning(f"⚠️ {message}")
            
            # Send Discord notification
            send_discord_notification(
                title=f"⚠️ PR Merge Blocked: #{pr_number} - {pr.title}",
                description=message,
                color=0xFFAA00  # Amber
            )
            
            return False, message
        
        # Check GitHub Actions workflow runs
        try:
            workflow_runs = list(repo.get_workflow_runs(head_sha=pr.head.sha))
            failing_workflows = [run for run in workflow_runs if run.conclusion not in ["success", "skipped"]]
            
            if failing_workflows:
                workflow_names = ", ".join([run.name for run in failing_workflows])
                message = f"PR #{pr_number} has failing GitHub Actions workflows: {workflow_names}"
                logging.warning(f"⚠️ {message}")
                
                # Send Discord notification
                send_discord_notification(
                    title=f"⚠️ PR Merge Blocked: #{pr_number} - {pr.title}",
                    description=message,
                    color=0xFFAA00  # Amber
                )
                
                return False, message
                
        except Exception as workflow_err:
            logging.warning(f"⚠️ Could not check workflow runs: {workflow_err}")
            # Continue anyway since this might fail in some cases, but log it
        
        # Check specific check runs (like CI tests)
        try:
            check_runs = list(commit.get_check_runs())
            failing_checks = [check for check in check_runs if check.conclusion not in ["success", "skipped", "neutral"]]
            
            if failing_checks:
                check_names = ", ".join([check.name for check in failing_checks])
                message = f"PR #{pr_number} has failing checks: {check_names}"
                logging.warning(f"⚠️ {message}")
                
                # Send Discord notification
                send_discord_notification(
                    title=f"⚠️ PR Merge Blocked: #{pr_number} - {pr.title}",
                    description=message,
                    color=0xFFAA00  # Amber
                )
                
                return False, message
                
        except Exception as check_err:
            logging.warning(f"⚠️ Could not check run status: {check_err}")
            # Continue anyway since this might fail in some cases, but log it
        
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