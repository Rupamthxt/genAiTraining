import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import dotenv

dotenv.load_dotenv()

# 1. Minimal UI Configuration
st.set_page_config(page_title="Chat", page_icon="💬")
st.title("Conversational AI")

# Sidebar for API Key (Keeps the main interface clean)
api_key = dotenv.get_key(dotenv.find_dotenv(), "GEMINI_API_KEY")

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    
    # Initialize the LLM
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # 2. Session State Management (The "Memory")
    # If this is the first time the app is loading, create an empty list for messages
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # 3. Render the existing conversation
    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            st.chat_message("user").write(message.content)
        elif isinstance(message, AIMessage):
            st.chat_message("assistant").write(message.content)

    # 4. Handle New User Input
    user_query = st.chat_input("Type your message here...")
    
    if user_query:
        # Display the user's message immediately
        st.chat_message("user").write(user_query)
        
        # Append user message to the historical memory
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        
        # Show a loading spinner while the LLM thinks
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Feed the ENTIRE chat history to the LLM
                response = llm.invoke(st.session_state.chat_history)
                
                # Display the AI's response
                st.write(response.content)
                
                # Append the AI's response to the historical memory
                st.session_state.chat_history.append(AIMessage(content=response.content))
else:
    st.info("Please enter your API key in the sidebar to begin.")