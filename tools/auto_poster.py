#!/usr/bin/env python3
"""
End-to-End Automated Deal Publisher & Telegram Bot
Tag ID: nick3003-21

This script runs fully automatically:
1. Loads product database & selects hot deals.
2. Formats deal posts with your affiliate link (nick3003-21).
3. Posts automatically to your Telegram Channel via Telegram Bot API.
4. Can run continuously on a timer or scheduled via GitHub Actions / Cron.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from affiliate_engine import load_config, load_products, generate_social_deal_post

# Optional Telegram Environment Variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

def send_telegram_message(bot_token, chat_id, message_text):
    """Sends formatted markdown message to Telegram channel automatically."""
    if not bot_token or not chat_id:
        print("⚠️ Telegram Bot Token or Chat ID not configured.")
        print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables for auto-posting.")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            res = response.read()
            print("✅ Deal successfully posted to Telegram Channel!")
            return True
    except Exception as e:
        print(f"❌ Failed to post to Telegram: {e}")
        return False

def run_auto_publisher(interval_minutes=2, loop_forever=False):
    config = load_config()
    products = load_products()
    
    print("=" * 60)
    print("🚀 END-TO-END AUTOMATED AFFILIATE PUBLISHER STARTED")
    print(f"Tag ID Active: {config.get('store_tag_id')}")
    print(f"Total Products in Queue: {len(products)}")
    print("=" * 60)

    posted_index = 0

    while True:
        if not products:
            print("No products found in database.")
            break
            
        current_product = products[posted_index % len(products)]
        print(f"\n[AUTO-BOT] Processing Product ({posted_index + 1}/{len(products)}): {current_product['title']}")
        
        deal_post = generate_social_deal_post(current_product)
        print("\n--- Formatted Deal Post ---")
        print(deal_post)
        print("---------------------------")

        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, deal_post)
        else:
            print("ℹ️ Simulation mode: Telegram credentials missing. Post printed above.")

        posted_index += 1

        if not loop_forever:
            break
            
        print(f"\n⏳ Waiting {interval_minutes} minutes before posting next deal...")
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    loop_mode = "--loop" in sys.argv
    run_auto_publisher(interval_minutes=60, loop_forever=loop_mode)
