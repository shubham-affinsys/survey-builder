import asyncio
import time
from itertools import cycle
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.future import select
from models import User  # Assuming your User model is defined here
from os import getenv

# Database URLs
DB_URL_ASYNC = f"postgresql+asyncpg://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:5433/{getenv('POSTGRES_DB')}"
DB_URL_SYNC = f"postgresql+psycopg2://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:5433/{getenv('POSTGRES_DB')}"

# Async Engine and Session
async_engine = create_async_engine(DB_URL_ASYNC, pool_size=20, max_overflow=10, future=True)
AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# Sync Engine and Session
sync_engine = create_engine(DB_URL_SYNC, pool_size=20, max_overflow=10, future=True)
SyncSessionLocal = scoped_session(sessionmaker(bind=sync_engine))

# Measure sync function for DB
def fetch_from_db_sync(req_id, worker_id, latencies):
    """Sync function to fetch data from DB."""
    start_time = time.time()
    try:
        with SyncSessionLocal() as db_session:
            result = db_session.execute(select(User))
            users = result.scalars().all()
            latencies.append(time.time() - start_time)  # Record latency for this request
            return users
    except Exception as e:
        latencies.append(time.time() - start_time)  # Error latency
        print(f"Worker {worker_id} - Request {req_id} - Error (sync): {e}")
        return []

# Measure async function for DB
async def fetch_from_db_async(req_id, worker_id, latencies):
    """Async function to fetch data from DB."""
    start_time = time.time()
    try:
        async with AsyncSessionLocal() as db_session:
            result = await db_session.execute(select(User))
            users = result.scalars().all()
            latencies.append(time.time() - start_time)  # Record latency for this request
            return users
    except Exception as e:
        latencies.append(time.time() - start_time)  # Error latency
        print(f"Worker {worker_id} - Request {req_id} - Error (async): {e}")
        return []

# Sync worker function (parallely running workers)
async def worker_sync(num_requests, worker_id, latencies):
    """Sync worker that makes a series of sync requests to the database."""
    print(f"Sync Worker {worker_id} started.")
    worker_start = time.time()

    for req_id in range(num_requests):
        fetch_from_db_sync(req_id, worker_id, latencies)

    worker_end = time.time()
    return worker_end - worker_start  # Return the total time for the worker

# Async worker function
async def worker_async(num_requests, worker_id, latencies):
    """Async worker that makes a series of async requests to the database."""
    print(f"Async Worker {worker_id} started.")
    worker_start = time.time()

    tasks = [fetch_from_db_async(req_id, worker_id, latencies) for req_id in range(num_requests)]
    await asyncio.gather(*tasks, return_exceptions=True)

    worker_end = time.time()
    return worker_end - worker_start  # Return the total time for the worker

# Main function to compare sync vs async performance
async def compare_sync_async(num_requests, num_workers):
    sync_latencies = []
    async_latencies = []

    # Sync workers execution (spawned in parallel)
    print("=== Sync Workers ===")
    sync_start = time.time()

    sync_worker_tasks = [
        asyncio.create_task(worker_sync(num_requests, worker_id=i+1, latencies=sync_latencies))
        for i in range(num_workers)
    ]
    sync_times = await asyncio.gather(*sync_worker_tasks)

    sync_end = time.time()

    # Async workers execution
    print("\n=== Async Workers ===")
    async_start = time.time()
    async_worker_tasks = [
        worker_async(num_requests, worker_id=i+1, latencies=async_latencies)
        for i in range(num_workers)
    ]
    await asyncio.gather(*async_worker_tasks)
    async_end = time.time()

    # Calculate total times
    sync_total_time = sum(sync_times)
    async_total_time = async_end - async_start

    # Calculate min, max, avg latencies
    sync_min_latency = min(sync_latencies)
    sync_max_latency = max(sync_latencies)
    sync_avg_latency = sum(sync_latencies) / len(sync_latencies)

    async_min_latency = min(async_latencies)
    async_max_latency = max(async_latencies)
    async_avg_latency = sum(async_latencies) / len(async_latencies)

    # Print results
    print("\n=== Performance Results ===")
    print(f"Sync Total Time: {sync_total_time:.4f} seconds")
    print(f"Async Total Time: {async_total_time:.4f} seconds")
    print(f"Sync Min Latency: {sync_min_latency:.4f} seconds")
    print(f"Sync Max Latency: {sync_max_latency:.4f} seconds")
    print(f"Sync Avg Latency: {sync_avg_latency:.4f} seconds")
    print(f"Async Min Latency: {async_min_latency:.4f} seconds")
    print(f"Async Max Latency: {async_max_latency:.4f} seconds")
    print(f"Async Avg Latency: {async_avg_latency:.4f} seconds")

    # Calculate percentage difference
    if sync_total_time > async_total_time:
        percentage_faster = (sync_total_time - async_total_time) / sync_total_time * 100
        print(f"Async is {percentage_faster:.2f}% faster than Sync.")
    else:
        percentage_faster = (async_total_time - sync_total_time) / async_total_time * 100
        print(f"Sync is {percentage_faster:.2f}% faster than Async.")

