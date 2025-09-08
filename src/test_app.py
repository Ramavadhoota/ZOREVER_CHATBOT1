import streamlit as st

st.title("Zorever Real Estate Chatbot - Test")
st.write("This is a test to see if the basic interface loads.")

st.write("If you can see this, Streamlit is working!")

# Simple chat input test
if prompt := st.chat_input("Type a test message here..."):
    st.write(f"You typed: {prompt}")

st.sidebar.header("Test Sidebar")
st.sidebar.write("This should appear in the sidebar.")
