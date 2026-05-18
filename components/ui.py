import streamlit as st

def render_premium_kpi(metal, score, catalyst):
    """Generates a custom HTML card for market movers."""
    # Determine colors and arrows
    if score > 0:
        color_class = "kpi-bullish"
        arrow = "▲ +"
    elif score < 0:
        color_class = "kpi-bearish"
        arrow = "▼ "
    else:
        color_class = "kpi-neutral"
        arrow = "▬ "

    # Build the HTML
    html = f"""
    <div class="premium-card">
        <div class="kpi-title">{metal}</div>
        <div class="kpi-value">{score:.2f}</div>
        <div class="{color_class}">{arrow}{score:.2f} Sentiment</div>
        <div class="kpi-desc">{catalyst}</div>
    </div>
    """
    # Render it into Streamlit
    st.markdown(html, unsafe_allow_html=True)
