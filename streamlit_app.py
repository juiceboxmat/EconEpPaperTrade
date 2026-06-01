import streamlit as st
import yfinance as yf
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# 1. Setup
st.set_page_config(page_title="Class Market Sim", layout="wide")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# 2. LOGIN WIDGET: Only call this once!
# Using a unique key prevents the "multiple identical forms" error.
authenticator.login(location='sidebar', key='unique_login_form')

# 3. Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Market Watch", "My Portfolio"])

# 4. Content
st.title("📈 EconEp Paper Trading")

if page == "Market Watch":
    st.header("Live Market News")
    ticker = st.text_input("Enter Ticker", "AAPL")
    if ticker:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        st.metric(label=ticker, value=f"${data['Close'].iloc[-1]:.2f}")

elif page == "My Portfolio":
    st.header("Your Investments")
    
    # Check the status after the single login call above
    if st.session_state.get('authentication_status'):
        st.write(f"Welcome back, {st.session_state.get('name')}!")
        st.success("You are successfully logged in.")
        if st.button('Logout'):
            authenticator.logout(location='sidebar')
            st.rerun()
    elif st.session_state.get('authentication_status') is False:
        st.error('Username/password is incorrect')
    elif st.session_state.get('authentication_status') is None:
        st.warning('Please log in using the sidebar')
