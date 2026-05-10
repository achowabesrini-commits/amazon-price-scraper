# amazon-price-scraper
Amazon Price Scraper built with Python, Requests, and BeautifulSoup. Optimized for speed and bypassing 503 errors through advanced Header management, avoiding the overhead and detection risks of Selenium.
# Amazon Price Scraper 🚀

A high-performance web scraper designed to extract product data from Amazon efficiently.

## 🛠️ Tech Stack
* **Python**: Core logic.
* **Requests & BeautifulSoup4**: Used for fast, lightweight HTML parsing.
* **Pandas**: Data structuring and CSV export.

## 💡 Key Features & Decisions
* **Bypassing Anti-Bot measures**: Implemented custom HTTP Headers to avoid Error 503 and Bot detection.
* **Efficiency First**: Chose BeautifulSoup over Selenium to achieve 10x faster execution and lower memory footprint.
* **Reliability**: Error handling for missing prices, ratings, or changes in the web structure.

## 📊 Output
The script generates a structured `.csv` file with:
- Product Name
- Price (USD)
- Rating
- Review Count
- Timestamp
