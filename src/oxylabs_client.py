import json
import os
import time 
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

OXYLABS_BASE_URL = "https://realtime.oxylabs.io/v1/queries"

def extract_content(payload):
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
        "query": asin,                                      # PAYLOAD IS DEFINED HERE
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