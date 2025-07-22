# from serpapi import *

# import streamlit as st
# import pandas as pd



# def search_and_extract(query, location="usa", num_results=10):
#     urls = search_with_fallback(query, location, num_results)
   

#     data = []
#     for url, _ in urls:
#         info = extract_info_from_page(url)
#         data.append(info)
#         time.sleep(random.uniform(2, 5))
#     return pd.DataFrame(data)  # We'll modularize scraping logic here

# st.set_page_config(page_title="Smart Web Scraper", layout="wide")

# st.title("🌐 Smart Web Scraper (Google → Bing → DuckDuckGo)")

# with st.sidebar:
#     st.header("🔎 Search Settings")
#     query = st.text_input("Search Query", value="digital marketing")
#     location = st.text_input("Search Location", value="usa")
#     num_results = st.slider("Number of Results", min_value=5, max_value=30, value=10)

#     if st.button("Start Scraping"):
#         with st.spinner("🔄 Scraping in progress..."):
#             result_df = search_and_extract(query, location, num_results)

#         if not result_df.empty:
#             st.success("✅ Scraping completed!")
#             st.subheader("📋 Extracted Results")
#             st.dataframe(result_df)

#             csv = result_df.to_csv(index=False).encode("utf-8")
#             st.download_button("📥 Download CSV", csv, file_name="scraped_results.csv", mime="text/csv")
#         else:
#             st.error("❌ No data found. Try a different query or check your connection.")



import streamlit as st
import pandas as pd
import time
import random
from serpapi import search_google, search_bing, extract_info_from_page 

def search_and_extract(query, location="usa", num_results=10):

    g_urls = search_google(query, location, num_results)
    print(f"Google URLs: {g_urls}")

    # Step 2: If Google returned no results, fallback to Bing
    if not g_urls:
        b_urls = search_bing(query, location, num_results)  # Make sure Bing accepts 3 args
        print(f"Bing URLs: {b_urls}")
        urls = b_urls if b_urls else []
    else:
        urls = g_urls

    data = []

    for url, _ in urls:
        info = extract_info_from_page(url)
        print(f"Extracted info: {info}")
        data.append(info)
        time.sleep(random.uniform(2, 3))

    return pd.DataFrame(data)


# 🌐 Streamlit Config
st.set_page_config(page_title="Smart Web Scraper", layout="wide")
st.markdown("<h1 style='text-align: center;'>🌐 Ranktunez Smart Seo platform </h1>", unsafe_allow_html=True)

# 🚀 Top horizontal input section
col1, col2, col3 = st.columns([3, 3, 3])
with col1:
    query = st.text_input("🔍 Search Query", "digital marketing")
with col2:
    location = st.selectbox("📍 Location", ["usa", "uk", "india", "canada", "australia"])
with col3:
    num_results = st.slider("📊 Number of Results", 5, 30, 10)

# 🚀 Scrape Button (Centered Below)
center_button = st.columns([4, 2, 4])
with center_button[1]:
    run = st.button("🚀 Start Scraping")

# 🔄 Trigger scrape
if run:
    with st.spinner("Scraping in progress..."):
        df = search_and_extract(query, location, num_results)

    if not df.empty:
        print(f"Scraped Data: {df}")

        # 📋 Show results in center
        st.markdown("### 📋 Extracted Results")
        st.dataframe(df, use_container_width=True)

        # 📥 Download
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, "scraped_results.csv", "text/csv")
    else:
        st.error("❌ No results found.")
