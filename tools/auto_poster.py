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
import urllib.error

# Ensure tools directory & root directory are in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Force UTF-8 output encoding for Windows & Linux compatibility
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

try:
    from affiliate_engine import load_config, load_products, generate_social_deal_post
except ImportError:
    from tools.affiliate_engine import load_config, load_products, generate_social_deal_post

DEFAULT_BOT_TOKEN = "8925867534:AAHJYAEUAqquXsqEntdoEdBcqd_moBIvR_4"
DEFAULT_CHAT_ID = "@amazonoffershub1"

def send_telegram_message(bot_token, chat_id, message_text):
    config = load_config()
    token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN") or config.get("telegram_bot_token") or DEFAULT_BOT_TOKEN
    chat = chat_id or os.environ.get("TELEGRAM_CHAT_ID") or config.get("telegram_chat_id") or DEFAULT_CHAT_ID

    if not token or not chat:
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
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res = response.read()
            print("[SUCCESS] Deal successfully posted to Telegram Channel!")
            return True
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP Error {e.code}: {e.read().decode('utf-8', errors='ignore')[:300]}")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to post to Telegram: {e}")
        return False

def run_auto_publisher(interval_minutes=2, loop_forever=False):
    config = load_config()
    products = load_products()
    
    print("=" * 60)
    print("END-TO-END AUTOMATED AFFILIATE PUBLISHER STARTED")
    print(f"Tag ID Active: {config.get('store_tag_id')}")
    print(f"Target Telegram Channel: {DEFAULT_CHAT_ID}")
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
