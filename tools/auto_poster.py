#!/usr/bin/env python3
"""
End-to-End Automated Deal Publisher & Telegram Bot
Tag ID: nick3003-21
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse

# Force UTF-8 output encoding for Windows Command Prompt compatibility
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from affiliate_engine import load_config, load_products, generate_social_deal_post

def send_telegram_message(bot_token, chat_id, message_text):
    """Sends formatted markdown message to Telegram channel automatically."""
    config = load_config()
    token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN") or config.get("telegram_bot_token", "")
    chat = chat_id or os.environ.get("TELEGRAM_CHAT_ID") or config.get("telegram_chat_id", "")

    if not token or not chat or "YOUR_BOT_TOKEN" in token:
        print("[WARNING] Telegram Bot Token or Chat ID not configured.")
        return False
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat,
        "text": message_text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            res = response.read()
            print("[SUCCESS] Deal successfully posted to Telegram Channel!")
            return True
    except Exception as e:
        print(f"[ERROR] Failed to post to Telegram: {e}")
        return False

def run_auto_publisher(interval_minutes=2, loop_forever=False):
    config = load_config()
    products = load_products()
    
    print("=" * 60)
    print("END-TO-END AUTOMATED AFFILIATE PUBLISHER STARTED")
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

        print("[AUTO-BOT] Sending deal to Telegram...")
        success = send_telegram_message(None, None, deal_post)
        
        if success:
            print("[AUTO-BOT] Telegram Message Sent Successfully!")

        posted_index += 1

        if not loop_forever:
            break
            
        print(f"\n[WAITING] {interval_minutes} minutes before posting next deal...")
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    loop_mode = "--loop" in sys.argv
    run_auto_publisher(interval_minutes=2, loop_forever=loop_mode)
