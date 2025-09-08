# import required modules
import requests
from bs4 import BeautifulSoup
import time
import random
import json

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/116.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
	"Mozilla/5.0 (Linux; Android 13; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36"
]

with open('100QueriesSet3.txt', 'r') as f:
	queries = [line.strip() for line in f if line.strip()]

results = {}

def scrape_duckduckgo(query):
	url = f"https://duckduckgo.com/html/?q={requests.utils.quote(query)}"
	headers = {
		"User-Agent": random.choice(USER_AGENTS)
	}
	resp = requests.get(url, headers=headers)
	soup = BeautifulSoup(resp.text, 'html.parser')
	links = []
	for a in soup.select('a.result__a'):
		href = a.get('href')
		if href:
			links.append(href)
		if len(links) == 10:
			break
	return links

for idx, query in enumerate(queries):
	print(f"Scraping query {idx+1}/{len(queries)}: {query}")
	results[query] = scrape_duckduckgo(query)
	if idx < len(queries) - 1:
		delay = random.randint(10, 30)
		print(f"Waiting {delay} seconds...")
		time.sleep(delay)

# Clean up DuckDuckGo redirect URLs to final URLs
from urllib.parse import parse_qs, urlparse, unquote
def clean_duckduckgo_url(url):
	if url.startswith('//duckduckgo.com/l/?uddg='):
		parsed = urlparse(url)
		qs = parse_qs(parsed.query)
		if 'uddg' in qs:
			return unquote(qs['uddg'][0])
	return url

cleaned_results = {}
for query, urls in results.items():
	cleaned_results[query] = [clean_duckduckgo_url(u) for u in urls]

# Save cleaned results to JSON file
with open('./duck-data/DuckDuckGo_Result3.json', 'w') as f:
	json.dump(cleaned_results, f, indent=2)
