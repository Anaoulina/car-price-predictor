
import time
import random
import logging
import functools

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

def retry(max_attempts: int = 3, delay: float = 3.0):
 
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    log.warning(f"[retry] {func.__name__} attempt {attempt}/{max_attempts} failed: {exc}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            log.error(f"[retry] {func.__name__} exhausted all {max_attempts} attempts.")
            return None
        return wrapper
    return decorator


def log_step(func):
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        log.info(f"START : {func.__name__}")
        result = func(*args, **kwargs)
        log.info(f"DONE : {func.__name__}")
        return result
    return wrapper


def random_delay(min_s: float = 2.0, max_s: float = 5.0):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            pause = random.uniform(min_s, max_s)
            log.info(f"  Sleeping {pause:.1f}s (human-like delay)")
            time.sleep(pause)
            return result
        return wrapper
    return decorator


def timer(func):
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        log.info(f" {func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper