# mypy: ignore-errors
from redis import asyncio as redis

from redis_db.config import REDIS_HOST, REDIS_PORT

redis_default = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True, db=0)
redis_session = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True, db=1)
redis_login = redis.Redis(host=REDIS_HOST, port=int(REDIS_PORT), decode_responses=True, db=2)  # registration or login
