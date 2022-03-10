from configs.config import redis
from rejson import Path
import json


arr = [{
    'fff': 123
}]

arr.append({
    '132': 'FUCK'
})
redis.set('queue', json.dumps(arr))
r = json.loads(redis.get('queue'))
print(r)

# redis.jsonset('queue', Path.rootPath(), obj=arr)
# print(redis.jsonget('queue'))
