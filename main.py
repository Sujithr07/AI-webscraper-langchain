import streamlit as st
from scrape import scrape_web
from parse import parse_content

st.title("AI Web Scraper")
url= st.text_input("Paste the URL: ")
query= st.text_input("What would you like to know?", value="Summarize the main points")

if st.button("Scrape"):
    st.write("Scraping the website...")
    result= scrape_web(url)
    st.write("Content retrieved. Processing with AI...")
    
    st.subheader("Cleaned Content")
    st.text(result[:500] + "..." if len(result) > 500 else result)
    
    st.subheader("AI Analysis")
    with st.spinner("Analyzing..."):
        ai_response= parse_content(result, query)
        st.write(ai_response)