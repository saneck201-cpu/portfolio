# Python Web Scraper → CSV & Excel

A command-line scraper that walks through multiple pages of a site, extracts structured data and saves it to **CSV** and **Excel**.

The demo target is [quotes.toscrape.com](https://quotes.toscrape.com/), a site built for scraping practice. The same approach can be adapted to product lists, prices, job boards and other public pages.

## Features
- Follows pagination automatically
- Extracts text, author and tags
- Saves `quotes.csv` (UTF-8, opens fine in Excel) and a formatted `quotes.xlsx`
- Polite: custom User-Agent, timeouts, delay between requests
- Command-line options: `--pages`, `--out`, `--url`

## Run it
```bash
pip install -r requirements.txt
python scraper.py --pages 5 --out my_quotes
```

## Built with
Python, requests, BeautifulSoup, openpyxl
