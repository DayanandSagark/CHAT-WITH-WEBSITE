
import streamlit as st
import bs4
from bs4 import BeautifulSoup
# Added langchain_core - chat messages
from langchain_core.messages import AIMessage,HumanMessage
# Added lang chain community document loaders - webbased loader
from langchain_community.document_loaders import WebBaseLoader
# Add recursive char text splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter



def get_response(usr_input):
    return "I don't know"

def get_vectorstore_from_url(url):
    #get the text in document form 
    loader = WebBaseLoader(url)
    document = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(document)
    return document_chunks

# APP CONFIG
st.set_page_config(page_title="Chat with websites", page_icon = "hello")
st.title("Chat with websites")
# session_state is the variable will persist the chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hi Iam Dayabot. How can I help you?"),
        ]

# SIDE BAR
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL pls..")

# validating the input website url not none
if website_url is None or website_url == "":
    st.info("Please enter website url")

else:
    #pass the web url for the document form
    document_chunks = get_vectorstore_from_url(website_url)
    with st.sidebar:
        st.write(document_chunks)
    # Create input prompts for your website
    # User input
    usr_qry = st.chat_input("Enter your message here ...")
    if usr_qry is not None and usr_qry != "":
        response = get_response(usr_qry)
        st.session_state.chat_history.append(HumanMessage(content=usr_qry))
        st.session_state.chat_history.append(AIMessage(content=response))
        
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




    





