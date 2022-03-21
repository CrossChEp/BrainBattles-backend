import json

from configs import redis


def get_redis_table(table_name: str):
    """

    """
    try:
        r = json.loads(redis.get(table_name))
        if not r:
            r = []
        return r
    except TypeError:
        redis.set(table_name, json.dumps([]))