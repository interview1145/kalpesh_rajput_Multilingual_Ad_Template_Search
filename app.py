import streamlit as st
import requests

st.set_page_config(page_title="Ad Template Search", layout="wide")

st.title("🔍 Multilingual Ad Template Search")

# Sidebar
st.sidebar.header("Search Settings")
# FIXED: Added http:// and the correct port
base_url = st.sidebar.text_input("FastAPI Base URL", value="http://127.0.0.1:8000")
top_k = st.sidebar.slider("Number of results", 1, 20, 5)

query = st.text_input("Enter your search query:", placeholder="e.g., Summer sale for shoes")

if query:
    # Ensure the URL is correctly formatted
    search_endpoint = f"{base_url.rstrip('/')}/search"
    
    with st.spinner("Searching..."):
        try:
            payload = {"query": query, "top_k": top_k}
            response = requests.post(search_endpoint, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                
                st.success(f"Found {len(results)} relevant templates")
                
                for item in results:
                    with st.container():
                        st.markdown(f"### {item['title']}")
                        col1, col2, col3 = st.columns([2, 1, 1])
                        with col1:
                            st.write(f"**Description:** {item['description']}")
                        with col2:
                            st.write(f"**Category:** {item['category']}")
                            st.write(f"**Created:** {item['created_at'][:10]}")
                        with col3:
                            st.metric("Rank Score", f"{item['rank_score']:.2f}")
                            st.write(f"**Usage:** {item['usage_count']}")
                        st.divider()
            else:
                st.error(f"Backend Error: {response.status_code}")
                st.json(response.json())
                
        except requests.exceptions.MissingSchema:
            st.error("Invalid URL. Make sure it starts with 'http://'")
        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to FastAPI at {search_endpoint}. Is main.py running?")
