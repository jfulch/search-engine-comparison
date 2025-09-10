import time
import random
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from urllib.parse import unquote

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/116.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36"
]

results_path = '../data/google-data/Google_Result.json'
input_queries_path = '../query-sets/100QueriesSet3.txt'

if os.path.exists(results_path):
    with open(results_path, 'r') as f:
        results = json.load(f)
else:
    results = {}

with open(input_queries_path, 'r') as f:
    queries = [line.strip() for line in f if line.strip()]

def clean_google_url(url):
    # Remove Google's redirect and tracking parameters
    if url.startswith("https://www.google.com/url?"):
        try:
            from urllib.parse import parse_qs, urlparse
            qs = parse_qs(urlparse(url).query)
            if "q" in qs:
                return unquote(qs["q"][0])
        except Exception:
            pass
    return url

def is_external_link(url):
    # Only keep links that do NOT contain google.com in the domain
    return "google.com" not in url

def scrape_google(query, driver):
    url = f"https://www.google.com/search?q={query}"
    driver.get(url)
    time.sleep(random.uniform(2, 4))  # Let page load
    links = []
    # Main selector for Google search results
    for a in driver.find_elements(By.CSS_SELECTOR, 'div#search a'):
        href = a.get_attribute('href')
        if href and href.startswith('http') and is_external_link(href):
            links.append(href)
        if len(links) == 10:
            break
    print(f"[DEBUG] Found {len(links)} external links for query: {query}")
    return links

chrome_options = Options()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')

driver = webdriver.Chrome(options=chrome_options)

cleaned_results = {}
for idx, query in enumerate(queries):
    if results.get(query) and results[query]:
        continue
    print(f"Scraping query {idx+1}/{len(queries)}: {query}")
    raw_links = scrape_google(query, driver)
    if not raw_links:
        print(f"[ERROR] No links found for query: {query}. Stopping process.")
        print(driver.page_source[:2000])
        driver.quit()
        exit(1)
    cleaned_results[query] = [clean_google_url(u) for u in raw_links]
    # Incrementally update the JSON file after each query
    with open(results_path, 'w') as f:
        json.dump({**results, **cleaned_results}, f, indent=2)
    if idx < len(queries) - 1:
        delay = random.randint(30, 120)
        print(f"Waiting {delay} seconds...")
        time.sleep(delay)

for query in results:
    if query not in cleaned_results:
        cleaned_results[query] = [clean_google_url(u) for u in results[query]]

driver.quit()

with open(results_path, 'w') as f:
    json.dump(cleaned_results, f, indent=2)