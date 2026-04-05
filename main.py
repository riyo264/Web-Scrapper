import streamlit as st
from src.oxylabs_client import scrape_product_details
from src.services import scrape_and_store_product

def render_header():
    st.title("Amazon Web Scrapper")
    st.caption("Enter your ASIN to get product information.")


def render_input():
    asin = st.text_input("ASIN", placeholder="Enter ASIN here")
    geo = st.text_input("Zip/Postal Code", placeholder="e.g., 831014")
    domain = st.selectbox("Domain", ["com", "co.uk", "de", "in", "fr", "it", "es", "ca", "ae"])
    return asin.strip(), geo.strip(), domain


def render_product_card(product): 
    with st.container(border=True):
        cols = st.columns([1, 2])

        try:
            images = product.get("images", [])
            if images and len(images) > 0:
                cols[0].image(images[0], width=200)
            else: 
                cols[0].write("No image available")

        except:
            cols[0].write("Error loading image")

        with cols[1]:
            st.subheader(product.get("title") or product["asin"])
            info_cols = st.columns(3)
            currency = product.get("currency", "")
            price = product.get("price", "-")
            info_cols[0].metric("Price", f"{currency} {price}" if currency else price)
            info_cols[1].write(f"Brand: {product.get('brand', '-')}") 
            info_cols[2].write(f"Product: {product.get('product', '-')}")

            domain_info = f"amazon.{product.get('domain_info', 'com')}"
            geo_info = product.get("geo_location", "-")
            st.caption(f"Domain: {domain_info} | Geo: {geo_info}")

            st.write(product.get("url", ""))
            if st.button("Start analyzing competitors", key=f"analyze_{product['asin']}"):
                st.session_state["analyzing_asin"] = product["asin"]

def main():
    st.set_page_config(page_title="Amazon Web Scrapper", page_icon=":mag:", layout = "wide")
    render_header()
    asin, geo, domain = render_input()
    
    if st.button("Scrape Product") and asin:
        with st.spinner("Scraping product information..."):
            product = scrape_and_store_product(asin, geo, domain)
        st.success("Product information scraped and stored successfully!")
        render_product_card(product)

if __name__ == "__main__":
    main()
