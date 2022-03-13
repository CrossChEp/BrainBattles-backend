import json

from configs import redis


def create_session(table_name: str):
    try:
        r = json.loads(redis.get(table_name))
        return r
    except TypeError:
        redis.set(table_name, json.dumps([]))