import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
import dotenv

dotenv.load_dotenv()

st.title("📚 Chat with your Notes")

api_key = dotenv.get_key(dotenv.find_dotenv(), "GEMINI_API_KEY")

uploaded_file = st.file_uploader("Upload a .txt file", type="txt")

if api_key and uploaded_file:
    os.environ["GOOGLE_API_KEY"] = api_key
    
    # 1. Save uploaded file temporarily
    with open("temp.txt", "wb") as f:
        f.write(uploaded_file.getvalue())
        
    # 2. Load and Split Text
    loader = TextLoader("temp.txt")
    docs = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(docs)
    
    # 3. Create Embeddings and Vector Store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_documents(split_docs, embeddings)
    retriever = vector_store.as_retriever()
    
    # 4. Set up the LangChain
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    prompt = ChatPromptTemplate.from_template("""
    Answer the following question based only on the provided context:
    <context>
    {context}
    </context>
    Question: {input}
    """)
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    # 5. Chat Interface
    user_query = st.text_input("Ask a question about your document:")
    if user_query:
        response = retrieval_chain.invoke({"input": user_query})
        st.write("### Answer:")
        st.write(response["answer"])