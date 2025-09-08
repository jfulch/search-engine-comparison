import json
from urllib.parse import parse_qs, urlparse, unquote

def clean_duckduckgo_url(url):
    if url.startswith('//duckduckgo.com/l/?uddg='):
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if 'uddg' in qs:
            return unquote(qs['uddg'][0])
    return url

with open('duck-data/DuckDuckGo_Result3.json', 'r') as f:
    data = json.load(f)

cleaned_data = {}
for query, urls in data.items():
    cleaned_data[query] = [clean_duckduckgo_url(u) for u in urls]

with open('duck-data/DuckDuckGo_Result3.json', 'w') as f:
    json.dump(cleaned_data, f, indent=2)