from configs.config import redis
from rejson import Path


arr = {
    'simon': 14,
    'daria': 15
}

redis.delete('queue')
redis.jsonset('queue', Path.rootPath(), obj=arr)
print(redis.jsonget('queue'))
