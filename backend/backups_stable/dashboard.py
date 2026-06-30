import streamlit as st
import requests

# 1. Page Configuration for a clean premium dark appearance
st.set_page_config(
    page_title="StockAlert AI Engine",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom structural dark styles
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 24px !important; }
    div.stButton > button { background-color: #10b981 !important; color: #020617 !important; border-radius: 8px; font-weight: bold; border: none; }
    div.stButton > button:hover { background-color: #059669 !important; }
    </style>
""", unsafe_allow_html=True)

# Header Title
st.title("📈 StockAlert AI Engine")
st.caption("Multi-timeframe algorithmic strategy dashboard")
st.markdown("---")

# 2. Search Field Section
query = st.text_input(
    label="AI Search Query",
    placeholder="e.g., show me high margin companies with low leverage or try a single ticker like 'SOFI'...",
    label_visibility="collapsed"
)

if st.button("Analyze Query") and query.strip():
    with st.spinner("Analyzing custom metrics pool..."):
        try:
            cleaned_query = query.strip().upper()
            stocks = []
            scan_rejected = False
            
            # Handle direct single ticker entry vs natural language phrases smoothly
            if len(cleaned_query) <= 5 and cleaned_query.isalpha():
                url = f"http://127.0.0.1:8000/scan/{cleaned_query.lower()}"
                response = requests.get(url)
                
                if response.status_code == 200:
                    res_data = response.json()
                    if res_data.get("status") == "REJECTED":
                        st.error(f"Asset Scan Rejected: {res_data.get('reason', 'Incomplete data payload from financial endpoints.')}")
                        scan_rejected = True
                    else:
                        stocks = [res_data]
            else:
                # Standard NLP search route
                url = f"http://127.0.0.1:8000/search?q={query}"
                response = requests.get(url)
                if response.status_code == 200:
                    stocks = response.json().get("matches", [])

            # Only show empty warning if the single stock scan didn't explicitly throw an error box
            if not stocks and not scan_rejected:
                st.warning("No matched stocks discovered in your candidate pool matching this specific intent currently.")
            
            # Render results in a structural grid layout cleanly
            for stock in stocks:
                if not stock or not stock.get("ticker"):
                    continue
                    
                with st.container():
                    # Create an isolated styling box for each stock card
                    st.markdown(f"""
                        <div style='background-color: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; margin-bottom: 20px;'>
                            <h2 style='margin:0; color: white; display: inline-block;'>{stock.get('ticker')}</h2>
                            <span style='background-color: #064e3b; color: #34d399; padding: 3px 8px; border-radius: 5px; margin-left: 12px; font-size: 12px;'>{stock.get('signal', 'HOLD/NEUTRAL')}</span>
                            <span style='background-color: #1e293b; color: #22d3ee; padding: 3px 8px; border-radius: 5px; margin-left: 6px; font-size: 12px;'>AI Score: {stock.get('ai_growth_score', 'N/A')}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Populate technical breakdown columns inside the container
                    metrics = stock.get("fundamental_metrics", {}) or {}
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Price", f"${metrics.get('price', 'N/A')}")
                    with col2:
                        gm = metrics.get('gross_margin', 'N/A')
                        st.metric("Gross Margin", f"{f'{gm:.2f}%' if isinstance(gm, (int, float)) else f'{gm}%'}")
                    with col3:
                        st.metric("Debt / Equity", f"{metrics.get('debt_to_equity', 'N/A')}")
                        
                    # Clean up indicator styling strings safely
                    raw_strengths = stock.get("strengths", []) or stock.get("reasons_summary", []) or []
                    cleaned_strengths = [str(s).replace("✔", "").strip() for s in raw_strengths if s]
                    
                    if cleaned_strengths:
                        st.markdown("**Strategy Passing Indicators:**")
                        st.write(" | ".join([f"✔️ {s}" for s in cleaned_strengths]))
                    st.markdown("---")
                    
        except Exception as e:
            st.error(f"Could not connect to FastAPI Backend engine: {str(e)}")