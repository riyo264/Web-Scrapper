# Web-Scrapper: Amazon Market Intelligence Tool
This repository contains a specialized Amazon Market Analysis & Competitor Intelligence tool. Built with Python and Streamlit, it leverages the Oxylabs Real-Time Scraper API to extract product data and utilizes OpenAI's GPT-4 to provide strategic market positioning and pricing recommendations.

<br>

# 🚀 Key Features
- Targeted Scraping: Extract detailed product information (price, rating, stock, images) using an Amazon ASIN, specific Geo-location (Zip Code), and Domain.
- Automated Competitor Discovery: Automatically identifies top competitors by searching across multiple strategies: "Featured," "Price Ascending/Descending," and "Average Rating."
- AI-Powered Insights: Integrates with LangChain and GPT-4 to generate a Market Analyst report, including:

  - Executive Summary
  - Market Positioning
  - Competitor Key Points
  - Actionable Recommendations

- Local Data Persistence: Uses TinyDB for a lightweight, document-oriented local database to store scraped results and avoid redundant API calls.
- Streamlit UI: A clean, multi-page web interface for managing scraped products and triggering deep-dive analyses.
<br>

# 🛠️ Tech Stack
  - Frontend: Streamlit
  - Orchestration: LangChain
  - LLM: OpenAI GPT-4
  - Data Source: Oxylabs Real-Time Scraper
  - Database: TinyDB
  - Language: Python 3.12

<br> 

# 🚦 Getting Started
**1. Prerequisites**
  - Python 3.12+
  - Oxylabs API Credentials (Username/Password)
  - OpenAI API Key

**2. Installation**
  ```
    # Clone the repository
    git clone https://github.com/your-username/web-scrapper.git
    cd web-scrapper
    # Install dependencies (using pip)
    pip install -r requirements.txt
  ```
**3. Configuration**
Rename `.env.example` to `.env` and fill in your credentials:
  ```
    OXYLABS_USERNAME="your_oxylabs_username"
    OXYLABS_PASSWORD="your_oxylabs_password"
    OPENAI_API_KEY="your_openai_api_key"
  ```

**4. Running the App**
```
streamlit run main.py
```
<br>

# 📖 Usage Guide
  - **Scrape Product**: Enter a target ASIN, specify the Zip Code (for localized pricing), and select the Domain (e.g., .in for India, .com for US).
  - **Browse Inventory**: View your local database of scraped products in the "Scraped Products" gallery.
  - **Find Competitors**: Click "Start analyzing competitors" on a product card to trigger a multi-strategy search for similar listings.
  - **AI Analysis**: Click "Analyze with LLM" to send the consolidated product and competitor data to GPT-4 for a professional market report.
<br>

# ⚠️ Disclaimer
This tool is for educational and research purposes. Please ensure your scraping activities comply with Amazon's Terms of Service and Oxylabs' usage policies.