# Run comparison
asyncio.run(compare_sync_async(num_requests=1000, num_workers=5))



# import asyncio
# from itertools import cycle
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.future import select
# from models import User  # Assuming your User model is defined here
# from os import getenv
# import time
# # Database URLs
# DB_URL = f"postgresql+asyncpg://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}:5433/{getenv('POSTGRES_DB')}"
# # print(DATABASE_URLS)
# # Create engines for each database URL
# # engines = [create_async_engine(url, pool_size=10, max_overflow=20, future=True) for url in DATABASE_URLS]
# engine = create_async_engine(DB_URL, pool_size=20, max_overflow=10, future=True)
# # Create a sessionmaker for each engine
# SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# # Create a round-robin iterator to cycle through sessions
# # session_cycle = cycle(SessionLocals)

# async def fetch_from_db(req_id, worker_id):
#     """Function to simulate database interaction with a new session per request."""
#     try:
#         # Get the next session in the cycle
#         # SessionLocal = next(session_cycle)
        
#         # Create a new session for each request
#         async with SessionLocal() as db_session:
#             print(f"Worker {worker_id} - Request {req_id} - Fetching data from DB using engine", flush=True)

#             # Example query for fetching all users
#             result = await db_session.execute(select(User))
#             users = result.scalars().all()

#             print(f"Worker {worker_id} - Request {req_id} - Fetched {len(users)} users from DB", flush=True)

#             return users

#     except Exception as e:
#         print(f"Worker {worker_id} - Request {req_id} - Error fetching from DB: {e}")
#         return []

# async def worker(num_requests, worker_id, response_times):
#     """An async worker that makes a series of async requests to the database."""
#     print(f"Worker {worker_id} started.")
#     worker_start = time.time()

#     tasks = [
#         fetch_from_db(req_id, worker_id) for req_id in range(num_requests)
#     ]
    
#     # Run DB tasks sequentially
#     results = await asyncio.gather(*tasks, return_exceptions=True)

#     worker_end = time.time()
#     print(f"Worker {worker_id} finished in {worker_end - worker_start:.4f} seconds.")
#     return results

# async def main_app(num_requests_per_worker, num_workers):
#     """Main application that launches multiple worker applications, each making database requests."""
#     print("Main application started.")
#     main_start = time.time()

#     response_times = []

#     # Create worker tasks
#     worker_tasks = [
#         worker(num_requests_per_worker, worker_id=i+1, response_times=response_times) for i in range(num_workers)
#     ]

#     # Run all workers concurrently
#     all_results = await asyncio.gather(*worker_tasks, return_exceptions=True)

#     main_end = time.time()
#     print("Main application finished.")
#     print(f"Total time taken for {num_workers * num_requests_per_worker} database requests: {main_end - main_start:.4f} seconds")

#     return all_results

# # Configurations
# num_requests_per_worker = 1000
# num_workers = 10

# # Run the main application
# asyncio.run(main_app(num_requests_per_worker, num_workers))



import time
import aiohttp
import asyncio
from itertools import cycle
errors =0
async def fetch(url, session, req_id, worker_id, response_times):
    global errors
    try:
        start_time = time.time()  # Record the time when the request starts
        print(f"Worker: {worker_id} - Request: {req_id} - sent to {url}", flush=True)

        async with session.get(url) as response:
            if response.status != 200:
                error+=1
                print(f"Worker: {worker_id} - Request: {req_id} to {url} -----------error-----------------", flush=True)
                return ""

            response.raise_for_status()

            end_time = time.time()  # Record the time when the request ends
            response_time = end_time - start_time  # Calculate the time taken for the request
            response_times.append(response_time)  # Store the response time for later analysis

            # print(f"Worker: {worker_id} - Request: {req_id} - Response Time: {response_time:.4f}s - Response from {url}", flush=True)
            return ""

    except aiohttp.ClientError as e:
        print(f"Request to {url} failed: {e}")
        return {"error": str(e)}
    except Exception as e:
        print(f"Unexpected error in worker {worker_id}, request {req_id}: {e}")

