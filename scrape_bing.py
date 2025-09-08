import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/116.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36"
]

# Load existing results
results_path = 'bing-data/Bing_Result3.json'
if os.path.exists(results_path):
    with open(results_path, 'r') as f:
        results = json.load(f)
else:
    results = {}

# Read queries
with open('100QueriesSet3.txt', 'r') as f:
    queries = [line.strip() for line in f if line.strip()]

def scrape_bing(query, max_retries=3):
    url = f"https://www.bing.com/search?q={requests.utils.quote(query)}"
    for attempt in range(max_retries):
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS)
            }
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            links = []
            for a in soup.select('li.b_algo h2 a'):
                href = a.get('href')
                if href and href.startswith('http'):
                    links.append(href)
                if len(links) == 10:
                    break
            return links
        except Exception as e:
            print(f"Error on attempt {attempt+1} for query '{query}': {e}")
            time.sleep(5)
    return []

for idx, query in enumerate(queries):
    if results.get(query):
        continue
    print(f"Scraping query {idx+1}/{len(queries)}: {query}")
    results[query] = scrape_bing(query)
    if idx < len(queries) - 1:
        delay = random.randint(10, 60)
        print(f"Waiting {delay} seconds...")
        time.sleep(delay)

with open(results_path, 'w') as f:
    json.dump(results, f, indent=2)
