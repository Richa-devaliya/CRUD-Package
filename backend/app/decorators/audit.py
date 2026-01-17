# backend/app/decorators/audit.py
from functools import wraps
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def audit_log(action: str):
    """
    Decorator to log audit trails for specific actions.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info(f"AUDIT: Starting action '{action}' with args: {args}, kwargs: {kwargs}")
            result = await func(*args, **kwargs)
            logger.info(f"AUDIT: Finished action '{action}'. Result: {result}")
            return result
        return wrapper
    return decorator