async def worker(urls, num_requests, worker_id, response_times):
    """An async worker application that makes a series of async requests across multiple URLs."""
    print(f"Worker {worker_id} started.")
    worker_start = time.time()

    async with aiohttp.ClientSession() as session:
        # Cycle through URLs and create tasks for each request
        tasks = [fetch(url, session, req_id, worker_id, response_times) for req_id, url in zip(range(num_requests), cycle(urls))]
        results = await asyncio.gather(*tasks, return_exceptions=True)  # Ensures all tasks complete even if some fail

    worker_end = time.time()
    print(f"Worker {worker_id} finished in {worker_end - worker_start:.4f} seconds.")
    return results

async def main_app(urls, num_requests_per_worker, num_workers):
    """Main application that launches multiple worker applications, distributing requests across multiple URLs."""
    print("Main application started.")
    main_start = time.time()

    # Create a list to store response times
    response_times = []

    # Create worker tasks
    worker_tasks = [
        worker(urls, num_requests_per_worker, worker_id=i+1, response_times=response_times) for i in range(num_workers)
    ]

    # Run all workers concurrently
    all_results = await asyncio.gather(*worker_tasks, return_exceptions=True)
    global errors
    # Calculate statistics for the response times
    if response_times:
        avg_response_time = sum(response_times) / len(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)
        print(f"\nAverage Response Time: {avg_response_time:.4f}s")
        print(f"Min Response Time: {min_response_time:.4f}s")
        print(f"Max Response Time: {max_response_time:.4f}s")

        print(f"errors :{errors}")

    main_end = time.time()
    print("Main application finished.")
    print(f"Total time taken for { len(urls) * num_workers * num_requests_per_worker} requests: {main_end - main_start:.4f} seconds")

    return all_results

# Configurations
urls = [
    "http://0.0.0.0:8081/surveys",
    "http://0.0.0.0:8081/users",
    "http://0.0.0.0:8081/answers",
    "http://0.0.0.0:8081/user-responses"
]  # Add more URLs as needed
num_requests_per_worker = 1000
num_workers = 10

# Run the main application
asyncio.run(main_app(urls, num_requests_per_worker, num_workers))


# # import time
# import aiohttp
# import asyncio
# import json
# import time
# import db

# async def fetch(url, session, req_id, test_id):
#     """Perform POST request to the URL with test data."""
#     test_data = {
#         "test_id": test_id,
#         "test_data": db.data
#     }

#     try:
#         async with session.post(url, json=test_data) as response:
#             response.raise_for_status()  # Check for any HTTP errors
#             response_data = await response.json()  # Assuming response is in JSON format
#             print(f"Completed request -- req_id: {req_id}")
#             print(f"Response for req_id {req_id}: {response_data}")  # Print the response data
#             return response_data

#     except aiohttp.ClientError as e:
#         print(f"Request to {url} failed: {e}")
#         return {"error": str(e)}

# async def worker(url, num_requests, worker_id):
#     """An async worker that makes a series of POST requests."""
#     print(f"Worker {worker_id} started.")
#     worker_start = time.time()

#     async with aiohttp.ClientSession() as session:
#         # Start the request counters
#         req_id_counter = 1
#         test_id_counter = 1

#         # Create a list of tasks for POST requests
#         tasks = [
#             fetch(f"{url}/{req_id_counter}", session, req_id=req_id_counter, test_id=f"test{test_id_counter}")
#             for req_id_counter, test_id_counter in zip(range(1, num_requests + 1), range(1, num_requests + 1))
#         ]

#         # Await all the tasks
#         results = await asyncio.gather(*tasks)

#     worker_end = time.time()
#     print(f"Worker {worker_id} finished in {worker_end - worker_start} seconds.")
#     return results

# async def main_app(url, num_requests_per_worker, num_workers):
#     """Main application that launches multiple worker applications."""
#     print("Main application started.")
#     main_start = time.time()

#     # Create worker tasks
#     worker_tasks = [
#         worker(url, num_requests_per_worker, worker_id=i+1) for i in range(num_workers)
#     ]

#     # Run all workers concurrently
#     all_results = await asyncio.gather(*worker_tasks)

#     main_end = time.time()
#     print("Main application finished.")
#     print(f"Total time taken for {num_workers * num_requests_per_worker} requests: {main_end - main_start} seconds")

#     return all_results

# # Configurations
# url = "http://0.0.0.0:8080/test"
# num_requests_per_worker = 10 # Number of requests per worker
# num_workers = 1  # Number of workers

# # Run the main application
# asyncio.run(main_app(url, num_requests_per_worker, num_workers))







# import time
# import aiohttp
# import asyncio

