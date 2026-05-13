import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Metal Sentiment Engine", layout="wide", page_icon="📈")
st.title("📈 Industrial Metals Sentiment & Catalyst Engine")
st.markdown("An autonomous AI pipeline analyzing global news to generate market sentiment.")

SHEET_ID = "1F2CRDPbZsgZgsFBOP8i97OB5jn_VXcw78u9A0dbQe_Q"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

@st.cache_data(ttl=60) 
def load_data():
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip()
    df = df.dropna(subset=['metal'])
    df = df[df['metal'] != ""]

    # 2. STRICT NORMALIZATION: Map rogue AI outputs to clean categories
    df['metal'] = df['metal'].astype(str).str.title().str.strip()
    metal_mapping = {
        'Iron': 'Iron Ore',
        'Aluminium': 'Aluminum'
    }
    df['metal'] = df['metal'].replace(metal_mapping)

    target_col = 'Timestamp' if 'Timestamp' in df.columns else 'timestamp'
    if target_col in df.columns:
        df[target_col] = pd.to_datetime(df[target_col], errors='coerce')
        df = df.dropna(subset=[target_col])
        df = df.sort_values(by=target_col, ascending=False)
    
    return df, target_col

try:
    df, time_col = load_data()
    metals = [m for m in df['metal'].unique() if pd.notna(m)]
    
    if len(metals) > 0:
        # 3. INTERACTIVITY: Add a Sidebar Filter
        st.sidebar.header("⚙️ Dashboard Controls")
        st.sidebar.markdown("Filter the dashboard by specific metals.")
        selected_metals = st.sidebar.multiselect(
            "Select Metals to Display:",
            options=sorted(metals),
            default=sorted(metals) # Selects all by default
        )
        
        # Filter the dataframe based on user selection
        filtered_df = df[df['metal'].isin(selected_metals)]
        
        if not filtered_df.empty:
            st.subheader("Latest Market Signals")
            
            num_columns = 4
            for i in range(0, len(selected_metals), num_columns):
                cols = st.columns(num_columns)
                chunk = selected_metals[i:i + num_columns]
                
                for j, metal in enumerate(chunk):
                    metal_df = filtered_df[filtered_df['metal'] == metal]
                    if not metal_df.empty:
                        latest_data = metal_df.iloc[0]
                        catalyst_text = str(latest_data['catalyst'])
                        if len(catalyst_text) > 90:
                            catalyst_text = catalyst_text[:87] + "..."
                            
                        with cols[j]:
                            st.metric(label=f"{metal} Sentiment", value=latest_data['score'])
                            st.caption(f"**Catalyst:** {catalyst_text}")
                
                st.write("---")

            # 4. BETTER VISUALIZATION: Current Sentiment Bar Chart
            st.subheader("Current Market Sentiment Ranking")
            st.markdown("Average sentiment of the most recent news batch.")
            
            # Calculate the average sentiment for the selected metals
            avg_sentiment = filtered_df.groupby('metal')['score'].mean().sort_values(ascending=False)
            st.bar_chart(avg_sentiment)

            st.subheader("Raw AI Analysis Database")
            st.dataframe(filtered_df, width='stretch') 
        else:
            st.warning("Please select at least one metal from the sidebar.")
            
    else:
        st.info("The database is currently empty. Waiting for n8n to send data...")

except Exception as e:
    st.error(f"Could not load data. Error: {e}")
