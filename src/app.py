
import streamlit as st
import bs4
from bs4 import BeautifulSoup
# Added langchain_core - chat messages
from langchain_core.messages import AIMessage,HumanMessage
# Added lang chain community document loaders - webbased loader
from langchain_community.document_loaders import WebBaseLoader
# Add recursive char text splitter - document chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter
# importing lang chain vector database - chroma
from langchain_community.vectorstores import Chroma

# importing embaddings open ai 
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from dotenv import load_dotenv
# prompt template
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
# complete retriever chain
from langchain.chains import create_history_aware_retriever,create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()
OPEN_API_KEY = st.secrets["OPENAI_API_KEY"]

def get_vectorstore_from_url(url):
    #get the text in document form 
    loader = WebBaseLoader(url)
    document = loader.load()

    # Split document into chunks
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(document)

    vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings())
    return vector_store

def get_context_retrieval_chain(vector_store):
    llm = ChatOpenAI()
    retriever = vector_store.as_retriever()

    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}"),
        ("user","Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
        ])

    retriever_chain = create_history_aware_retriever(llm,retriever,prompt)
    return retriever_chain


def get_coverstaional_rag_chain(retriver_chain):
    llm =ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        ("system","Answer the user questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}"),

    ])
    stuff_documents_chain = create_stuff_documents_chain(llm,prompt)
    return create_retrieval_chain(retriver_chain,stuff_documents_chain)

def get_response(usr_input):
    #return "I don't know"
    retriever_chain = get_context_retrieval_chain(st.session_state.vector_store)
    conversation_rag_chain = get_coverstaional_rag_chain(retriever_chain)

    response = conversation_rag_chain.invoke({
        "chat_history" : st.session_state.chat_history,
        "input" : usr_qry
    })
    
    return response['answer']

# APP CONFIG
st.set_page_config(page_title="Chat with websites", page_icon = "hello")
st.title("Chat with websites")
# session_state is the variable will persist the chat history


# SIDE BAR
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL pls..")

# validating the input website url not none
if website_url is None or website_url == "":
    st.info("Please enter website url")

else:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hi Iam Dayabot. How can I help you?"),
            ]
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = get_vectorstore_from_url(website_url)
    #pass the web url for the document form
    #vector_store = get_vectorstore_from_url(website_url)
    # create conversational chain
        #1. first the reriver chain is created and then 2. that is passed to conversational chain
    #retriever_chain = get_context_retrieval_chain(st.session_state.vector_store)
    #conversation_rag_chain = get_coverstaional_rag_chain(retriever_chain)
    #with st.sidebar:
     #   st.write(document_chunks)
    # Create input prompts for your website
    # User input
    usr_qry = st.chat_input("Enter your message here ...")
    if usr_qry is not None and usr_qry != "":
        response = get_response(usr_qry)
        #response = conversation_rag_chain.invoke({
        #    "chat_history" : st.session_state.chat_history,
        #    "input" : usr_qry,

        #})
        #st.write(response)
        st.session_state.chat_history.append(HumanMessage(content=usr_qry))
        st.session_state.chat_history.append(AIMessage(content=response))
        # tested for retrieval documents
        #retrieved_documents = retriever_chain.invoke({
        #    "chat_history" : st.session_state.chat_history,
         #    "input" : usr_qry
        #})
        #st.write(retrieved_documents)
        
    #Conversation
    for message in st.session_state.chat_history:
        if isinstance(message,AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        if isinstance(message,HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)  

    #with st.sidebar:
    #    st.write(st.session_state.chat_history)





## Check for chat in the streamlit
#with st.chat_message("DAYABot"):
#   st.write("How can i help you?")

#with st.chat_message("Human"):
 #   st.write("I want to know about Langchain")




    





