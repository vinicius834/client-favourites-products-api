import os
import redis

class Cache:
    redis_connection = redis.Redis(host='redis', port=6379, db=0)
    expire = os.environ["CACHE_EXPIRE"]
    current_page_number = 1

    @classmethod
    def save(cls, key, value):
        cls.redis_connection.set(key, value, cls.expire)

    @classmethod
    def get(cls, key):
        value = cls.redis_connection.get(key)
        if not value:
            return None
        return value