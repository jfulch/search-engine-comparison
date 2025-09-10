import json
import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("google_api_key")
CX = os.getenv("google_cse_id")

results_path = '../data/google-data/Google_Result.json'
input_queries_path = '../query-sets/100QueriesSet3.txt'

if os.path.exists(results_path):
    with open(results_path, 'r') as f:
        results = json.load(f)
else:
    results = {}

with open(input_queries_path, 'r') as f:
    queries = [line.strip() for line in f if line.strip()]

def search_google_api(query, api_key, cx):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "num": 10
    }
    try:
        resp = requests.get(url, params=params)
        data = resp.json()
        links = []
        for item in data.get("items", []):
            link = item.get("link")
            if link and "google.com" not in link:
                links.append(link)
            if len(links) == 10:
                break
        return links
    except Exception as e:
        print(f"[ERROR] API error for query '{query}': {e}")
        return []

cleaned_results = {}
for idx, query in enumerate(queries):
    if results.get(query) and results[query]:
        continue
    print(f"Query {idx+1}/{len(queries)}: {query}")
    links = search_google_api(query, API_KEY, CX)
    if not links:
        print(f"[ERROR] No links found for query: {query}. Stopping process.")
        break
    cleaned_results[query] = links
    with open(results_path, 'w') as f:
        json.dump({**results, **cleaned_results}, f, indent=2)
    # Delay removed

for query in results:
    if query not in cleaned_results:
        cleaned_results[query] = results[query]

with open(results_path, 'w') as f:
    json.dump(cleaned_results, f, indent=2)

print("Done. Results saved to", results_path)