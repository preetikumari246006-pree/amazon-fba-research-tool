# main.py — Entry point, run this file!

import time
from scraper import scrape_amazon_products
from excel_export import create_excel_report
from config import KEYWORDS, MAX_PAGES


def print_banner():
    print("""
╔══════════════════════════════════════════════════╗
║       🔍 Amazon FBA Product Research Tool        ║
║         Find Profitable Products Fast!           ║
╚══════════════════════════════════════════════════╝
    """)


def print_progress(current, total, keyword):
    percent = int((current / total) * 100)
    bar = "█" * (percent // 5) + "░" * (20 - percent // 5)
    print(f"\n[{bar}] {percent}% — Researching: '{keyword}'")


def main():
    print_banner()

    all_products = []
    total_keywords = len(KEYWORDS)

    print(f"📋 Keywords to research: {total_keywords}")
    print(f"📄 Pages per keyword: {MAX_PAGES}")
    print(f"🔎 Total searches: {total_keywords * MAX_PAGES}")
    print("\n" + "─" * 50)

    start_time = time.time()

    # ── Scrape each keyword ──
    for index, keyword in enumerate(KEYWORDS, 1):
        print_progress(index, total_keywords, keyword)

        products = scrape_amazon_products(keyword, MAX_PAGES)
        all_products.extend(products)

        print(f"  ✅ Found {len(products)} products for '{keyword}'")

    print("\n" + "─" * 50)

    # ── Results Summary ──
    elapsed = round(time.time() - start_time, 2)
    print(f"\n⏱️  Scraping completed in {elapsed} seconds")
    print(f"📦  Total products collected: {len(all_products)}")

    if not all_products:
        print("\n⚠️  No products found!")
        print("    Possible reasons:")
        print("    1. Amazon blocked the request")
        print("    2. Check your internet connection")
        print("    3. Try different keywords in config.py")
        return

    # ── Export to Excel ──
    print("\n📊 Generating Excel report...")
    filepath = create_excel_report(all_products)

    # ── High opportunity products ──
    high_score = [
        p for p in all_products
        if p.get("Profit Score", 0) >= 70
    ]

    print("\n" + "═" * 50)
    print(f"🏆  High Opportunity Products: {len(high_score)}")
    print(f"📁  Report saved to: {filepath}")
    print("═" * 50)

    # ── Show top 3 in terminal ──
    if high_score:
        top3 = sorted(
            high_score,
            key=lambda x: x.get("Profit Score", 0),
            reverse=True
        )[:3]

        print("\n🥇 TOP 3 OPPORTUNITIES RIGHT NOW:\n")
        for i, p in enumerate(top3, 1):
            print(f"  {i}. {p['Title'][:50]}...")
            print(f"     💰 Price: ${p['Price ($)']}")
            print(f"     ⭐ Rating: {p['Rating']}")
            print(f"     💬 Reviews: {p['Reviews']}")
            print(f"     🎯 Profit Score: {p['Profit Score']}/100")
            print()

    print("✅ Done! Open your Excel file to see full results.\n")


if __name__ == "__main__":
    main()
