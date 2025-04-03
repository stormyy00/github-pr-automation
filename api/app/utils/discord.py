import logging
import os 
import requests
import json

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

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