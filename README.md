# CodeAlpha_WebScraping

**Task:** Web Scraping (CodeAlpha Data Analytics Internship)

## Overview
Scrapes book data — title, price, star rating, availability, and category —
from [books.toscrape.com](https://books.toscrape.com/), a public sandbox site
built specifically for web scraping practice.

## Tools
- `requests` — fetch raw HTML
- `BeautifulSoup` (bs4) — parse HTML and extract fields
- `pandas` — structure and export the results

## How it works
1. Loops through all 50 catalogue pages.
2. For each book listing, extracts: title (from the link's `title` attribute),
   price (from the `price_color` class), star rating (decoded from the
   `star-rating` CSS class), and stock availability.
3. Visits each book's individual page to fetch its category from the
   breadcrumb navigation.
4. Saves everything to `books_dataset.csv`.

## Run it
\`\`\`bash
pip install requests beautifulsoup4 pandas
python scrape_books.py
\`\`\`

Output: `books_dataset.csv` with ~1000 rows and columns:
`title, price_gbp, rating, availability, category, rating_numeric`

## Notes
- A 1-second delay between page requests (and 0.3s for per-book category
  lookups) is included to scrape responsibly and avoid overloading the
  server.
- This site explicitly permits scraping for practice purposes.