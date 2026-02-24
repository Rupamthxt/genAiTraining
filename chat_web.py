import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
import dotenv

dotenv.load_dotenv()

st.title("My First AI App")

# We assume the API key is already in the environment from the previous step,
# but for a standalone app, you'd want the user to input it securely:
api_key = dotenv.get_key(dotenv.find_dotenv(), "GEMINI_API_KEY")

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

    # Basic Chat UI
    user_input = st.chat_input("Ask me anything...")
    
    if user_input:
        st.chat_message("user").write(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = llm.invoke(user_input)
                st.write(response.content)
else:
    st.sidebar.warning("Please enter your API key to start.")