# Nifty 50 Bull/Bear Predictor

Live AI-powered trend predictor for Nifty 50 (NSE) using technical analysis (EMA, RSI, MACD) + news sentiment (Economic Times).

## Live Demo
[![Nifty Predictor](https://img.shields.io/badge/Live-Dashboard-blue)](https://keer0205-nifty-predictor.streamlit.app)

## Features
- **Real-time NSE data** via yfinance
- **Technical:** EMA20/50, RSI, MACD
- **Sentiment:** NLP from Economic Times
- **Timezone:** IST (India Standard Time)
- **Prediction:** Bullish/Bearish/Neutral

## Screenshots
![Dashboard](screenshot.png)  <!-- Upload your screenshot here -->

## Tech Stack
- Python, Streamlit
- TA-Lib, yfinance
- VADER Sentiment, BeautifulSoup

## Setup
```bash
pip install -r requirements.txt
streamlit run app.py
