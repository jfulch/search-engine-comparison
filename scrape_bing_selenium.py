import time
import random
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import unquote
import base64
from urllib.parse import urlparse, parse_qs, unquote

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/116.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36"
]

results_path = 'bing-data/Bing_Result.json'
input_queries_path = 'query-sets/50QueriesSet3.txt'

if os.path.exists(results_path) and os.path.getsize(results_path) > 0:
    with open(results_path, 'r') as f:
        results = json.load(f)
else:
    results = {}

with open(input_queries_path, 'r') as f:
    queries = [line.strip() for line in f if line.strip()]

def clean_bing_url(url):
    # If it's a Bing redirect, extract and decode the real URL from the 'u' parameter
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    if "bing.com/ck/a" in url and "u" in qs:
        b64 = qs["u"][0]
        # Remove leading 'a1' if present, then decode
        if b64.startswith("a1"):
            b64 = b64[2:]
        try:
            decoded = base64.b64decode(b64).decode("utf-8")
            return unquote(decoded)
        except Exception:
            return url
    return url

def is_external_link(url):
    # Only keep links that are not Bing internal, not navigation, not ads
    parsed = urlparse(url)
    # Exclude Bing domains
    if "bing.com" in parsed.netloc:
        # Allow Bing redirect links (which will be cleaned), but not navigation
        if "/ck/a" in parsed.path:
            return True
        return False
    # Exclude other known ad or navigation links if needed
    return True

def scrape_bing(query, driver):
    url = f"http://www.bing.com/search?q={query}"
    driver.get(url)
    time.sleep(random.uniform(2, 4))
    links = []
    for a in driver.find_elements(By.CSS_SELECTOR, 'li.b_algo h2 a'):
        href = a.get_attribute('href')
        if href and href.startswith('http') and is_external_link(href):
            links.append(clean_bing_url(href))
        if len(links) == 10:
            break
    print(f"[DEBUG] Raw links: {[a.get_attribute('href') for a in driver.find_elements(By.CSS_SELECTOR, 'li.b_algo h2 a')]}")
    print(f"[DEBUG] Filtered links: {links}")
    return links

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')

# You may need to set the path to your chromedriver here
# driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)

cleaned_results = {}
for idx, query in enumerate(queries):
    # Only skip queries that already have non-empty results
    if results.get(query) and results[query]:
        continue
    print(f"Scraping query {idx+1}/{len(queries)}: {query}")
    try:
        raw_links = scrape_bing(query, driver)
    except Exception as e:
        print(f"[ERROR] Exception occurred for query: {query}. Stopping process.")
        print(str(e))
        driver.quit()
        exit(1)
    if not raw_links:
        print(f"[ERROR] No links found for query: {query}. Stopping process.")
        print(driver.page_source[:2000])
        driver.quit()
        exit(1)
    cleaned_results[query] = [clean_bing_url(u) for u in raw_links]
    # Incrementally update the JSON file after each query
    with open(results_path, 'w') as f:
        json.dump({**results, **cleaned_results}, f, indent=2)
    if idx < len(queries) - 1:
        delay = random.randint(30, 120)
        print(f"Waiting {delay} seconds...")
        time.sleep(delay)

# Only fill in missing queries from previous results
for query in results:
    if query not in cleaned_results:
        cleaned_results[query] = [clean_bing_url(u) for u in results[query]]

driver.quit()

with open(results_path, 'w') as f:
    json.dump(cleaned_results, f, indent=2)