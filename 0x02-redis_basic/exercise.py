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
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Any) -> str:
        """
        a method that takes a data
        argument and returns a string
        """
        key = str(uuid.uuid4())

        self._redis.set(key, data)

        return key
