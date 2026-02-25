import streamlit as st
import os
import yfinance as yf
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_classic.agents import create_tool_calling_agent
from langchain_classic.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
import dotenv

dotenv.load_dotenv()


st.set_page_config(page_title="Financial Agent", page_icon="📈")
st.title("AI Financial Assistant")

api_key = dotenv.get_key(dotenv.find_dotenv(), "GEMINI_API_KEY")


@tool
def get_stock_price(ticker: str) -> str:
    """Fetches the current live stock price for a given ticker symbol (e.g., AAPL, POLYCAB.NS, ADANIENT.NS)."""
    try:
        stock = yf.Ticker(ticker)
        price = stock.fast_info.last_price 
        if ".NS" in ticker or ".BO" in ticker:
            return f"The current price of {ticker} is ₹{price:.2f}"
        else:
            return f"The current price of {ticker} is ${price:.2f}"
    except Exception as e:
        return f"Could not fetch price for {ticker}. Please ensure the ticker is correct."


tools = [get_stock_price]

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    
    
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a highly capable financial assistant. Use your tools to fetch live data if the user asks for stock prices. Do not guess prices."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        st.chat_message(role).write(msg.content)

    user_query = st.chat_input("E.g., What is the price of ADANIENT.NS? If I buy 50 shares, how much will it cost?")
    
    if user_query:
        st.chat_message("user").write(user_query)
        st.session_state.messages.append(HumanMessage(content=user_query))
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing markets..."):
                
                response = agent_executor.invoke({
                    "input": user_query,
                    "chat_history": st.session_state.messages
                })
                
                st.write(response["output"])
                st.session_state.messages.append(AIMessage(content=response["output"]))
else:
    st.info("Please enter your API key in the sidebar to start.")
