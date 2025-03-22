# import httpx
# import asyncio
# import time

# url = "http://localhost:5000/api/tasks/cache"

# async def fetch_tasks(client, request_num):
#     start_time = time.time()
#     response = await client.get(url)
#     end_time = time.time()
#     print(f"Request {request_num}:")
#     print(f" - Status: {response.status_code}")
#     print(f" - Time: {end_time - start_time:.4f} seconds")
#     print(f" - Tasks count: {len(response.json())}")
#     print("-" * 50)

import httpx
import asyncio
import time

url = "http://localhost:5000/api/tasks/cache"

async def fetch_tasks(client, request_num):
    start_time = time.time()
    response = await client.get(url)
    end_time = time.time()
    if request_num % 10 == 0 or request_num == 1:  # In lần 1 và mỗi 10 request
        print(f"Request {request_num}:")
        print(f" - Status: {response.status_code}")
        print(f" - Time: {end_time - start_time:.4f} seconds")
        print(f" - Tasks count: {len(response.json())}")
        print("-" * 50)

async def main():
    start_time = time.time()
    async with httpx.AsyncClient() as client:
        tasks = [fetch_tasks(client, i+1) for i in range(50)]
        await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Total time for 100 requests: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    asyncio.run(main())