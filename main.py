import streamlit as st
from scrape import scrape_web
from parse import parse_content

st.set_page_config(page_title="AI Web Scraper", layout="wide", initial_sidebar_state="expanded")

st.title("AI Web Scraper")

with st.sidebar:
    st.header("Settings")
    st.info("Configure your scraping and analysis preferences")
    use_proxy = st.checkbox("Use Bright Data Proxy", value=True)
    clean_content = st.checkbox("Clean HTML Content", value=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input")
    url = st.text_input("Website URL", placeholder="https://example.com")

with col2:
    st.subheader("Analysis Query")
    query = st.text_area("What would you like to know?", value="Summarize the main points", height=100)

st.divider()

if st.button("Start Scraping", use_container_width=True):
    if not url:
        st.error("Please enter a valid URL")
    elif not query.strip():
        st.error("Please enter an analysis query")
    else:
        try:
            with st.container():
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Initializing browser...")
                progress_bar.progress(20)
                
                result = scrape_web(url, clean=clean_content)
                status_text.text("Content retrieved")
                progress_bar.progress(50)
                
                status_text.text("Processing with AI...")
                progress_bar.progress(75)
                
                ai_response = parse_content(result, query)
                progress_bar.progress(100)
                status_text.text("Analysis complete")
                
                st.success("Scraping and analysis completed successfully")
                
                st.divider()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.expander("View Cleaned Content", expanded=True):
                        preview_length = 1000
                        preview = result[:preview_length] + "..." if len(result) > preview_length else result
                        st.text(preview)
                        st.caption(f"Content length: {len(result)} characters")
                
                with col2:
                    with st.expander("View Full Analysis", expanded=True):
                        st.markdown(ai_response)
                
                st.divider()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Content Size", f"{len(result)} chars")
                with col2:
                    st.metric("Status", "Complete")
                with col3:
                    st.metric("Query Type", "Analysis")
        
        except ValueError as e:
            st.error(f"Invalid input: {str(e)}")
        except TimeoutError as e:
            st.error(f"Timeout: {str(e)}")
        except Exception as e:
            st.error(f"Error: {str(e)}")