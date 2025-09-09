import threading
from firebase_config import send_message

_queue = []
_lock = threading.Lock()

def queue_message(sender_id: str, message_text: str) -> None:
    with _lock:
        _queue.append({"sender": sender_id, "message": message_text})
    print(f"📦 Queued message → {message_text}")

def flush_queue(root, retry_interval: int = 5000) -> None:
    global _queue
    with _lock:
        if _queue:
            print(f"🔄 Attempting to resend {len(_queue)} queued message(s)...")
            for msg in _queue[:]:
                try:
                    send_message(msg["sender"], msg["message"])
                    _queue.remove(msg)
                    print(f"✅ Delivered queued message → {msg['message']}")
                except Exception as e:
                    print(f"❌ Failed to deliver queued message ({msg['message']}): {e}")
    root.after(retry_interval, lambda: flush_queue(root, retry_interval))

def get_queue_size() -> int:
    with _lock:
        return len(_queue)

def clear_queue() -> None:
    global _queue
    with _lock:
        _queue.clear()
    print("🗑️ Offline queue cleared.")