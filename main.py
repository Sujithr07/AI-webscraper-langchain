import streamlit as st

st.title("AI Web Scraper")
url= st.text_input("Paste the URL: ")

if st.button("Scrape"):
    st.write("Scraping the website")