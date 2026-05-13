import streamlit as st
import pandas as pd

# Set up the page for a wider, cleaner layout
st.set_page_config(page_title="Metal Sentiment Engine", layout="wide")
st.title("📈 Industrial Metals Sentiment & Catalyst Engine")
st.markdown("An autonomous AI pipeline analyzing global news to generate market sentiment for industrial metals.")

SHEET_ID = "1F2CRDPbZsgZgsFBOP8i97OB5jn_VXcw78u9A0dbQe_Q"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

@st.cache_data(ttl=60) 
def load_data():
    df = pd.read_csv(CSV_URL)
    
    # 1. Clean headers
    df.columns = df.columns.str.strip()
    
    # 2. Remove empty rows
    df = df.dropna(subset=['metal'])
    df = df[df['metal'] != ""]

    # 3. NORMALIZATION: Force all metals to Title Case (e.g., 'copper' -> 'Copper')
    df['metal'] = df['metal'].astype(str).str.title().str.strip()

    # 4. Handle Timestamps
    target_col = 'Timestamp' if 'Timestamp' in df.columns else 'timestamp'
    if target_col in df.columns:
        df[target_col] = pd.to_datetime(df[target_col], errors='coerce')
        df = df.dropna(subset=[target_col]) # Drop if timestamp failed to parse
        df = df.sort_values(by=target_col, ascending=False)
    
    return df, target_col

try:
    df, time_col = load_data()
    
    st.subheader("Latest Market Signals")
    
    metals = [m for m in df['metal'].unique() if pd.notna(m)]
    
    if len(metals) > 0:
        # UX UPGRADE: Chunk the metrics into rows of 4 so they don't squish
        num_columns = 4
        for i in range(0, len(metals), num_columns):
            cols = st.columns(num_columns)
            chunk = metals[i:i + num_columns]
            
            for j, metal in enumerate(chunk):
                metal_df = df[df['metal'] == metal]
                if not metal_df.empty:
                    latest_data = metal_df.iloc[0]
                    
                    # Truncate overly long AI text to keep the UI clean
                    catalyst_text = str(latest_data['catalyst'])
                    if len(catalyst_text) > 90:
                        catalyst_text = catalyst_text[:87] + "..."
                        
                    with cols[j]:
                        st.metric(label=f"{metal} Sentiment", value=latest_data['score'])
                        st.caption(f"**Catalyst:** {catalyst_text}")
            
            # Add a subtle visual divider between rows of metrics
            st.write("---")

        st.subheader("Sentiment Trend Over Time")
        
        # CHART UPGRADE: Pivot and forward-fill so lines connect properly
        chart_df = df.copy()
        chart_df.set_index(time_col, inplace=True)
        chart_data = chart_df.pivot(columns='metal', values='score')
        
        # ffill() carries the last known score forward until a new one drops
        chart_data = chart_data.ffill() 
        
        st.line_chart(chart_data)

        st.subheader("Raw AI Analysis Database")
        st.dataframe(df, width='stretch') 
        
    else:
        st.info("The database is currently empty. Waiting for n8n to send data...")

except Exception as e:
    st.error(f"Could not load data. Error: {e}")
