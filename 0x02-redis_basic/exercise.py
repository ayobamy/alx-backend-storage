#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Any


class Cache:
    """
    redis cache
    """
    def __init__(self):
        """
        store an instance of the
        redis client
        """
        _redis = redis.Redis()
        _redis.flushdb()

    def store(self, data: Any) -> str:
        """
        a method that takes a data
        argument and returns a string
        """
        r = redis.Redis()
        key = str(uuid.uuid4())

        r.set(key, data)

        return key
