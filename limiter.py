import time
import redis

class TokenBucket:
    def __init__(self, redis_client, client_id: str, rate: float, capacity: int):
        """
        rate: tokens per second (e.g. 5 means 5 requests/second allowed)
        capacity: max bucket size
        """
        self.redis = redis_client
        self.client_id = client_id
        self.rate = rate
        self.capacity = capacity

    def allow(self) -> bool:
        key_tokens = f"{self.client_id}:tokens"
        key_timestamp = f"{self.client_id}:timestamp"

        # Get last values
        tokens = self.redis.get(key_tokens)
        timestamp = self.redis.get(key_timestamp)

        if tokens is None:
            tokens = self.capacity
            timestamp = time.time()
        else:
            tokens = float(tokens)
            timestamp = float(timestamp)

        now = time.time()
        elapsed = now - timestamp

        # Add tokens based on elapsed time
        tokens = min(self.capacity, tokens + elapsed * self.rate)

        allowed = tokens >= 1
        if allowed:
            tokens -= 1  # consume a token

        # Save updated state
        pipe = self.redis.pipeline()
        pipe.set(key_tokens, tokens)
        pipe.set(key_timestamp, now)
        pipe.execute()

        return allowed
