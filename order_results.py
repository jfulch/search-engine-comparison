import json

# Paths to your files
results_path = 'data/yahoo-data/Yahoo_Result.json'
queries_path = 'query-sets/100QueriesSet3.txt'
output_path = 'data/yahoo-data/Yahoo_Result_ordered.json'

# Load queries in order
with open(queries_path, 'r') as f:
    queries = [line.strip() for line in f if line.strip()]

# Load results
with open(results_path, 'r') as f:
    results = json.load(f)

# Reorder results according to queries
ordered_results = {}
for query in queries:
    ordered_results[query] = results.get(query, [])

# Save ordered results
with open(output_path, 'w') as f:
    json.dump(ordered_results, f, indent=2)

print(f"Ordered results saved to {output_path}")