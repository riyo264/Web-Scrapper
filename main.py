import streamlit as st

def render_header():
    st.title("Amazon Scrapper")
    st.caption("Enter your ASIN to get product information.")

def render_input():
    asin = st.text_input("ASIN", placeholder="Enter ASIN here")
    geo = st.text_input("Zip/Postal Code", placeholder="e.g., 831014")
    domain = st.selectbox("Domain", ["com", "co.uk", "de", "in", "fr", "it", "es", "ca", "ae"])
    return asin.strip(), geo.strip(), domain

def main():
    st.set_page_config(page_title="Amazon Scrapper", page_icon=":mag:")
    render_header()
    asin, geo, domain = render_input()
    
    if st.button("Scrape Product") and asin:
        with st.spinner("Scraping product information..."):
            st.write("Scrape")
            # TODO: scrape product
        st.success("Product information scraped successfully!")

if __name__ == "__main__":
    main()
