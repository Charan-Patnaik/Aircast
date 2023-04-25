import redis
from dotenv import load_dotenv
import os

load_dotenv()

client = redis.Redis(host=os.environ.get('REDIST_HOST'))

def islimiter(key, limit):
    req = client.incr(key)
    if req == 1:
        client.expire(key, 3600)
        ttl = 3600
    else:
        ttl = client.ttl(key)
    if req > limit:
        return False
    else:
        return True
    

def register_otp(user_email, otp):
    client.set(user_email, str(otp), ex= 300)

def verify_otp(user_email):
    data = client.get(user_email)

    return data.decode('utf-8')