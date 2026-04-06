import json
import os
from typing import Any, Optional, Tuple

from redis import Redis
from redis.exceptions import RedisError


_redis_client: Optional[Redis] = None


def get_redis_client() -> Optional[Redis]:
    global _redis_client

    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        return None

    if _redis_client is None:
        _redis_client = Redis.from_url(redis_url, decode_responses=True)

    return _redis_client


def get_json(key: str) -> Optional[Any]:
    client = get_redis_client()
    if client is None:
        return None

    try:
        value = client.get(key)
    except RedisError:
        return None

    if value is None:
        return None

    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def set_json(key: str, value: Any, ttl_seconds: int) -> None:
    client = get_redis_client()
    if client is None:
        return

    try:
        client.setex(key, ttl_seconds, json.dumps(value))
    except RedisError:
        return


def delete_keys(*keys: str) -> None:
    client = get_redis_client()
    if client is None or not keys:
        return

    try:
        client.delete(*keys)
    except RedisError:
        return


def check_cache() -> Tuple[bool, str]:
    client = get_redis_client()
    if client is None:
        return True, "disabled"

    try:
        client.ping()
        return True, "ok"
    except RedisError as exc:
        return False, str(exc)
