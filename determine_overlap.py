import json
import csv

# =============================================
ASK_RESULTS_PATH = 'data/yahoo-data/Yahoo_Result_ordered.json'
GOOGLE_RESULTS_PATH = 'data/google-data/Google_Result_ordered.json'
OUTPUT_CSV_PATH = 'results/yahoo_overlap_results.csv'
# =============================================

def spearman_coefficient(google_urls, ask_urls):
    overlap = [url for url in ask_urls if url in google_urls]
    n = len(google_urls)
    if not overlap:
        return 0.0
    ranks_google = [google_urls.index(url) + 1 for url in overlap]
    ranks_ask = [ask_urls.index(url) + 1 for url in overlap]
    d_squared_sum = sum((rg - ra) ** 2 for rg, ra in zip(ranks_google, ranks_ask))
    if n == 1:
        return 0.0
    rs = 1 - (6 * d_squared_sum) / (n * (n**2 - 1))
    return rs

with open(ASK_RESULTS_PATH, 'r') as f:
    ask_results = json.load(f)
with open(GOOGLE_RESULTS_PATH, 'r') as f:
    google_results = json.load(f)

queries = list(google_results.keys())
rows = []
total_overlap = 0
total_percent = 0
total_spearman = 0

for idx, query in enumerate(queries):
    google_urls = google_results.get(query, [])
    ask_urls = ask_results.get(query, [])
    n_google = len(google_urls)
    overlap_urls = [url for url in ask_urls if url in google_urls]
    num_overlap = len(overlap_urls)
    percent_overlap = (num_overlap / n_google * 100) if n_google else 0
    spearman = spearman_coefficient(google_urls, ask_urls)
    rows.append([
        query,
        num_overlap,
        round(percent_overlap, 2),
        round(spearman, 2)
    ])
    total_overlap += num_overlap
    total_percent += percent_overlap
    total_spearman += spearman

num_queries = len(queries)
avg_overlap = round(total_overlap / num_queries, 2) if num_queries else 0
avg_percent = round(total_percent / num_queries, 2) if num_queries else 0
avg_spearman = round(total_spearman / num_queries, 2) if num_queries else 0

rows.append([
    "Averages",
    avg_overlap,
    avg_percent,
    avg_spearman
])

with open(OUTPUT_CSV_PATH, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        "Queries",
        "Number of Overlapping Results",
        "Percent Overlap",
        "Spearman Coefficient"
    ])
    writer.writerows(rows)

print(f"Done. Results saved to {OUTPUT_CSV_PATH}")