# async def fetch(url, session, req_id, worker_id, response_times):
#     try:
#         start_time = time.time()  # Record the time when the request starts
#         print(f"Worker: {worker_id} - Request: {req_id} - sent ",flush=True)

#         async with session.get(url) as response:

#             if response.status != 200:
#                 print(f"Worker: {worker_id} - Request: {req_id}  -----------errror-----------------",flush=True)
#                 return ""

#             response.raise_for_status()
#             # res = await response.json()

#             end_time = time.time()  # Record the time when the request ends

#             response_time = end_time - start_time  # Calculate the time taken for the request
#             response_times.append(response_time)  # Store the response time for later analysis

#             print(f"Worker: {worker_id} - Requsest: {req_id} - Response Time: {response_time:.4f}s - Res: ",flush=True)
#             # time.sleep(.1)
#             return ""

#     except aiohttp.ClientError as e:
#         print(f"Request to {url} failed: {e}")
#         return {"error": str(e)}

# async def worker(url, num_requests, worker_id, response_times):
#     """An async worker application that makes a series of async requests."""
#     print(f"Worker {worker_id} started.")
#     worker_start = time.time()

#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch(url, session, req_id, worker_id, response_times) for req_id in range(0, num_requests)]
#         results = await asyncio.gather(*tasks)

#     worker_end = time.time()
#     print(f"Worker {worker_id} finished in {worker_end - worker_start:.4f} seconds.")
#     return results

# async def main_app(url, num_requests_per_worker, num_workers):
#     """Main application that launches multiple worker applications."""
#     print("Main application started.")
#     main_start = time.time()

#     # Create a list to store response times
#     response_times = []

#     # Create worker tasks
#     worker_tasks = [
#         worker(url, num_requests_per_worker, worker_id=i+1, response_times=response_times) for i in range(num_workers)
#     ]

#     # Run all workers concurrently
#     all_results = await asyncio.gather(*worker_tasks)

#     # Calculate statistics for the response times
#     if response_times:
#         avg_response_time = sum(response_times) / len(response_times)
#         min_response_time = min(response_times)
#         max_response_time = max(response_times)
#         print(f"\nAverage Response Time: {avg_response_time:.4f}s")
#         print(f"Min Response Time: {min_response_time:.4f}s")
#         print(f"Max Response Time: {max_response_time:.4f}s")

#     main_end = time.time()
#     print("Main application finished.")
#     print(f"Total time taken for {num_workers * num_requests_per_worker} requests: {main_end - main_start:.4f} seconds")

#     return all_results

# # Configurations
# url = "http://0.0.0.0:8080/surveys"  # Update URL as needed
# num_requests_per_worker = 100
# num_workers = 10

# # Run the main application
# asyncio.run(main_app(url, num_requests_per_worker, num_workers))



# import time
# import aiohttp
# import asyncio

# count =0
# async def fetch(url, session):
#     global count
#     print("sleep ",count)
#     count+=1
#     async with session.get(url) as response:
#         time.sleep(.2)
#         return ""

# async def main(url, n):
#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch(url, session) for _ in range(n)]
#         results = await asyncio.gather(*tasks)
#     return results

# start = time.time()

# url = "http://0.0.0.0:8080/surveys"

# n = 100

# asyncio.run(main(url, n))

# end = time.time()
# print(f"Time taken for {n} requests: {end - start} seconds")





# import time
# import aiohttp
# import asyncio

# count =0
# async def fetch(url, session):
#     global count
#     print("sleep ",count)
#     count+=1
#     time.sleep(.1)
#     print("sending request...")
#     async with session.get(url) as response:
#         print("request sent and recieved response")
#         time.sleep(.2)
#         return ""

# async def main(url, n):
#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch(url, session) for _ in range(n)]
#         results = await asyncio.gather(*tasks)
#     return results

# start = time.time()

# url = "http://0.0.0.0:8080/surveys"

# n = 100

# asyncio.run(main(url, n))

# end = time.time()
# print(f"Time taken for {n} requests: {end - start} seconds")


# import time
# import aiohttp
# import asyncio
# import requests
# count =0
# def fetch(url):
#     global count
#     print("sleep ",count)
#     count+=1
#     with requests.get(url) as response:
#         time.sleep(.2)
#         return ""

# def main(url, n):
#     # with aiohttp.ClientSession() as session:
#     for _ in range(n):
#         fetch(url) 
#         # results = await asyncio.gather(*tasks)
#     # return results

# start = time.time()

# url = "http://0.0.0.0:8080/surveys"

# n = 100

# # asyncio.run(main(url, n))
# main(url,n)

# end = time.time()
# print(f"Time taken for {n} requests: {end - start} seconds")