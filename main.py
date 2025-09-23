from fastapi import FastAPI, Request, HTTPException
import redis
from limiter import TokenBucket

app = FastAPI()

# Connect to Redis (make sure Redis is running locally on default port)
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# Config: 10 requests per minute per client
RATE = 10 / 60   # 10 per 60 seconds = 0.166 tokens/sec
CAPACITY = 10

@app.middleware("http")
async def rate_limiter(request: Request, call_next):
    client_ip = request.client.host
    limiter = TokenBucket(redis_client, client_ip, RATE, CAPACITY)

    if not limiter.allow():
        raise HTTPException(status_code=429, detail="Too Many Requests")

    response = await call_next(request)
    return response

@app.get("/")
def home():
    return {"message": "Hello, you are under rate limiting!"}

@app.get("/data")
def get_data():
    return {"data": "Here’s some protected API response"}
