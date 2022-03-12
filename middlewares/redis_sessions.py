import json

from configs import redis


def create_session(table_name: str):
    try:
        json.loads(redis.get(table_name))
    except TypeError:
        redis.set(table_name, json.dumps([]))