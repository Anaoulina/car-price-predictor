import time
from functools import wraps

def retry_on_error(retries=3, delay=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"⚠️ Error in {func.__name__}: {e}")
                    if attempt < retries:
                        print(f"🔄 Retrying ({attempt}/{retries}) in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print(f"❌ Function failed after {retries} attempts.")
            return None
        return wrapper
    return decorator