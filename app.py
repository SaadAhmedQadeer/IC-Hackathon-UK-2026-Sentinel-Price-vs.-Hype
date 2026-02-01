import streamlit as st
import plotly.graph_objects as go
from logic import get_stock_data, get_news_sentiment, generate_demo_sentiment
import pandas as pd
from textblob import TextBlob

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Sentinel", page_icon="📈", layout="wide")
##

##
# --- CSS FOR STYLING (Make it look pro) ---
# --- CSS FOR STYLING (Updated to fix Button) ---
st.markdown("""
<style>
    /* 1. Main App Background */
    .stApp {
        background-color: #000000;
        color: white;
    }
    
    /* 2. Fix the "Run Analysis" Button */
    div.stButton > button {
        background-color: #ff4b4b; /* Streamlit Red */
        color: white;              /* White Text */
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }

    /* 3. Button Hover Effect */
    div.stButton > button:hover {
        background-color: #ff3333; /* Slightly brighter red on hover */
        color: white;
        border: none;
    }
    
    /* 4. Metric Cards (Optional polish) */
    div[data-testid="stMetricValue"] {
        color: #ff4b4b; /* Make numbers pop with color */
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("⚙️ Control Panel")
ticker = st.sidebar.text_input("Stock Ticker", "NVDA").upper()
days_range = st.sidebar.slider("Time Range (Days)", 5, 30, 14)
demo_mode = st.sidebar.checkbox("✅ Enable Demo Mode", value=True)

st.sidebar.markdown("---")
st.sidebar.info("Tip: Uncheck 'Demo Mode' to attempt live data fetching (slower).")

# --- MAIN PAGE ---
st.title(f"📈 Sentinel: {ticker} Analysis")
st.markdown("### Real-time Market vs. Sentiment Correlation")

# --- APP LOGIC ---
if st.button("Run Analysis") or True: # 'or True' makes it run on load
    
    # 1. Get Data
    with st.spinner('Fetching market data...'):
        stock_df = get_stock_data(ticker, period=f"{days_range}d")
    
    if stock_df is None or stock_df.empty:
        st.error("Error fetching stock data. Check the ticker.")
    else:
        # 2. Get Sentiment (Mocked for Hackathon Stability)
        sentiment_df = generate_demo_sentiment(days=len(stock_df))
        news_headlines = get_news_sentiment(ticker)
        
        # 3. Top Metrics Row
        current_price = stock_df['Close'].iloc[-1]
        price_change = current_price - stock_df['Close'].iloc[0]
        avg_sentiment = sentiment_df['Sentiment'].mean()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${current_price:.2f}", f"{price_change:.2f}")
        col2.metric("Market Sentiment Score", f"{avg_sentiment:.2f}", "Neutral" if -0.2 < avg_sentiment < 0.2 else ("Bullish" if avg_sentiment > 0 else "Bearish"))
        col3.metric("News Volume", "High", "Trending")

        # 4. The "Money Shot" Graph
        # We use Plotly to overlay two different Y-axes (Price vs Sentiment)
        fig = go.Figure()

        # Trace 1: Stock Price (Blue Line)
        fig.add_trace(go.Scatter(
            x=stock_df.index, 
            y=stock_df['Close'], 
            name="Stock Price ($)",
            line=dict(color='#00CC96', width=3)
        ))

        # Trace 2: Sentiment (Red/Orange Line) - Uses a secondary Y-axis
        fig.add_trace(go.Scatter(
            x=stock_df.index, 
            y=sentiment_df['Sentiment'], 
            name="News Sentiment",
            line=dict(color='#EF553B', width=2, dash='dot'),
            yaxis="y2"
        ))

        # Layout to handle double axis
        fig.update_layout(
            title="Price Action vs. Media Hype",
            height=500,
            yaxis=dict(title="Stock Price", side="left"),
            yaxis2=dict(title="Sentiment Score (-1 to 1)", side="right", overlaying="y", range=[-1, 1]),
            template="plotly_dark",
            legend=dict(x=0, y=1.1, orientation="h")
        )

        st.plotly_chart(fig, use_container_width=True)

        # 5. News Feed Section
        st.markdown("### 📰 Latest Detected Headlines")
        for news in news_headlines:
            sentiment_val = TextBlob(news).sentiment.polarity
            color = "green" if sentiment_val > 0 else "red" if sentiment_val < 0 else "gray"

            st.markdown(f"**:{color}[{'POSITIVE' if sentiment_val > 0 else 'NEGATIVE'}]** - {news}")
