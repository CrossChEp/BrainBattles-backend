from configs.config import redis
import json


arr = [{
    'fff': 123
}]

arr.append({
    '132': 'FUCK'
})
r = json.loads(redis.get('queue'))
print(r)

# redis.jsonset('queue', Path.rootPath(), obj=arr)
# print(redis.jsonget('queue'))
