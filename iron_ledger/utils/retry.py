import time
import logging
from functools import wraps
from typing import Callable, Any

from iron_ledger.constants import RateLimits
from iron_ledger.exceptions import ApiError

logger = logging.getLogger(__name__)

def with_retry(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        max_retries = RateLimits.MAX_RETRIES
        assert max_retries >= 1, f"MAX_RETRIES must be >= 1, got {max_retries}"
        base_delay = RateLimits.BASE_DELAY
        
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except ApiError as e:
                # Check for 429 Too Many Requests
                if e.status_code == 429:
                    if attempt == max_retries - 1:
                        logger.error(f"Max retries ({max_retries}) reached for 429 Too Many Requests")
                        raise
                    
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Rate limited (429). Retrying in {delay} seconds (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                else:
                    raise
    return wrapper
