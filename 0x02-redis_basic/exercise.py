#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Union, Optional, Callable


class Cache:
    """
    redis cache
    """
    def __init__(self) -> None:
        """
        store an instance of the
        redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        a method that takes a data
        argument and returns a string
        """
        key = str(uuid.uuid4())

        self._redis.set(key, data)

        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> \
            Union[str, bytes, int, float]:
        """
        a get method that take a key
        string argument and an optional
        Callable argument named fn.
        """
        value = self._redis.get(key)

        if value is not None:
            if fn:
                value = fn(value)
            return value
        else:
            return None

    def get_str(self, val: bytes) -> str:
        """
        automatically parametrize Cache.get
        returns a string
        """
        return str(val, val.decode('utf-8'))

    def get_int(self, val: bytes) -> int:
        """
        automatically parametrize Cache.get
        returns an int
        """
        val = int(val, val.decode('utf-8'))

        return val if val else 0
