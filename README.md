# API Rate Limiter (FastAPI + Redis)

A **production-ready API rate limiter** built using **FastAPI**, **Redis**, and the **Token Bucket algorithm**.

This project demonstrates how to protect your APIs from abuse, ensure fair usage across clients, and control server load.

---

## Table of Contents

* [Overview](#overview)
* [How It Works](#how-it-works)
* [Tech Stack](#tech-stack)
* [Setup & Installation](#setup--installation)
* [Configuration](#configuration)
* [Running the App](#running-the-app)
* [Endpoints](#endpoints)
* [Rate Limiting Details](#rate-limiting-details)
* [Use Cases](#use-cases)
* [Improvements](#improvements)
* [License](#license)

---

## 📝 Overview

This project implements a **Token Bucket rate limiter** as a middleware in FastAPI.

* Clients are identified by IP address (can be swapped for API keys).
* Each client gets a “bucket” of tokens.
* Each request consumes one token.
* Tokens refill at a steady rate over time.
* If the bucket is empty, the client receives a **429 Too Many Requests** error.

---

## How It Works

### Token Bucket Algorithm

* **Capacity**: Maximum number of tokens in the bucket (burst allowance).
* **Rate**: Tokens refilled per second (sustained rate).
* **Allow request**: If a token is available → consume one → request passes.
* **Reject request**: If no tokens available → return `429 Too Many Requests`.

This allows **bursts** of requests while enforcing a **steady long-term limit**.

---

## Tech Stack

* **[FastAPI](https://fastapi.tiangolo.com/)** – API framework
* **[Redis](https://redis.io/)** – In-memory data store for distributed token tracking
* **[Uvicorn](https://www.uvicorn.org/)** – ASGI server for FastAPI
* **[python-dotenv](https://pypi.org/project/python-dotenv/)** – For environment variable management

---

## 🚀 Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/rate_limiter_api.git
cd rate_limiter_api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start Redis

* **Local** (Linux/macOS):

  ```bash
  redis-server
  ```
<!-- * **Docker**:

  ```bash
  docker run -d --name redis -p 6379:6379 redis
  ``` -->

### 4. Create a `.env` file

```ini
REDIS_HOST=<your redis host>
REDIS_PORT=<your redis port>
REDIS_USER=<your redis username>
REDIS_PASS=<your redis password>
```

---

## Configuration

In `main.py`:

```python
RATE = 10 / 60   # refill rate (10 requests per 60 seconds)
CAPACITY = 10    # max tokens per bucket
```

You can adjust these to match your API’s limits:

* Higher **capacity** → larger burst allowed.
* Higher **rate** → more requests per second allowed.

---

## Running the App

Start the FastAPI app:

```bash
uvicorn main:app --reload
```

Visit in your browser:

* [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* [http://127.0.0.1:8000/data](http://127.0.0.1:8000/data)

After exceeding your request quota, you’ll see:

```json
{
  "detail": "Too Many Requests"
}
```

---

## Endpoints

* `GET /` → Basic test endpoint (rate-limited).
* `GET /data` → Example protected API response.

---

## Rate Limiting Details

* **Client Identifier**: IP address (`request.client.host`).
* **Token Storage**: Redis (shared across multiple API servers).
* **Rejections**: HTTP 429 with JSON error.
* **Customizable**: Swap `client_ip` for API keys or JWT claims.

---

## Use Cases

* **Prevent API abuse** – Stop spam, bots, or denial-of-service attempts.
* **Fair usage enforcement** – Ensure each user or API key gets equal access.
* **Cost control** – If you pay per API call, rate limiting saves \$\$\$.
* **Protect downstream services** – Avoid overloading your DB or third-party APIs.
* **Multi-tenant SaaS** – Enforce per-tenant request quotas.

---

## Improvements

Some ideas to extend this project:

* Support multiple strategies (fixed window, sliding window).
* Allow per-endpoint limits (e.g., stricter for `/login`).
* Add headers in responses (`X-RateLimit-Remaining`, `X-RateLimit-Reset`).
* Use API keys or JWT claims instead of IP addresses.
* Integrate with **NGINX/Kong API Gateway** for global enforcement.

---

## License

MIT License. Free to use, modify, and distribute.

---
