import logging
import requests
import json
from github import Github
from flask import Flask, request, jsonify
from ..utils.discord import send_discord_notification
from ..utils.analyze import analyze_pr
from app.config import repo

class Webhook:
    def github_webhook():
        # Get the event type
        event_type = request.headers.get("X-GitHub-Event")
        
        if not event_type:
            return jsonify({"error": "Not a GitHub webhook event"}), 400
        
        try:
            data = request.json
            
            # Handle pull request events
            if event_type == "pull_request":
                action = data.get("action")
                pr_number = data.get("pull_request", {}).get("number")
                
                if not pr_number:
                    return jsonify({"error": "Missing PR number"}), 400
                
                # Handle PR opened or reopened events
                if action in ["opened", "reopened", "ready_for_review"]:
                    # Notify Discord about new PR
                    pr_title = data.get("pull_request", {}).get("title", "Unknown PR")
                    pr_user = data.get("pull_request", {}).get("user", {}).get("login", "Unknown User")
                    pr_url = data.get("pull_request", {}).get("html_url", "#")
                    
                    send_discord_notification(
                        title=f"🔄 New PR: #{pr_number} - {pr_title}",
                        description=f"A new pull request is ready for review",
                        color=0x5865F2,  # Discord Blurple
                        fields=[
                            {"name": "Repository", "value": f"{repo.ORG_NAME}/{repo.REPO_NAME}", "inline": True},
                            {"name": "Author", "value": pr_user, "inline": True},
                            {"name": "Link", "value": pr_url, "inline": False}
                        ]
                    )
                    
                    # Auto-review the PR
                    review = analyze_pr(pr_number)
                    
                    return jsonify({
                        "status": "success", 
                        "message": f"Processed {action} event for PR #{pr_number}",
                        "review": review
                    })
                    
            return jsonify({"status": "ignored", "message": f"Event {event_type} ignored"})
            
        except Exception as e:
            logging.error(f"❌ Error processing webhook: {e}")
            return jsonify({"error": str(e)}), 500
