import redis
import json

import config.secrets 

# only used as namespace for module, not OOP
class Redis:
    def create_connection():
        return redis.Redis(host=config.secrets.REDIS_HOST, 
                           port=config.secrets.REDIS_PORT)
    
    def enqueue_message(r:redis.Redis, queue_name, message):
        # left push into queue (right pop when dequeue) of the given queue name
        # json dumps translates the dictionary into JSON formatted string to be unmarshalled at GO's backend
        r.lpush(queue_name, json.dumps(message))

    def set_key(r:redis.Redis, key, value):
        # set key value pair in redis
        r.set(key, value)
    
    def get_key(r:redis.Redis, key):
        # get value of the key
        return r.get(key)