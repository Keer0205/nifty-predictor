# app.py - NIFTY 50 PREDICTOR (FORCED IST TIME)
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import talib
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime
import pytz

st.set_page_config(page_title="Nifty Predictor", layout="wide")
st.title("NIFTY 50 BULL/BEAR PREDICTOR")
st.markdown("**Technical + News Sentiment | Live from NSE**")

# FORCE IST (INDIA TIME) — WORKS ANYWHERE IN THE WORLD
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist).strftime("%d %B %Y, %I:%M %p")
st.markdown(f"**Last Updated: {current_time} IST**")

@st.cache_data(ttl=1800)
def get_data():
    df = yf.download('^NSEI', period='1y', progress=False)
    df = df.dropna()
    close = df['Close'].astype('float64').values.flatten()
    ema20 = talib.EMA(close, 20)
    ema50 = talib.EMA(close, 50)
    rsi = talib.RSI(close, 14)
    macd, signal, _ = talib.MACD(close)
    df = df.iloc[-len(ema20):].copy()
    df['EMA20'] = ema20
    df['EMA50'] = ema50
    df['RSI'] = rsi
    df['MACD'] = macd
    df['MACD_Signal'] = signal
    return df

@st.cache_data(ttl=900)
def get_sentiment():
    try:
        url = "https://economictimes.indiatimes.com/markets/indices/nifty-50"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        headlines = [h.get_text().strip() for h in soup.find_all('h3')[:8] if h.get_text().strip()]
        analyzer = SentimentIntensityAnalyzer()
        scores = [analyzer.polarity_scores(h)['compound'] for h in headlines]
        avg = np.mean(scores) if scores else 0
        return "Bullish" if avg > 0.1 else "Bearish" if avg < -0.1 else "Neutral"
    except:
        return "Neutral"

df = get_data()
latest = df.iloc[-1]
sentiment = get_sentiment()

price = float(latest['Close'])
ema20 = float(latest['EMA20'])
ema50 = float(latest['EMA50'])
rsi = float(latest['RSI'])
macd = float(latest['MACD'])
signal = float(latest['MACD_Signal'])

tech_score = sum([price > ema20, ema20 > ema50, rsi > 50, macd > signal])
tech = "Bullish" if tech_score >= 3 else "Bearish" if tech_score <= 1 else "Neutral"
final = "BULLISH" if tech == "Bullish" and sentiment != "Bearish" else \
        "BEARISH" if tech == "Bearish" and sentiment != "Bullish" else "NEUTRAL"

col1, col2 = st.columns(2)
with col1:
    st.metric("Nifty Price", f"₹{price:,.2f}")
    st.metric("RSI", f"{rsi:.1f}")
with col2:
    st.metric("Technical", tech)
    st.metric("Sentiment", sentiment)

st.markdown(f"## **FINAL PREDICTION: {final}**")

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df.index[-60:], df['Close'][-60:], label='Nifty 50', color='blue', linewidth=2)
ax.plot(df.index[-60:], df['EMA20'][-60:], label='EMA20', color='orange', alpha=0.8)
ax.plot(df.index[-60:], df['EMA50'][-60:], label='EMA50', color='red', alpha=0.8)
ax.set_title("Nifty 50 Trend (Last 60 Days)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.caption("Data: Yahoo Finance | News: Economic Times | Updates every 30 mins")