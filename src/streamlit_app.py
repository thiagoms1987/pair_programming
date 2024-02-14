import streamlit as st
from utils_tools import agent

st.title('Pair Programming App')

user_message = st.text_input('Enter your message here:')

if st.button('Submit'):
    response_message = agent(user_message).get("message")
    
    st.write(response_message)
