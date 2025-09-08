import json

# Path to DuckDuckGo results file
results_path = 'duck-data/DuckDuckGo_Result3.json'

with open(results_path, 'r') as f:
    data = json.load(f)

# Find first query with empty results
for idx, (query, urls) in enumerate(data.items()):
    if not urls:
        print(f"First blank result at index {idx}: '{query}'")
        # Optionally, write remaining queries to a new file
        remaining_queries = list(data.keys())[idx:]
        with open('remaining_duck_queries.txt', 'w') as out:
            for q in remaining_queries:
                out.write(q + '\n')
        print(f"Remaining queries written to remaining_duck_queries.txt")
        break
else:
    print("No blank results found.")
