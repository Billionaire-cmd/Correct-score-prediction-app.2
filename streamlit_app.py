import streamlit as st
import requests

# Backend API URL
api_url = "http://localhost:5000/place_trade"  # Update with your hosted backend URL

st.title("🤖🤖🤖📉📈Rabiotic Trading Strategy Bot")

# Input fields
license_key = st.text_input("License Key")
symbol = st.selectbox("Market Symbol", [
    # Synthetic Indices
    "Volatility 10 Index", "Volatility 25 Index", "Volatility 50 Index",
    "Volatility 75 Index", "Volatility 100 Index", "Crash 1000 Index",
    "Crash 500 Index", "Boom 1000 Index", "Boom 500 Index", "Step Index",
    "Range Break 100 Index", "Range Break 200 Index",
    # Forex Pairs
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD", "USDCAD", "NZDUSD",
    "EURGBP", "EURJPY",
    # Crypto Pairs
    "BTCUSD", "ETHUSD", "LTCUSD", "XRPUSD", "BCHUSD", "ADAUSD", "DOTUSD",
    "BNBUSD", "SOLUSD", "DOGEUSD", "MATICUSD", "AVAXUSD"
])
timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "4h", "1d"])
take_profit = st.number_input("Take Profit", min_value=0.0)
stop_loss = st.number_input("Stop Loss", min_value=0.0)

# Button to execute the strategy
if st.button("Run Strategy"):
    payload = {
        "license_key": license_key,
        "symbol": symbol,
        "timeframe": timeframe,
        "take_profit": take_profit,
        "stop_loss": stop_loss
    }

    try:
        # Sending request to the backend
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(result["message"])
            st.write(f"Action: {result['action']}")
            st.write(f"Symbol: {result['symbol']}")
            st.write(f"Timeframe: {result['timeframe']}")
            st.write(f"Take Profit: {result['take_profit']}")
            st.write(f"Stop Loss: {result['stop_loss']}")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to connect to server: {e}")
