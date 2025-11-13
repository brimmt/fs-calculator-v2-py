from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)


# This works with ALL SlowAPI versions
def rate_limit_handler(request, exc):
    return {"detail": f"Rate limit exceeded: {exc.detail}"}
