import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def render_sentiment_matrix(df):
    """Renders an executive Quadrant Matrix comparing Sentiment vs. News Volume."""
    
    # 1. Aggregate Data: Calculate Average Sentiment AND Total Article Count (Volume)
    matrix_df = df.groupby('metal').agg(
        Avg_Sentiment=('score', 'mean'),
        News_Volume=('score', 'count')
    ).reset_index()

    # 2. Build the Scatter Plot
    fig = px.scatter(
        matrix_df,
        x='Avg_Sentiment',
        y='News_Volume',
        text='metal',
        size='News_Volume', 
        color='Avg_Sentiment',
        color_continuous_scale=['#EF4444', '#475569', '#10B981'], 
        range_color=[-1, 1]
    )

    # 3. Premium Styling & Typography
    fig.update_traces(
        textposition='top center',
        marker=dict(line=dict(width=1, color='#1E293B')),
        textfont=dict(color='#F8FAFC', size=12)
    )

    # 4. Draw Quadrant Crosshairs
    median_vol = matrix_df['News_Volume'].median()
    fig.add_vline(x=0, line_width=2, line_dash="dot", line_color="#475569")
    fig.add_hline(y=median_vol, line_width=2, line_dash="dot", line_color="#475569")

    # 5. Add Background Watermark Annotations
    max_vol = matrix_df['News_Volume'].max() + 1
    fig.add_annotation(x=0.5, y=max_vol, text="High Buzz / Bullish", showarrow=False, font=dict(color="#10B981", size=14), opacity=0.3)
    fig.add_annotation(x=-0.5, y=max_vol, text="High Buzz / Bearish", showarrow=False, font=dict(color="#EF4444", size=14), opacity=0.3)

    # 6. Final Layout adjustments
    fig.update_layout(
        title="Commodity Matrix: Market Buzz vs. Average Sentiment",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#F8FAFC"),
        xaxis=dict(showgrid=True, gridcolor='#334155', title="← Bearish | Average Sentiment | Bullish →", range=[-1.1, 1.1]),
        yaxis=dict(showgrid=True, gridcolor='#334155', title="News Volume (Article Count)"),
        margin=dict(l=0, r=0, t=40, b=0),
        height=500,
        coloraxis_showscale=False 
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_time_series(df, time_col):
    """Renders a continuous time-series line chart with forward-filled data."""
    # 1. Pivot and aggregate
    chart_df = df.pivot_table(
        index=time_col, 
        columns='metal', 
        values='score', 
        aggfunc='mean'
    )
    
    # 2. Forward-fill empty spaces
    chart_df = chart_df.ffill().reset_index()

    # 3. Melt the dataframe
    melted_df = chart_df.melt(
        id_vars=time_col, 
        value_vars=chart_df.columns[1:], 
        var_name='Metal', 
        value_name='Sentiment'
    )

    # 4. Build the Plotly Express chart
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
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=20, b=0),
        height=450
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_volatility_distribution(df):
    """Renders a box plot showing sentiment volatility, spread, and outliers."""
    
    st.markdown("<h4 style='color: #c9d1d9; font-weight: 400; margin-top: 2rem; margin-bottom: 0.5rem;'>Asset Volatility Distribution</h4>", unsafe_allow_html=True)
    st.markdown("<p style='color: #8b949e; font-size: 0.85rem;'>Analyzes the spread, median, and outliers of market sentiment. Wider distributions indicate higher market uncertainty.</p>", unsafe_allow_html=True)

    # Build the Box Plot with underlying data points visible
    fig = px.box(
        df,
        x='score',
        y='metal',
        color='metal',
        points="all", 
        hover_data=['catalyst'] 
    )

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#F8FAFC"),
        xaxis=dict(showgrid=True, gridcolor='#334155', title="Sentiment Score", range=[-1.1, 1.1]),
        yaxis=dict(showgrid=True, gridcolor='#334155', title=""),
        margin=dict(l=0, r=0, t=20, b=0),
        height=450,
        showlegend=False 
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
