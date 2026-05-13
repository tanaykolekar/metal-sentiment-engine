import streamlit as st
import pandas as pd
# import plotly.express as px # Optional, but recommended for Step 4

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(page_title="Metal Sentiment Engine", layout="wide")

@st.cache_data
def load_and_clean_data(file_path):
    # Load your sheet/csv
    df = pd.read_csv(file_path) 
    
    # Standardize Metal Names to Title Case (Fixes the Copper/copper issue)
    df['metal'] = df['metal'].astype(str).str.title()
    
    # Convert timestamps to proper datetime objects
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Sort by time so charts render chronologically
    df = df.sort_values('Timestamp')
    
    return df

# Initialize your dataframe
df = load_and_clean_data("your_database.csv")
