import streamlit as st
import pandas as pd
from data.loader import fetch_and_clean_data
from components.charts import render_sentiment_ranking
from components.tables import render_interactive_table
from components.charts import render_sentiment_ranking, render_time_series
from components.market_data import render_live_ticker
from components.charts import render_sentiment_matrix, render_time_series

# 1. Page Config MUST be the first command
st.set_page_config(page_title="Metal Insights", layout="wide", page_icon="⚡")

# 2. Inject Premium CSS
with open("assets/custom.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Load Data
try:
    df, time_col = fetch_and_clean_data()
except Exception as e:
    st.error(f"Critical System Error: Database unreachable. {e}")
    st.stop()

# 4. Global Sidebar Architecture
with st.sidebar:
    st.title("⚡ Settings")
    metals = sorted([m for m in df['metal'].unique() if pd.notna(m)])
    selected_metals = st.multiselect("Active Portfolio", metals, default=metals[:5])
    
    st.markdown("---")
    st.caption("Powered by autonomous AI pipelines.")

filtered_df = df[df['metal'].isin(selected_metals)]

# 5. Application Layout Hierarchy
st.title("Commodity Sentiment Intelligence")
st.markdown("Real-time AI analysis of global macroeconomic catalysts.")

if not filtered_df.empty:
    render_live_ticker(selected_metals)
    # 6. TABBED NAVIGATION (Crucial for SaaS feel)
    tab1, tab2, tab3 = st.tabs(["📊 Executive Dashboard", "📈 Trend Analysis", "🗄️ Raw AI Database"])
    
    with tab1:
        st.subheader("Market Movers")
        # Get the top 4 most volatile/recent signals
        latest_signals = filtered_df.drop_duplicates(subset=['metal'], keep='first').head(4)
        
        cols = st.columns(4)
        for i, row in enumerate(latest_signals.itertuples()):
            with cols[i % 4]:
                # FIX: Add + and - signs so Streamlit colors the arrows correctly
                delta_str = "+ Bullish" if row.score > 0 else "- Bearish" if row.score < 0 else "Neutral"
                
                st.metric(
                    label=f"{row.metal}", 
                    value=f"{row.score}",
                    delta=delta_str,
                    delta_color="normal" if row.score != 0 else "off"
                )
                # Truncate string gracefully
                cat_text = str(row.catalyst)
                st.caption(f"{cat_text[:80]}..." if len(cat_text) > 80 else cat_text)
        
        st.markdown("<br>", unsafe_allow_html=True) # Spacing
        render_sentiment_matrix(filtered_df)

    with tab2:
        st.subheader("Time-Series Volatility")
        # Pass the filtered dataframe and the timestamp column name
        render_time_series(filtered_df, time_col)

    with tab3:
        st.subheader("Interactive Audit Log")
        render_interactive_table(filtered_df)

else:
    st.warning("No data available for the selected portfolio.")
