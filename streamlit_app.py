import streamlit as st
import yfinance as yf
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# 1. Page Configuration (Must be first)
st.set_page_config(page_title="Class Market Sim", layout="wide")

# 2. Load Config
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# 3. Initialize Authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# 4. Login Widget (Only called once, with a forced unique key)
# The key 'unique_auth_form' prevents the duplicate form exception.
authenticator.login(location='sidebar', key='unique_auth_form')

# 5. Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Market Watch", "My Portfolio"])

# 6. Main App Content
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
    
    # Check status from session_state
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
