import yfinance as yf
import streamlit as st
import pandas as pd

# Mapping your metals to Yahoo Finance Tickers (Futures & ETFs)
TICKER_MAP = {
    'Copper': 'HG=F',       # Copper Futures
    'Gold': 'GC=F',         # Gold Futures
    'Silver': 'SI=F',       # Silver Futures
    'Platinum': 'PL=F',     # Platinum Futures
    'Palladium': 'PA=F',    # Palladium Futures
    'Aluminum': 'ALI=F',    # Aluminum Futures
    'Lithium': 'LIT',       # Global X Lithium & Battery Tech ETF (Best proxy)
    'Zinc': 'ZNC=F',        # Zinc Futures
    'Iron Ore': 'IRON',     # Iron Ore Proxy
    'Nickel': 'JJN'         # Nickel ETN Proxy
}

@st.cache_data(ttl=300) # Cache for 5 minutes so Yahoo doesn't block you
def fetch_live_prices(active_metals):
    """Fetches live prices and 24h percentage change for selected metals."""
    live_data = {}
    
    for metal in active_metals:
        if metal in TICKER_MAP:
            try:
                ticker = yf.Ticker(TICKER_MAP[metal])
                # Fetch the last 2 days to calculate the daily change
                hist = ticker.history(period="2d")
                
                if len(hist) >= 2:
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2]
                    pct_change = ((current_price - prev_price) / prev_price) * 100
                    
                    live_data[metal] = {
                        'price': current_price,
                        'change': pct_change
                    }
            except Exception:
                # If a ticker fails to load, just skip it gracefully
                pass
                
    return live_data

def render_live_ticker(active_metals):
    """Renders a beautiful row of live pricing metrics."""
    prices = fetch_live_prices(active_metals)
    
    if prices:
        st.markdown("### 🔴 Live Global Spot Prices")
        cols = st.columns(len(prices))
        
        for i, (metal, data) in enumerate(prices.items()):
            with cols[i]:
                st.metric(
                    label=f"{metal} Price",
                    value=f"${data['price']:,.2f}",
                    delta=f"{data['change']:.2f}%",
                    delta_color="normal"
                )
        st.markdown("<br>", unsafe_allow_html=True)
