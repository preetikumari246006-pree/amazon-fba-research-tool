# scraper.py — Core scraping engine

import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from config import DELAY

# Setup logging
logging.basicConfig(
    filename='logs/scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive",
}


def get_page(url):
    """Fetch a page and return BeautifulSoup object"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code == 200:
            logging.info(f"SUCCESS: {url}")
            return BeautifulSoup(response.content, "lxml")
        else:
            logging.warning(f"Status {response.status_code} for {url}")
            return None

    except Exception as e:
        logging.error(f"ERROR fetching {url}: {e}")
        return None


def scrape_amazon_products(keyword, max_pages=3):
    """Scrape Amazon search results for a keyword"""

    all_products = []

    for page in range(1, max_pages + 1):
        url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}&page={page}"
        print(f"  Scraping page {page} for '{keyword}'...")

        soup = get_page(url)

        if not soup:
            print(f"  ⚠️ Skipping page {page} — could not load")
            continue

        # Find all product cards
        products = soup.find_all("div", {"data-component-type": "s-search-result"})

        for product in products:
            data = extract_product_data(product, keyword)
            if data:
                all_products.append(data)

        # Random delay between pages (avoid getting blocked)
        sleep_time = DELAY + random.uniform(0.5, 1.5)
        time.sleep(sleep_time)

    return all_products


def extract_product_data(product, keyword):
    """Extract all data from a single product card"""

    try:
        # --- TITLE ---
        title_tag = product.find("span", {"class": "a-size-medium"}) or \
                    product.find("span", {"class": "a-size-base-plus"})
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # --- PRICE ---
        price_whole = product.find("span", {"class": "a-price-whole"})
        price_fraction = product.find("span", {"class": "a-price-fraction"})

        if price_whole:
            price_text = price_whole.get_text(strip=True).replace(",", "")
            fraction = price_fraction.get_text(strip=True) if price_fraction else "00"
            price = float(f"{price_text}.{fraction}")
        else:
            price = None

        # --- RATING ---
        rating_tag = product.find("span", {"class": "a-icon-alt"})
        rating_text = rating_tag.get_text(strip=True) if rating_tag else ""
        rating = float(rating_text.split(" ")[0]) if rating_text else None

        # --- REVIEW COUNT ---
        review_tag = product.find("span", {"class": "a-size-base", "dir": "auto"})
        review_text = review_tag.get_text(strip=True).replace(",", "") if review_tag else "0"
        try:
            reviews = int(review_text)
        except:
            reviews = 0

        # --- ASIN (Amazon Product ID) ---
        asin = product.get("data-asin", "N/A")

        # --- PRODUCT URL ---
        link_tag = product.find("a", {"class": "a-link-normal s-no-outline"})
        product_url = f"https://www.amazon.com{link_tag['href']}" if link_tag else "N/A"

        # --- BEST SELLER BADGE ---
        badge = product.find("span", {"class": "a-badge-label"})
        is_best_seller = "YES" if badge else "NO"

        # --- SPONSORED? ---
        sponsored = product.find("span", string="Sponsored")
        is_sponsored = "YES" if sponsored else "NO"

        # --- CALCULATE PROFIT SCORE ---
        profit_score = calculate_profit_score(price, rating, reviews)

        return {
            "Keyword": keyword,
            "Title": title,
            "ASIN": asin,
            "Price ($)": price,
            "Rating": rating,
            "Reviews": reviews,
            "Best Seller": is_best_seller,
            "Sponsored": is_sponsored,
            "Profit Score": profit_score,
            "URL": product_url,
        }

    except Exception as e:
        logging.error(f"Error extracting product: {e}")
        return None


def calculate_profit_score(price, rating, reviews):
    """
    Scoring system:
    - Price sweet spot: $15-$70 (FBA ideal range)
    - High rating: 4.0+
    - Low reviews: less competition = opportunity!
    Score: 0 to 100
    """
    score = 0

    # Price score (max 40 points)
    if price:
        if 15 <= price <= 70:
            score += 40
        elif 10 <= price <= 100:
            score += 25
        elif price > 0:
            score += 10

    # Rating score (max 30 points)
    if rating:
        if rating >= 4.5:
            score += 30
        elif rating >= 4.0:
            score += 20
        elif rating >= 3.5:
            score += 10

    # Review score (max 30 points)
    if reviews <= 100:
        score += 30
    elif reviews <= 500:
        score += 20
    elif reviews <= 1000:
        score += 10

    return score
