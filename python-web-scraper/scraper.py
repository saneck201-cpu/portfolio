"""Simple web scraper: collects quotes from quotes.toscrape.com (a site made for practice)
and saves them to CSV and Excel.

Usage:
    python scraper.py                      # first 3 pages -> quotes.csv + quotes.xlsx
    python scraper.py --pages 10 --out my_quotes
"""
import argparse
import csv
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook

START_URL = "https://quotes.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0 (portfolio-scraper)"}
FIELDS = ["text", "author", "tags"]


def parse_page(html: str | bytes) -> tuple[list[dict], str | None]:
    """Return (rows, relative link to the next page or None).

    Pass raw bytes (response.content) so BeautifulSoup detects the encoding itself.
    """
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for block in soup.select("div.quote"):
        text_el = block.select_one("span.text")
        author_el = block.select_one("small.author")
        if not text_el or not author_el:
            continue
        rows.append({
            "text": text_el.get_text(strip=True).strip("“”\""),
            "author": author_el.get_text(strip=True),
            "tags": ", ".join(t.get_text(strip=True) for t in block.select("a.tag")),
        })
    next_link = soup.select_one("li.next a")
    return rows, next_link["href"] if next_link else None


def scrape(start_url: str, max_pages: int, delay: float = 0.5) -> list[dict]:
    rows: list[dict] = []
    url = start_url
    session = requests.Session()
    session.headers.update(HEADERS)
    for page in range(1, max_pages + 1):
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
        page_rows, next_href = parse_page(resp.content)
        rows.extend(page_rows)
        print(f"Page {page}: {len(page_rows)} quotes")
        if not next_href:
            break
        url = urljoin(url, next_href)
        time.sleep(delay)  # be polite to the server
    return rows


def save_csv(rows: list[dict], path: str) -> None:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def save_xlsx(rows: list[dict], path: str) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Quotes"
    ws.append(FIELDS)
    for row in rows:
        ws.append([row[k] for k in FIELDS])
    ws.column_dimensions["A"].width = 90
    ws.column_dimensions["B"].width = 22
    ws.column_dimensions["C"].width = 40
    wb.save(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape quotes to CSV and Excel")
    parser.add_argument("--url", default=START_URL, help="start URL")
    parser.add_argument("--pages", type=int, default=3, help="max pages to scrape")
    parser.add_argument("--out", default="quotes", help="output file name without extension")
    args = parser.parse_args()

    rows = scrape(args.url, args.pages)
    save_csv(rows, f"{args.out}.csv")
    save_xlsx(rows, f"{args.out}.xlsx")
    print(f"Done: {len(rows)} rows saved to {args.out}.csv and {args.out}.xlsx")


if __name__ == "__main__":
    main()
