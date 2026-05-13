import streamlit as st
import pandas as pd

# The NEW Sheet ID from your screenshot (image_477be2.png)
SHEET_ID = "1F2CRDPbZsgZgsFBOP8i97OB5jn_VXcw78u9A0dbQe_Q"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

@st.cache_data(ttl=60) # Reduced to 1 minute for testing
def load_data():
    df = pd.read_csv(CSV_URL)
    
    # CLEANING: Strip hidden spaces from headers and make them case-insensitive
    df.columns = df.columns.str.strip()
    
    # Debugging: If it still fails, this will show you what columns exist
    # st.write("Columns found:", list(df.columns)) 

    # Look for timestamp regardless of 'T' or 't'
    target_col = 'Timestamp' if 'Timestamp' in df.columns else 'timestamp'
    
    if target_col in df.columns:
        df[target_col] = pd.to_datetime(df[target_col])
        df = df.sort_values(by=target_col, ascending=False)
    
    return df, target_col

try:
    df, time_col = load_data()
    
    st.subheader("Latest Market Signals")
    metals = df['metal'].unique()
    cols = st.columns(len(metals))
    
    for i, metal in enumerate(metals):
        latest_data = df[df['metal'] == metal].iloc[0]
        with cols[i]:
            st.metric(label=f"{metal.capitalize()} Sentiment", value=latest_data['score'])
            st.caption(f"**Catalyst:** {latest_data['catalyst']}")

    st.divider()
    st.subheader("Sentiment Trend Over Time")
    chart_data = df.pivot(index=time_col, columns='metal', values='score')
    st.line_chart(chart_data)

    st.subheader("Raw AI Analysis Database")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Could not load data. Error: {e}")
