import plotly.graph_objects as go
import plotly.express as px
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

def render_time_series(df, time_col):
    """Renders a continuous time-series line chart with forward-filled data."""
    # 1. Pivot and aggregate to average out duplicate timestamps
    chart_df = df.pivot_table(
        index=time_col, 
        columns='metal', 
        values='score', 
        aggfunc='mean'
    )
    
    # 2. Forward-fill empty spaces so lines connect seamlessly, then reset index
    chart_df = chart_df.ffill().reset_index()

    # 3. Melt the dataframe back into a long format which Plotly Express prefers
    melted_df = chart_df.melt(
        id_vars=time_col, 
        value_vars=chart_df.columns[1:], 
        var_name='Metal', 
        value_name='Sentiment'
    )

    # 4. Build the premium Plotly Express chart
    fig = px.line(
        melted_df, 
        x=time_col, 
        y='Sentiment', 
        color='Metal',
        markers=True,
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#F8FAFC"),
        xaxis=dict(showgrid=True, gridcolor='#334155', title=""),
        yaxis=dict(showgrid=True, gridcolor='#334155', title="Sentiment Score", range=[-1.1, 1.1]),
        hovermode="x unified", # SaaS UI trick: shows all metal scores on a single vertical hover line
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=20, b=0),
        height=450
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
