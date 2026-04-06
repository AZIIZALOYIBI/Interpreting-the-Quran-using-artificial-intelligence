"""
Async worker for processing AI requests from Redis queue.
"""
import asyncio
import json
import os
import logging
from quran_solver import QuranSolver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
QUEUE_NAME = "quran_requests"
RESULTS_PREFIX = "result:"


async def process_request(solver: QuranSolver, request_data: dict) -> dict:
    question = request_data.get("question", "")
    category = request_data.get("category")
    return solver.get_quran_solution(question, category)


async def main():
    try:
        import redis.asyncio as aioredis
        r = await aioredis.from_url(REDIS_URL)
        solver = QuranSolver()
        logger.info("Worker started. Listening for requests...")

        while True:
            try:
                item = await r.blpop(QUEUE_NAME, timeout=5)
                if item:
                    _, data_bytes = item
                    request_data = json.loads(data_bytes)
                    request_id = request_data.get("id", "unknown")
                    logger.info(f"Processing request: {request_id}")

                    result = await process_request(solver, request_data)
                    result["request_id"] = request_id

                    await r.setex(
                        f"{RESULTS_PREFIX}{request_id}",
                        3600,
                        json.dumps(result, ensure_ascii=False),
                    )
                    logger.info(f"Completed request: {request_id}")
            except Exception as e:
                logger.error(f"Error processing request: {e}")
                await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"Worker failed to start: {e}")
        logger.info("Worker running in demo mode (no Redis)")
        while True:
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())
