import streamlit as st
import yfinance as yf

# 1. Page Title
st.set_page_config(page_title="Class Market Sim", layout="wide")
st.title("📈 EconEp Paper Trading")

# 2. Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Market Watch", "My Portfolio"])

# 3. Simple Mock Logic for "Market Watch"
if page == "Market Watch":
    st.header("Live Market News")
    st.write("Welcome to the class simulation! Check back here for updates.")
    
    # Quick example of pulling data using yfinance
    ticker_symbol = st.text_input("Enter Ticker (e.g., AAPL, TSLA)", "AAPL")
    if ticker_symbol:
        stock = yf.Ticker(ticker_symbol)
        data = stock.history(period="1d")
        st.write(f"Current price for {ticker_symbol}:")
        st.metric(label=ticker_symbol, value=f"${data['Close'].iloc[-1]:.2f}")

# 4. Placeholder for Portfolio
elif page == "My Portfolio":
    st.header("Your Investments")
    st.write("Log in to see your trade history.")
    # We will build the login logic here in the next step!
