import redis
import os
from dotenv import load_dotenv
import json

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))

# only used as namespace for module, not OOP
class Redis:
    def create_connection():
        return redis.Redis(host=REDIS_HOST, 
                           port=REDIS_PORT)
    
    def enqueue_message(r:redis.Redis, queue_name, message):
        # left push into queue (right pop when dequeue) of the given queue name
        # json dumps translates the dictionary into JSON formatted string to be unmarshalled at GO's backend
        r.lpush(queue_name, json.dumps(message))

    # def dequeue_message(r:redis.Redis, queue_name):
    #     print(r.rpop(queue_name))
        
    
    