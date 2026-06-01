import streamlit as st
import yfinance as yf
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

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

# This must be the very first thing in your sidebar logic
authenticator.login(location='sidebar')

# 1. Page Title
st.set_page_config(page_title="Class Market Sim", layout="wide")
st.title("📈 EconEp Paper Trading")

# --- LOGIN ALWAYS IN SIDEBAR ---
# By calling this here, it is outside the "page" logic, so it never disappears.
authenticator.login(location='sidebar')

# 2. Sidebar for navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", ["Market Watch", "My Portfolio"])

# 3. Simple Mock Logic for "Market Watch"
if page == "Market Watch":
    st.header("Live Market News")
    # ... (your existing code) ...

# 4. Portfolio Page
elif page == "My Portfolio":
    st.header("Your Investments")
    
    # Check status from the session state (now populated by the call above)
    if st.session_state.get('authentication_status'):
        st.write(f"Welcome back, {st.session_state.get('name')}!")
        st.success("You are logged in.")
        
        if st.button('Logout'):
            authenticator.logout(location='sidebar')
            
    elif st.session_state.get('authentication_status') is False:
        st.error('Username/password is incorrect')
    elif st.session_state.get('authentication_status') is None:
        st.warning('Please log in using the sidebar')
