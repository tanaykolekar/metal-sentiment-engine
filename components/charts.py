import plotly.graph_objects as go
import streamlit as st

def render_sentiment_ranking(df):
    # Calculate averages
    avg_sent = df.groupby('metal')['score'].mean().sort_values(ascending=True)
    
    # Assign premium colors based on sentiment
    colors = ['#EF4444' if x < 0 else '#10B981' for x in avg_sent.values] # Red / Emerald
    
    fig = go.Figure(go.Bar(
        x=avg_sent.values,
        y=avg_sent.index,
        orientation='h',
        marker_color=colors,
        text=[f"{val:.2f}" for val in avg_sent.values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Macro Sentiment Ranking",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#F8FAFC"),
        xaxis=dict(showgrid=True, gridcolor='#334155', zeroline=True, zerolinecolor='#94A3B8'),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=40, b=0),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
