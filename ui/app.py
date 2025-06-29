import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

# Backend URL
BACKEND_URL = "http://localhost:8000/chat"

def main():
    st.title("FinSolve Technologies - Role-Based Chatbot")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar for login
    with st.sidebar:
        st.header("Authentication")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Login")
        
        if login_button:
            try:
                # Test authentication
                auth = HTTPBasicAuth(username, password)
                response = requests.post(
                    BACKEND_URL,
                    json={"message": "Test connection"},
                    auth=auth
                )
                if response.status_code == 200:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Logged in successfully!")
                else:
                    st.error("Invalid credentials")
            except Exception as e:
                st.error(f"Connection error: {str(e)}")
        # Clear chat button
        if st.session_state.get("authenticated"):
            st.divider()
            st.header("Chat Controls")
            if st.button("Clear Chat History", use_container_width=True):
                st.session_state.messages = []
                st.success("Chat history cleared!")

    # Chat interface
    if st.session_state.get("authenticated"):
        st.subheader(f"Welcome, {st.session_state.username}!")
        
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # User input
        if prompt := st.chat_input("Ask a question..."):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get response from backend
            auth = HTTPBasicAuth(st.session_state.username, password)
            response = requests.post(
                BACKEND_URL,
                json={"message": prompt},
                auth=auth
            )
            
            if response.status_code == 200:
                bot_response = response.json()["response"]
            else:
                bot_response = f"Error: {response.status_code} - {response.text}"
            
            # Add bot response to history
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            
            # Display bot response
            with st.chat_message("assistant"):
                st.markdown(bot_response)
    else:
        st.info("Please log in to access the chatbot")

if __name__ == "__main__":
    main()