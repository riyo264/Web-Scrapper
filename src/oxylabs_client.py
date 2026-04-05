import json
import os
import time 
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


OXYLABS_BASE_URL = "https://realtime.oxylabs.io/v1/queries"


def extract_content(payload):                                                           # PAYLOAD IS DEFINED BELOW IN THE scrape_product_details FUNCTION
    if isinstance(payload, dict):
        if "results" in payload and isinstance(payload["results"], list) and payload["results"]:
            first = payload["results"][0]
            if isinstance(first, dict) and "content" in first:                        # IT EXTRACTS THE CONTENT FROM THE FIRST RESULT IF AVAILABLE AND HANLES THE EDGE CASES
                return first["content"] or {}                                         # IF THE CONTENT IS EMPTY OR NULL, IT RETURNS AN EMPTY DICTIONARY INSTEAD OF NONE
        if "content" in payload:
            return payload.get("content", {})
        
    return payload


def post_query(payload):
    username = os.getenv("OXYLABS_USERNAME")
    password = os.getenv("OXYLABS_PASSWORD")

    response = requests.post(OXYLABS_BASE_URL, auth=(username, password), json=payload)      # IT SENDS A POST REQUEST TO THE OXYLABS API WITH BASIC 
    response_json = response.json()                                                          # AUTHENTICATION USING THE USERNAME AND PASSWORD FROM THE ENVIRONMENT VARIABLES, AND THE PAYLOAD AS JSON DATA.

    return response_json


def normalize_product(content):
    category_path = []
    if content.get("category_path"):
        category_path = [cat.strip() for cat in content["category_path"] if cat]

    return {
        "asin": content.get("asin"),
        "url": content.get("url"),
        "brand": content.get("brand"),
        "title": content.get("title"),
        "stock": content.get("stock"),                                                          # OXYLABS SENDS THE PRODUCTS INFORMATION WITH A BROAD VARIETY OF FIELDS
        "categories": content.get("category", []) or content.get("categories", []),             # SO THIS FUNCTION ONLY RETURN THOSE INFORMATION WHICH ARE USEFUL TO US HENCE NORMALIZING THE DATA
        "price": content.get("price"),
        "rating": content.get("rating"),
        "category_path": category_path,
        "product_overview": content.get("product_overview", []),
        "images": content.get("images", []),
        "currency": content.get("currency"),
        "buy_box": content.get("buy_box", []),
    }


def scrape_product_details(asin, geo_location, domain):
    payload = {
        "source": "amazon_product",
        "query": asin,                                                                       # PAYLOAD IS DEFINED HERE
        "geo_location": geo_location,
        "domain": domain,
        "parse": True
    }
    raw = post_query(payload)
    content = extract_content(raw)
    normalized = normalize_product(content)
    if not normalized.get("asin"):
        normalized["asin"] = asin

    normalized["amazon_domain"] = domain
    normalized["geo_location"] = geo_location
    return normalized


def clean_product_name(title):                                                               # THIS FUNCTION CLEANS THE PRODUCT TITLE BY REMOVING ANY EXTRA INFORMATION 
    if "-" in title:
        title = title.split("-")[0]
    if "|" in title:
        title = title.split("|")[0]
    return title.strip()


def extract_search_results(content):
    items = []
    if not isinstance(content, dict):
        return items
    
    if "results" in content:
        results = content["results"]
        if isinstance(results, dict):
            if "organic" in results:
                items.extend(results["organic"])
            if "paid" in results:
                items.extend(results["paid"])
    elif "products" in content and isinstance(content["products"], list):
        items.extend(content["products"])
    return items


def normalize_search_result(item):                                                          # NORMALIZE THE COMPETITOR DATA TO EXTRACT ONLY THE ASIN, TITLE, CATEGORY, PRICE AND RATING
    asin = item.get("asin") or item.get("product_asin")
    title = item.get("title")
    if not (asin and title):
        return None                                    

    return {
        "asin": asin,
        "title": title,
        "category": item.get("category"),
        "price": item.get("price"),
        "rating": item.get("rating"),
    }


def search_competitors(query_title, domain, categories, pages=1, geo_location=""):        # THIS FUNCTION SEARCH FOR COMPETITORS AND SENDS ALL THE DATA TO THE EXTRACT_SEARCH_RESULTS AND NORMALIZE_SEARCH_RESULT FUNCTION TO PERFORM THEIR TASKS
    st.write(":mag: Searching for competitors...")

    search_title = clean_product_name(query_title)
    results = []
    seen_asins = set()

    strategies = ["featured", "price_asc", "price_desc", "avg_rating"]

    for sort_by in strategies:
        for page in range(1, max(1, pages) + 1):
            payload = {
                "source": "amazon_search",
                "query": search_title,
                "parse": True,
                "domain": domain,
                "geo_location": geo_location,
                "sort_by": sort_by,
                "page": page
            }
            
            if categories and categories[0]:                                             # CHECK IF THE FIRST CATEGORY IS NOT EMPTY
                payload["refinements"] = {"category": categories[0]}                     # ADD THE CATEGORY TO THE PAYLOAD IF AVAILABLE

            content = extract_content(post_query(payload))
            items = extract_search_results(content)

            for item in items:
                result = normalize_search_result(item)
                if result and result["asin"] not in seen_asins:
                    seen_asins.add(result["asin"])
                    results.append(result)

            time.sleep(0.5)                                                             # ADD A SHORT DELAY BETWEEN REQUESTS TO AVOID HITTING RATE LIMITS

    st.write(f"Found {len(results)} competitors.")
    return results


def scrape_multiple_products(asins, geo_location, domain):                             # OUTPUT THE SCRAPING PROGRESS AND SCRAPE MULTIPLE PRODUCTS BASED ON THE ASINS PROVIDED, AND HANDLE ANY ERRORS THAT MAY OCCUR DURING THE SCRAPING PROCESS
    st.write(":mag: Scraping details...")
    products = []
    
    progress_text = st.empty()
    progress_bar = st.progress(0)
    total = len(asins)

    for idx, a in enumerate(asins, 1):
        try:
            progress_text.write(f"Scraping {idx}/{total} - ASIN: {a}")
            progress_bar.progress(idx / total)

            product = scrape_product_details(a, geo_location, domain)
            products.append(product)
            progress_text.write(f"✅Found {product.get('title', a)}")
        except Exception as e:
            progress_text.write(f"❌Error scraping ASIN {a}")
            continue
        time.sleep(0.1)

    progress_text.empty()
    progress_bar.empty()

    st.write(f"✅ Successfully scraped {len(products)} out of {total} competitors.")
    return products