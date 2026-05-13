import streamlit as st
import pandas as pd

# ==========================================
# STEP 1: Page Config & Data Pipeline
# ==========================================
# This must be the very first Streamlit command
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

# Initialize your master dataframe
# IMPORTANT: Replace "your_database.csv" with your actual file path!
df = load_and_clean_data("your_database.csv")


# ==========================================
# STEP 2: Sidebar Navigation & Filtering
# ==========================================
st.sidebar.title("Engine Controls")

# Create a multi-select box populated by the unique (and now cleaned) metal names
available_metals = df['metal'].unique()

selected_metals = st.sidebar.multiselect(
    "Filter by Metal:", 
    options=available_metals, 
    default=available_metals # Default to showing all
)

# Create the filtered dataframe based on the user's selection
filtered_df = df[df['metal'].isin(selected_metals)]


# ==========================================
# STEP 3: Executive Summary & Metrics
# ==========================================
st.title("Metal Sentiment Engine")

st.subheader("Market Overview")
st.info("Market sentiment is currently volatile. Copper shows downward pressure due to London warehouse pricing, while Palladium applications advance.")

st.markdown("### Latest Signals")

# Only attempt to draw metrics if there's data and a selection
if not filtered_df.empty:
    # Get the latest entry for each selected metal
    latest_data = filtered_df.drop_duplicates(subset=['metal'], keep='last')
    
    # Create dynamic columns based on how many metals are selected
    columns = st.columns(len(latest_data))
    
    for i, (index, row) in enumerate(latest_data.iterrows()):
        metal_name = row['metal']
        current_score = row['score']
        
        # Mock delta calculation (replace with actual day-over-day math later)
        mock_delta = 0.1 if current_score > 0 else -0.1 
        
        with columns[i]:
            st.metric(
                label=f"{metal_name} Sentiment", 
                value=f"{current_score:.2f}", 
                delta=f"{mock_delta:.2f}"
            )
else:
    st.warning("Please select at least one metal from the sidebar to view metrics.")


# ==========================================
# STEP 4: Visualizations
# ==========================================
st.markdown("---")
st.subheader("Sentiment Trend Over Time")

if not filtered_df.empty:
    # Pivot the table so columns are metals and rows are timestamps
    # Using pivot_table handles duplicate timestamps better than simple pivot
    chart_data = filtered_df.pivot_table(index='Timestamp', columns='metal', values='score', aggfunc='mean')
    st.line_chart(chart_data)


# ==========================================
# STEP 5: Expandable Catalyst Feed
# ==========================================
st.markdown("---")
st.subheader("Catalyst Feed")

if not filtered_df.empty:
    # Sort to show the newest catalysts first
    feed_df = filtered_df.sort_values('Timestamp', ascending=False)
    
    for index, row in feed_df.iterrows():
        # Set the color indicator based on sentiment score
        status_icon = "🟢" if row['score'] > 0 else "🔴" if row['score'] < 0 else "⚪"
        
        # Format the timestamp for clean reading
        time_str = row['Timestamp'].strftime('%b %d, %H:%M')
        
        # Create the expander title
        header = f"{status_icon} {row['metal']} | Score: {row['score']} | {time_str}"
        
        with st.expander(header):
            st.write("**AI Analysis Catalyst:**")
            st.write(row['catalyst'])
