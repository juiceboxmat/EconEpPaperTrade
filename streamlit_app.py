import streamlit as st
import yfinance as yf
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)


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

# 4. Portfolio with Login Gate
elif page == "My Portfolio":
    st.header("Your Investments")
    
    # This creates the login widget
    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status:
        st.write(f"Welcome, {name}!")
        st.write("You are now logged in and can view your portfolio.")
        # You'll add your portfolio tracking logic here later
        if st.button('Logout'):
            authenticator.logout('Logout', 'main')
            
    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')
