# Search Engine Comparison

## Overview
This project compares the search results of Google with those of other major search engines (Ask Jeeves, Bing, DuckDuckGo, Yahoo) for a set of queries. The goal is to analyze how similar or different the search results are, both in terms of overlap and ranking order.

## Features
- Automated scraping of top search results from Google and other engines for up to 100 queries.
- Incremental JSON storage of results for each query.
- Filtering to exclude non-native results (e.g., YouTube links).
- Statistical analysis of search result overlap and ranking similarity.

## Analysis Metrics
- **Percent Overlap:** Measures the percentage of Google’s top 10 results that also appear in the other search engine’s top 10.
- **Spearman Coefficient:** Measures how similarly the overlapping results are ranked between Google and the other engine (1 = identical order, 0 = no correlation, -1 = reverse order).

## Workflow
1. Scrape search results for each query from Google and another engine.
2. Store results in JSON files, one per engine.
3. Run analysis scripts to compare results and output a CSV file with overlap and Spearman statistics for each query.

## Output
- CSV file listing, for each query:
  - Query text
  - Number of overlapping results
  - Percent overlap
  - Spearman rank correlation coefficient

## Requirements
- Python 3.x
- Selenium WebDriver
- ChromeDriver (for Selenium)
- Google Custom Search API (for Google results)
- .env file for API keys

## Usage
1. Run the scraper scripts for each search engine.
2. Run the analysis script (`determine_overlap.py`) to generate the comparison CSV.
3. Review the CSV output to interpret overlap and ranking similarity.

## Example
```
Queries,Number of Overlapping Results,Percent Overlap,Spearman Coefficient
How is the spinning mule fuelled,2,20.0,0.99
...
```

## Notes
- Low percent overlap means few results are shared between engines.
- High Spearman coefficient means shared results are ranked similarly.
- The project can be extended to other search engines or more queries.