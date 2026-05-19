import streamlit as st
import plotly.express as px

def render_executive_briefing(df):
    """Generates an algorithmic text summary of the market."""
    st.markdown("### 📰 Algorithmic Morning Briefing")
    st.markdown("Automated synthesis of the most critical market catalysts driving today's volatility.")
    
    # Get the single most recent article for each metal
    latest_df = df.drop_duplicates(subset=['metal'], keep='first')
    
    bullish = latest_df[latest_df['score'] >= 0.3].sort_values(by='score', ascending=False)
    bearish = latest_df[latest_df['score'] <= -0.3].sort_values(by='score', ascending=True)
    
    cols = st.columns(2)
    
    with cols[0]:
        st.success("**🟢 Major Bullish Drivers**")
        if not bullish.empty:
            for _, row in bullish.iterrows():
                st.markdown(f"- **{row['metal']} (+{row['score']}):** {row['catalyst']}")
        else:
            st.write("No major bullish catalysts detected in the recent cycle.")
            
    with cols[1]:
        st.error("**🔴 Major Bearish Pressures**")
        if not bearish.empty:
            for _, row in bearish.iterrows():
                st.markdown(f"- **{row['metal']} ({row['score']}):** {row['catalyst']}")
        else:
            st.write("No major bearish pressures detected in the recent cycle.")

def render_theme_heatmap(df):
    """Renders a Treemap showing which themes are dominating the news."""
    st.markdown("### 🗺️ Macroeconomic Theme Heatmap")
    st.markdown("Size represents news volume. Color represents average sentiment.")
    
    # Safety check: If the Google Sheet hasn't updated yet, don't crash the app
    if 'theme' not in df.columns:
        st.info("⏳ Theme data is currently populating from the AI pipeline. Check back in a few minutes.")
        return
        
    # Aggregate data for the Treemap
    theme_df = df.groupby(['theme', 'metal']).agg(
        Volume=('score', 'count'),
        Avg_Sentiment=('score', 'mean')
    ).reset_index()

    
    fig = px.treemap(
        theme_df, 
        path=[px.Constant("Global Market Drivers"), 'theme', 'metal'],
        values='Volume',
        color='Avg_Sentiment',
        # UPDATED: High-contrast financial terminal color scale
        color_continuous_scale=['#FF3333', '#0E1117', '#00FF44'], 
        color_continuous_midpoint=0
    )
    
    fig.update_layout(
        margin=dict(t=20, l=0, r=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
