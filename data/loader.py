import pandas as pd
import streamlit as st

SHEET_ID = "1F2CRDPbZsgZgsFBOP8i97OB5jn_VXcw78u9A0dbQe_Q"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

@st.cache_data(ttl=300) # Cache for 5 mins for performance
def fetch_and_clean_data():
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['metal'])
    
    df['metal'] = df['metal'].astype(str).str.title().str.strip()
    df['metal'] = df['metal'].replace({'Iron': 'Iron Ore', 'Aluminium': 'Aluminum'})
    
    target_col = 'Timestamp' if 'Timestamp' in df.columns else 'timestamp'
    df[target_col] = pd.to_datetime(df[target_col], errors='coerce')
    df = df.dropna(subset=[target_col]).sort_values(by=target_col, ascending=False)
    
    return df, target_col
