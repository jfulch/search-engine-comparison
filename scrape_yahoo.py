import requests
from bs4 import BeautifulSoup
import time
import random
import json
import os
from urllib.parse import unquote, parse_qs, urlparse

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/116.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36"
]

results_path = 'yahoo-data/Yahoo_Result3.json'
input_queries_path = 'query-sets/25QueriesSet3.txt'

if os.path.exists(results_path):
    with open(results_path, 'r') as f:
        results = json.load(f)
else:
    results = {}

with open(input_queries_path, 'r') as f:
    queries = [line.strip() for line in f if line.strip()]

def scrape_yahoo(query, max_retries=3):
    url = f"https://search.yahoo.com/search?p={requests.utils.quote(query)}"
    session = requests.Session()
    for attempt in range(max_retries):
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://search.yahoo.com/",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            }
            resp = session.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            links = []

            for a in soup.select('div#web ol li div.compTitle a'):
                href = a.get('href')
                if href and href.startswith('http'):
                    links.append(href)
                if len(links) == 10:
                    break

            if len(links) < 10:
                for a in soup.select('div#web a'):  
                    href = a.get('href')
                    if href and href.startswith('http') and href not in links:
                        links.append(href)
                    if len(links) == 10:
                        break
            print(f"[DEBUG] Found {len(links)} links for query: {query}")
            if not links:
                print(f"[DEBUG] No results found for query: {query}")
                print(resp.text[:2000])  
            return links
        except Exception as e:
            print(f"Error on attempt {attempt+1} for query '{query}': {e}")
            time.sleep(5)
    return []

for idx, query in enumerate(queries):
    if results.get(query):
        continue
    print(f"Scraping query {idx+1}/{len(queries)}: {query}")
    results[query] = scrape_yahoo(query)
    if idx < len(queries) - 1:
        delay = random.randint(10, 60)
        print(f"Waiting {delay} seconds...")
        time.sleep(delay)

def clean_yahoo_url(url):
    
    if 'RU=' in url:
        try:
            
            parsed = urlparse(url)
            qs = parse_qs(parsed.query)
            
            if 'RU=' in url:
               
                start = url.find('RU=') + 3
                end = url.find('/RK=', start)
                if end == -1:
                    end = len(url)
                real_url = url[start:end]
                return unquote(real_url)
        except Exception:
            pass
    return url   

cleaned_results = {}
for query, urls in results.items():
    cleaned_results[query] = [clean_yahoo_url(u) for u in urls]

with open(results_path, 'w') as f:
    json.dump(cleaned_results, f, indent=2)