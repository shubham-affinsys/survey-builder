import asyncio
import httpx
import time
from itertools import count

urls = [
    "https://survey-builder-production.up.railway.app/survey_questions/123",
    "https://survey-builder-production.up.railway.app/surveys",
    "https://survey-builder-production.up.railway.app/users",
    ]

# urls = [
#     "http://127.0.0.1:8081/survey_questions/123",
#     "http://127.0.0.1:8081/surveys",
#     "http://127.0.0.1:8081/users",
#     ]


start = time.time()
n = 100 # Number of iterations

# counter = count()  # Thread-safe atomic counter

async def req(client, url):
    # current_request = next(counter)  # Atomic increment
    # print(f"Request sent {current_request}")
    response = await client.get(url)
    # print(f"Got response for {current_request}: {response.status_code}")

async def main():
    async with httpx.AsyncClient() as client:
        tasks = []
        for _ in range(n):
            for url in urls:
                tasks.append(req(client, url))
        await asyncio.gather(*tasks)

# Run the main coroutine
asyncio.run(main())

end = time.time()
print(f"Time taken for {n * len(urls)} requests: {end - start}s")
