import streamlit as st
import yfinance as yf
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# 1. Page Config must be the first Streamlit command
st.set_page_config(page_title="Class Market Sim", layout="wide")

# Load config
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# 2. LOGIN: Call this ONCE at the top of the sidebar
authenticator.login(location='sidebar', key='unique_login_key')

# 3. Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Market Watch", "My Portfolio"])

st.title("📈 EconEp Paper Trading")

# 4. Logic for "Market Watch"
if page == "Market Watch":
    st.header("Live Market News")
    ticker_symbol = st.text_input("Enter Ticker (e.g., AAPL)", "AAPL")
    if ticker_symbol:
        stock = yf.Ticker(ticker_symbol)
        data = stock.history(period="1d")
        st.metric(label=ticker_symbol, value=f"${data['Close'].iloc[-1]:.2f}")

# 5. Portfolio Page
elif page == "My Portfolio":
    st.header("Your Investments")
    
    # Check session state (the .login() call above already populated this)
    if st.session_state.get('authentication_status'):
        st.write(f"Welcome back, {st.session_state.get('name')}!")
        st.success("You are logged in.")
        if st.button('Logout'):
            authenticator.logout(location='sidebar')
    elif st.session_state.get('authentication_status') is False:
        st.error('Username/password is incorrect')
    elif st.session_state.get('authentication_status') is None:
        st.warning('Please log in using the sidebar')
