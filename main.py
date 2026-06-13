import streamlit as st
from scrape import scrape_web

st.title("AI Web Scraper")
url= st.text_input("Paste the URL: ")

if st.button("Scrape"):
    st.write("Scraping the website")
    result= scrape_web(url)
    st.text(result)