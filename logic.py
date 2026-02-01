import yfinance as yf
from textblob import TextBlob
import pandas as pd
import random
from datetime import datetime, timedelta

# 1. Fetch Stock Data
def get_stock_data(ticker, period="7d"):
    """Fetches historical stock data from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        return df
    except Exception as e:
        return None

# 2. Fetch News (Simulated for Reliability)
def get_news_sentiment(ticker):
    """
    In a real app, we would scrape Google News. 
    For a Hackathon, scraping often gets blocked. 
    We will simulate realistic headlines based on the stock's movement to ensure a perfect demo.
    """
    
    # Mock headlines for demo purposes
    positive_headlines = [
        f"{ticker} announces breakthrough technology",
        f"Analysts upgrade {ticker} to Buy",
        f"Record breaking profits for {ticker}",
        f"{ticker} CEO announces new partnership"
    ]
    
    negative_headlines = [
        f"{ticker} faces regulatory scrutiny",
        f"Supply chain issues hit {ticker}",
        f"{ticker} misses earnings expectations",
        f"Investors worried about {ticker} future"
    ]
    
    neutral_headlines = [
        f"{ticker} holds annual meeting",
        f"Market recap: {ticker} stays steady",
        f"What to expect from {ticker} this week"
    ]

    # Randomly generate 5 headlines for the dashboard list
    all_headlines = positive_headlines + negative_headlines + neutral_headlines
    recent_news = random.sample(all_headlines, 5)
    
    return recent_news

# 3. Generate Mock Sentiment Data (The "Demo Mode")
def generate_demo_sentiment(days=7):
    """
    Generates a mock sentiment score list to match the graph duration.
    Values range from -1 (Negative) to 1 (Positive).
    """
    dates = [datetime.today() - timedelta(days=x) for x in range(days)]
    dates.reverse()
    
    # Create smooth-ish random data
    sentiment_scores = [random.uniform(-0.5, 0.8) for _ in range(days)]
    
    df = pd.DataFrame({
        'Date': dates,
        'Sentiment': sentiment_scores
    })
    df.set_index('Date', inplace=True)
    return df