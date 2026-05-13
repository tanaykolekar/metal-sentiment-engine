import streamlit as st
import pandas as pd

# Set up the page
st.set_page_config(page_title="Metal Sentiment Engine", layout="wide")
st.title("📈 Industrial Metals Sentiment & Catalyst Engine")
st.markdown("An autonomous AI pipeline analyzing global news to generate market sentiment for industrial metals.")

# The public CSV export URL for your specific Google Sheet
SHEET_ID = "13sV6AHcNS6hBec1HQx33C7A_xV0A1n6NGByctdBw9Mw"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

# Cache the data for 10 minutes so it doesn't overload Google Sheets
@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(CSV_URL)
    # Ensure Timestamp is a datetime object
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    # Sort so the newest data is at the top
    df = df.sort_values(by='Timestamp', ascending=False)
    return df

try:
    df = load_data()
    
    # Create a layout with columns for the latest metrics
    st.subheader("Latest Market Signals")
    metals = df['metal'].unique()
    cols = st.columns(len(metals))
    
    for i, metal in enumerate(metals):
        # Get the most recent row for this specific metal
        latest_data = df[df['metal'] == metal].iloc[0]
        
        with cols[i]:
            st.metric(
                label=f"{metal.capitalize()} Sentiment", 
                value=latest_data['score']
            )
            st.caption(f"**Catalyst:** {latest_data['catalyst']}")

    st.divider()

    # Show the historical trend chart
    st.subheader("Sentiment Trend Over Time")
    # Pivot the data so each metal is its own line on the chart
    chart_data = df.pivot(index='Timestamp', columns='metal', values='score')
    st.line_chart(chart_data)

    # Show the raw database
    st.subheader("Raw AI Analysis Database")
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Could not load data. Error: {e}")