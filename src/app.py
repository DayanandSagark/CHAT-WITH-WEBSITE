
import streamlit as st
# Added langchain_core
from langchain_core.messages import AIMessage,HumanMessage

def get_response(usr_input):
    return "I don't know"

# APP CONFIG
st.set_page_config(page_title="Chat with websites", page_icon = "hello")
st.title("Chat with websites")
chat_history = [
    AIMessage(content="Hi Iam Dayabot. How can I help you?"),
]

# SIDE BAR
with st.sidebar:
    st.header("Settings")
    website_url = st.text_input("Website URL pls..")


# Create input prompts for your website
# User input
usr_qry = st.chat_input("Enter your message here ...")
if usr_qry is not None and usr_qry != "":
    response = get_response(usr_qry)
    chat_history.append(HumanMessage(content=usr_qry))
    chat_history.append(AIMessage(content=response))

    #with st.chat_message("Human"):
     #   st.write(usr_qry)
    #with st.chat_message("AI"):
     #   st.write("I dont know..")

with st.sidebar:
    st .write(chat_history)





## Check for chat in the streamlit
#with st.chat_message("DAYABot"):
#   st.write("How can i help you?")

#with st.chat_message("Human"):
 #   st.write("I want to know about Langchain")




    





