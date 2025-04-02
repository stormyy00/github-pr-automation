from flask_cors import CORS
import os
import ollama
import logging
import requests
import json
from github import Github
from flask import Flask, request, jsonify

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG_NAME = os.getenv("ORG_NAME", "stormyy00")
REPO_NAME = os.getenv("REPO_NAME", "email-automation")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins="*")

# Check if GitHub Token is provided
if not GITHUB_TOKEN:
    logging.error("❌ GITHUB_TOKEN is missing! Set it as an environment variable.")
    exit(1)

if not DISCORD_WEBHOOK_URL:
    logging.warning("⚠️ DISCORD_WEBHOOK_URL not found. Discord notifications will be disabled.")

try:
    # Initialize GitHub client
    github = Github(GITHUB_TOKEN)
    repo = github.get_repo(f"{ORG_NAME}/{REPO_NAME}")
    logging.info(f"✅ Connected to GitHub repo: {ORG_NAME}/{REPO_NAME}")
except Exception as e:
    logging.error(f"❌ Failed to connect to GitHub: {e}")
    exit(1)

# Function to send Discord notifications
def send_discord_notification(title, description, color=0x5865F2, fields=None):
    if not DISCORD_WEBHOOK_URL:
        logging.warning("Discord notification skipped: No webhook URL configured")
        return False
    
    try:
        # Create Discord embed
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": None  # Discord will use current time
        }
        
        # Add fields if provided
        if fields:
            embed["fields"] = fields
        
        payload = {
            "embeds": [embed]
        }
        
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 204:
            logging.info(f"✅ Discord notification sent: {title}")
            return True
        else:
            logging.error(f"❌ Discord notification failed: {response.status_code} - {response.text}")
            return False
    
    except Exception as e:
        logging.error(f"❌ Error sending Discord notification: {e}")
        return False

# Function to analyze PR code using Ollama (Llama 3.2)
def analyze_pr(pr_number):
    try:
        pr = repo.get_pull(pr_number)
        logging.info(f"Successfully fetched PR #{pr_number}: {pr.title}")
        
        files = list(pr.get_files())  # Convert to list to handle iterator
        logging.info(f"PR #{pr_number} has {len(files)} changed files")
        
        if not files:
            logging.warning(f"⚠️ PR #{pr_number} has no file changes.")
            return "No file changes detected in this PR."
        
        # Get actual diff content rather than just filenames
        diff_content = ""
        for file in files:
            logging.info(f"File: {file.filename}, Has patch: {hasattr(file, 'patch')}, Patch length: {len(file.patch) if hasattr(file, 'patch') and file.patch else 0}")
            diff_content += f"File: {file.filename}\n"
            patch_content = file.patch if hasattr(file, 'patch') and file.patch else 'Binary file or no patch available'
            
            # Limit patch content size to prevent overloading Ollama
            max_patch_length = 2000
            if len(patch_content) > max_patch_length:
                patch_content = patch_content[:max_patch_length] + "... [truncated]"
                
            diff_content += f"Changes: {patch_content}\n\n"
        
        # Limit overall diff size
        max_diff_length = 20000
        if len(diff_content) > max_diff_length:
            diff_content = diff_content[:max_diff_length] + "\n\n... [additional changes truncated due to size]"
        
        logging.info(f"Collected diff content for PR #{pr_number} ({len(diff_content)} characters)")
        
        prompt = f"""
            You are an AI code reviewer analyzing GitHub pull requests.
            1. Identify significant logic changes.
            2. Summarize changes concisely in 100 words or less with a 1000 character limit. 
                - Title: 256 characters
                - Description: 4096 characters
                - Total Embed Size: 6000 characters (sum of all fields)
            3. Provide constructive feedback and highlight potential improvements.
            4. Assess if this PR is safe to merge automatically.
            
            PR Title: {pr.title}
            PR Description: {pr.body if pr.body else 'No description provided'}
            
            File Changes:
            {diff_content}
        """
        
        logging.info(f"Sending prompt to Ollama for PR #{pr_number}")
        
        try:
            # Check if Ollama is available
            model_list = ollama.list()
            logging.info(f"Available models: {model_list}")
            
            # Use a model that's definitely available (if llama3.2 isn't)
            model_to_use = "llama3.2"
            if "llama3.2" not in str(model_list):
                # Use the first available model
                for model_info in model_list.get('models', []):
                    model_to_use = model_info.get('name')
                    if model_to_use:
                        break
                logging.info(f"llama3.2 not found, using {model_to_use} instead")
            
            # AI Review with Ollama
            response = ollama.chat(
                model=model_to_use,
                messages=[{"role": "user", "content": prompt}],
                options={"timeout": 120}  # 2 minute timeout
            )
            
            if not response:
                logging.error("Ollama returned empty response")
                return "Error: Ollama returned empty response"
                
            logging.info(f"Received response from Ollama: {str(response)[:100]}...")
            
            if "message" not in response:
                logging.error(f"Unexpected response format from Ollama: {response}")
                return "Error: Unexpected response format from Ollama"
                
            review_content = response["message"]["content"]
            
            if not review_content:
                logging.error("Ollama returned empty content")
                return "Error: Ollama returned empty content"
                
            logging.info(f"✅ Generated review for PR #{pr_number}: {review_content[:100]}...")
            
            # Send Discord notification about the review
            send_discord_notification(
                title=f"🔍 PR Review: #{pr_number} - {pr.title}",
                description=f"AI review generated for PR #{pr_number}",
                color=0x00AAFF,  # Blue
                fields=[
                    {"name": "Repository", "value": f"{ORG_NAME}/{REPO_NAME}", "inline": True},
                    {"name": "Author", "value": pr.user.login, "inline": True},
                    {"name": "Review", "value": review_content[:1000] + ("..." if len(review_content) > 1000 else "")}
                ]
            )
            
            return review_content
            
        except Exception as ollama_err:
            logging.error(f"❌ Ollama error: {ollama_err}")
            return f"Error with Ollama: {ollama_err}"
            
    except Exception as e:
        logging.error(f"❌ Error analyzing PR #{pr_number}: {e}")
        return f"Error analyzing PR: {e}"

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

