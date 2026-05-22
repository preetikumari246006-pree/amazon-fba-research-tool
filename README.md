# 🔍 Amazon FBA Product Research Tool

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

> **Find profitable Amazon FBA products in minutes — not hours!**
> Tools like Jungle Scout charge $49/month for this. This does it FREE.

---

## 🚀 What This Tool Does

- 🔎 Scrapes Amazon search results for any keyword
- 💰 Extracts Price, Rating, Reviews, Best Seller status
- 🎯 Calculates a **Profit Score (0-100)** for each product
- 📊 Exports a **beautiful 3-sheet Excel report** automatically
- ⚡ Researches multiple keywords in one run

---

## 📊 Excel Report Preview

| Sheet | What's Inside |
|-------|--------------|
| 📦 All Products | Every scraped product with full data |
| 🏆 Top Opportunities | High score products sorted by opportunity |
| 📊 Summary | Quick stats — averages, totals, best sellers |

---

## 🎯 Profit Score System

Our unique scoring algorithm (0-100):

| Factor | Points | Criteria |
|--------|--------|----------|
| 💰 Price | 40 pts | Sweet spot $15-$70 |
| ⭐ Rating | 30 pts | 4.0+ stars |
| 💬 Reviews | 30 pts | Under 100 = low competition |

**Score Guide:**
- 🟢 70-100 = High Opportunity
- 🟡 40-69  = Medium Opportunity  
- 🔴 0-39   = Skip This Product

---

## ⚙️ Installation

**1. Clone the repository**
```bash
git clone https://github.com/0xpreeti/amazon-fba-research-tool.git
cd amazon-fba-research-tool
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure keywords**

Open `config.py` and set your keywords:
```python
KEYWORDS = [
    "yoga mat",
    "water bottle",
    "phone stand"
]
```

**4. Run the tool**
```bash
python main.py
```

---

---

## 🛠️ Built With

- [Python 3.8+](https://python.org)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [Requests](https://pypi.org/project/requests/)
- [OpenPyXL](https://pypi.org/project/openpyxl/)

---

## 📜 License

MIT License — free to use and modify

---

## 👩‍💻 Author

Built with ❤️ for Amazon FBA sellers who want data-driven decisions

> ⭐ **Star this repo if it helped you!**
