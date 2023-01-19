#!/usr/bin/env python3
"""
Writing strings to Redis
"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    count function calls
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    """
    function call history
    """
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"
    
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function
        """
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output, str(output))

        return method(self, *args, **kwargs)

    return wrapper

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
    
    @count_calls
    @call_history
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