# API to fetch PRs
@app.route("/api/pull-requests", methods=["GET"])
def list_prs():
    try:
        pulls = repo.get_pulls(state="open")
        logging.info(f"✅ Retrieved {pulls.totalCount} open PRs.")
        return jsonify([{
            "number": pr.number, 
            "title": pr.title, 
            "user": pr.user.login,
            "created_at": pr.created_at.isoformat(),
            "updated_at": pr.updated_at.isoformat(),
            "mergeable": pr.mergeable
        } for pr in pulls])
    except Exception as e:
        logging.error(f"❌ Error fetching PRs: {e}")
        return jsonify({"error": str(e)}), 500

# API to review a PR
@app.route("/api/review-pr/<int:pr_number>", methods=["GET"])
def review_pr(pr_number):
    review = analyze_pr(pr_number)
    return jsonify({"pr_number": pr_number, "review": review})

# API to auto-merge a PR
@app.route("/api/merge-pr/<int:pr_number>", methods=["POST"])
def merge_pr(pr_number):
    review = analyze_pr(pr_number)
    success, message = auto_merge_pr(pr_number, review)
    
    return jsonify({
        "pr_number": pr_number,
        "success": success,
        "message": message,
        "review": review
    })

# Setup webhook endpoint for GitHub events
@app.route("/api/webhook", methods=["POST"])
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
            if action in ["opened", "reopened", "ready_for_review", "synchronize"]:
                # Notify Discord about new PR
                pr_title = data.get("pull_request", {}).get("title", "Unknown PR")
                pr_user = data.get("pull_request", {}).get("user", {}).get("login", "Unknown User")
                pr_url = data.get("pull_request", {}).get("html_url", "#")
                
                send_discord_notification(
                    title=f"🔄 New PR: #{pr_number} - {pr_title}",
                    description=f"A new pull request is ready for review",
                    color=0x5865F2,  # Discord Blurple
                    fields=[
                        {"name": "Repository", "value": f"{ORG_NAME}/{REPO_NAME}", "inline": True},
                        {"name": "Author", "value": pr_user, "inline": True},
                        {"name": "Link", "value": pr_url, "inline": False}
                    ]
                )
                
                # Auto-review the PR
                review = analyze_pr(pr_number)
                
                # Try to auto-merge if review looks good
                success, message = auto_merge_pr(pr_number, review)
                
                return jsonify({
                    "status": "success", 
                    "message": f"Processed {action} event for PR #{pr_number}",
                    "review": review,
                    "merge_attempted": True,
                    "merge_success": success,
                    "merge_message": message
                })
                
        return jsonify({"status": "ignored", "message": f"Event {event_type} ignored"})
        
    except Exception as e:
        logging.error(f"❌ Error processing webhook: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})

# Run the Flask server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logging.info(f"🚀 Starting Flask server on http://127.0.0.1:{port}/")
    app.run(host="0.0.0.0", port=port)