import json
import os
import time
from datetime import datetime

RECEIPTS_FILE = 'data/receipts.json'

def load_receipts():
    """Load all receipts from the file."""
    try:
        os.makedirs(os.path.dirname(RECEIPTS_FILE), exist_ok=True)
        if not os.path.exists(RECEIPTS_FILE) or os.path.getsize(RECEIPTS_FILE) == 0:
            return []
        with open(RECEIPTS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading receipts: {e}")
        return []

def save_receipt(receipt):
    """Save a new receipt to the file."""
    try:
        os.makedirs(os.path.dirname(RECEIPTS_FILE), exist_ok=True)
        receipts = load_receipts()
        receipts.append(receipt)
        with open(RECEIPTS_FILE, 'w') as f:
            json.dump(receipts, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving receipt: {e}")
        return False

def generate_receipt(username, cart, total):
    """Generate a receipt object."""
    return {
        'receipt_id': f"REC-{int(time.time())}",
        'username': username,
        'items': cart,
        'total': total,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }