import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (educational scraping project - CodeAlpha internship)"}


def get_category(book_url):
    """
    Visit an individual book's page to grab its category.
    The category sits in a breadcrumb trail near the top of the page.
    """
    full_url = "https://books.toscrape.com/catalogue/" + book_url
    response = requests.get(full_url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    breadcrumb = soup.select("ul.breadcrumb li a")
    # breadcrumb[0] = "Home", breadcrumb[1] = category name
    if len(breadcrumb) >= 2:
        return breadcrumb[1].text.strip()
    return "Unknown"


def scrape_all_books(include_category=True, max_pages=50):
    all_books = []

    for page in range(1, max_pages + 1):
        url = BASE_URL.format(page)
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            print(f"Stopped at page {page} (status {response.status_code})")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article", class_="product_pod")

        if not articles:
            break

        for article in articles:
            title = article.h3.a["title"]
            price_text = article.find(class_="price_color").text.strip()
            price = float(price_text.replace("£", "").replace("Â", ""))
            rating_word = article.find(class_="star-rating")["class"][1]
            availability = article.find(class_="instock availability").text.strip()
            book_relative_url = article.h3.a["href"]

            book_data = {
                "title": title,
                "price_gbp": price,
                "rating": rating_word,
                "availability": availability,
            }

            if include_category:
                book_data["category"] = get_category(book_relative_url)
                time.sleep(0.3)  # polite delay for the extra per-book request

            all_books.append(book_data)

        print(f"Page {page} done — {len(articles)} books collected so far: {len(all_books)}")
        time.sleep(1)  # polite delay between page requests

    return pd.DataFrame(all_books)


if __name__ == "__main__":
    df = scrape_all_books(include_category=True)

    # Convert rating words to numbers for easier analysis later
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    df["rating_numeric"] = df["rating"].map(rating_map)

    df.to_csv("books_dataset.csv", index=False)
    print(f"\nDone. Saved {len(df)} books to books_dataset.csv")
    print(df.head())