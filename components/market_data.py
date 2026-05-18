import yfinance as yf
import streamlit as st
import pandas as pd

# Expanded Mapping to include your newly discovered metals
TICKER_MAP = {
    'Copper': 'HG=F',       
    'Gold': 'GC=F',         
    'Silver': 'SI=F',       
    'Platinum': 'PL=F',     
    'Palladium': 'PA=F',    
    'Aluminum': 'ALI=F',    
    'Lithium': 'LIT',       
    'Zinc': 'ZNC=F',        
    'Iron Ore': 'IRON',     
    'Nickel': 'JJN',
    'Crude Oil': 'CL=F',    # New
    'Coal': 'BTU',          # New (Peabody Energy Proxy)
    'Cobalt': 'CCJ',        # New (Broad battery materials proxy)
    'Tin': 'JJT',           # New (Tin ETN)
    'Tungsten': 'SMTS'      # New
}

@st.cache_data(ttl=300) 
def fetch_live_prices(active_metals):
    """Fetches live prices and 24h percentage change for selected metals."""
    live_data = {}
    
    for metal in active_metals:
        if metal in TICKER_MAP:
            try:
                ticker = yf.Ticker(TICKER_MAP[metal])
                
                # FIX: Fetch 5 days of history to survive weekends and market holidays
                hist = ticker.history(period="5d")
                
                if len(hist) >= 2:
                    # Always grab the very last row, and the row immediately before it
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2]
                    pct_change = ((current_price - prev_price) / prev_price) * 100
                    
                    live_data[metal] = {
                        'price': current_price,
                        'change': pct_change
                    }
            except Exception:
                # If Yahoo Finance is down for a specific ticker, skip gracefully
                pass
                
    return live_data

def render_live_ticker(active_metals):
    """Renders a beautiful row of live pricing metrics."""
    prices = fetch_live_prices(active_metals)
    
    if prices:
        st.markdown("### 🔴 Live Global Spot Prices")
        
        # Dynamically create exactly as many columns as there are valid prices
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
