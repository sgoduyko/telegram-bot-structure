import os
from typing import Optional

REDIS_HOST: Optional[str] = os.getenv("REDIS_HOST")
REDIS_PORT: Optional[str] = os.getenv("REDIS_PORT")


if REDIS_HOST is None:
    raise ValueError("REDIS_HOST is not set")

if REDIS_PORT is None:
    raise ValueError("REDIS_PORT is not set")
