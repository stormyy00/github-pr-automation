import logging
import ollama
from .discord import send_discord_notification
from app.config import repo
import os
# Function to analyze PR code using Ollama (Llama 3.2)

ORG_NAME = os.getenv("ORG_NAME", "stormyy00")
REPO_NAME = os.getenv("REPO_NAME", "email-automation")

def analyze_pr(pr_number):
    try:
        pr = repo().get_pull(pr_number)
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
        max_diff_length = 15000
        if len(diff_content) > max_diff_length:
            diff_content = diff_content[:max_diff_length] + "\n\n... [additional changes truncated due to size]"
        
        logging.info(f"Collected diff content for PR #{pr_number} ({len(diff_content)} characters)")
        
        prompt = f"""
            You are an AI code reviewer analyzing GitHub pull requests.
            1. Identify significant logic changes.
            2. Summarize changes concisely in 100 words or less.
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