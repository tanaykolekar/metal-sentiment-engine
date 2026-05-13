import streamlit as st
import pandas as pd

# The Sheet ID from your screenshot (image_477be2.png)
SHEET_ID = "1F2CRDPbZsgZgsFBOP8i97OB5jn_VXcw78u9A0dbQe_Q"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

@st.cache_data(ttl=60) 
def load_data():
    df = pd.read_csv(CSV_URL)
    
    # 1. Clean headers
    df.columns = df.columns.str.strip()
    
    # 2. FIX: Remove any rows where the 'metal' column is empty or NaN
    # This prevents the "out-of-bounds" error from row 6 in your sheet
    df = df.dropna(subset=['metal'])
    df = df[df['metal'] != ""]

    # 3. Handle Timestamps
    target_col = 'Timestamp' if 'Timestamp' in df.columns else 'timestamp'
    if target_col in df.columns:
        df[target_col] = pd.to_datetime(df[target_col])
        df = df.sort_values(by=target_col, ascending=False)
    
    return df, target_col

try:
    df, time_col = load_data()
    
    st.subheader("Latest Market Signals")
    
    # Filter for valid unique metals
    metals = [m for m in df['metal'].unique() if pd.notna(m)]
    
    if len(metals) > 0:
        cols = st.columns(len(metals))
        for i, metal in enumerate(metals):
            # Get the most recent row for this specific metal
            metal_df = df[df['metal'] == metal]
            
            if not metal_df.empty:
                latest_data = metal_df.iloc[0]
                with cols[i]:
                    st.metric(label=f"{metal.capitalize()} Sentiment", value=latest_data['score'])
                    st.caption(f"**Catalyst:** {latest_data['catalyst']}")

        st.divider()
        st.subheader("Sentiment Trend Over Time")
        chart_data = df.pivot(index=time_col, columns='metal', values='score')
        st.line_chart(chart_data)

        st.subheader("Raw AI Analysis Database")
        # Updated 'width' parameter to fix the log warning
        st.dataframe(df, width='stretch') 
    else:
        st.info("The database is currently empty. Waiting for n8n to send data...")

except Exception as e:
    st.error(f"Could not load data. Error: {e}")
