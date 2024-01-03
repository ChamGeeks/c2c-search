import os
from dotenv import load_dotenv

from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceHub
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
import streamlit as st


def get_vector_store() -> FAISS:
    embeddings = OpenAIEmbeddings()
    print("LOADING DB")
    vs = FAISS.load_local("./data/db", embeddings)
    print("DB LOADED")
    return vs


def get_conversation_chain(vector_store:FAISS, system_message:str, human_message:str) -> ConversationalRetrievalChain:
    """
    Get the chatbot conversation chain

    Args:
        vector_store (FAISS): Vector store
        system_message (str): System message
        human_message (str): Human message

    Returns:
        ConversationalRetrievalChain: Chatbot conversation chain
    """
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(model="HuggingFaceH4/zephyr-7b-beta") # if you want to use open source LLMs
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={
            "prompt": ChatPromptTemplate.from_messages(
                [
                    system_message,
                    human_message,
                ]
            ),
        },
    )
    return conversation_chain

def handle_style_and_responses(user_question: str) -> None:
    """
    Handle user input to create the chatbot conversation in Streamlit

    Args:
        user_question (str): User question
    """
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    human_style = "background-color: #e6f7ff; border-radius: 10px; padding: 10px;"
    chatbot_style = "background-color: #f9f9f9; border-radius: 10px; padding: 10px;"

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.markdown(
                f"<p style='text-align: right;'><b>User</b></p> <p style='text-align: right;{human_style}'> <i>{message.content}</i> </p>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<p style='text-align: left;'><b>Chatbot</b></p> <p style='text-align: left;{chatbot_style}'> <i>{message.content}</i> </p>",
                unsafe_allow_html=True,
            )


def streamlit():
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        """
        You are a chatbot tasked with responding to questions about ski touring itineraries.
        
        The user will provide text describing a desired outing. Your job is to infer the following details about the outing:
        - the outing area, as a geographical location 
        - the minimum and maximum levels of difficulty desired, using the following levels: F (easy), PD (not difficult), AD (quite difficult), D (difficult), TD (very difficult), and ED (extremely difficult).
        - the minimum and maximum amount of ascent desired, in meters
        You will try to infer these details from the text provided by the user. As long as any detail is missing, you will ask the 
        user for the missing information. 
        
        Once all details have been inferred, you will respond with the most relevant route page for the context below:\n
        {context}
        """
    )
    human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")
    
    st.session_state.vector_store = get_vector_store()
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.set_page_config(
        page_title="Skitour Chatbot",
        page_icon=":books:",
    )

    st.title("Skitour Chatbot")
    st.subheader("Chat with c2c!")
    st.markdown(
        """
        This chatbot was created to help mountaineers find tomorrow's adventure quickly and go to bed early.
        """
    )
    st.image("https://photos.google.com/share/AF1QipPUj_oofXV6yuG62an4AsMmNeSUrQCFKqcGTsmoTMRNhZhf8McB9ASdPdRXnE8VnA/photo/AF1QipNnhlFW1rk-mGMYxL5COV-nQUwodlJiiO8RShtf?key=V3UxcmxPVGlIRFdZTFBseWI0SEtIM1RKdFFkb3hR") # Image rights to Alex Knight on Unsplash

    user_question = st.text_input("Describe the adventure you are looking for")
    with st.spinner("Processing..."):
        if user_question:
            handle_style_and_responses(user_question)

    st.session_state.conversation = get_conversation_chain(
        st.session_state.vector_store, system_message_prompt, human_message_prompt
    )


def cli():
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        """
        You are a chatbot tasked with responding to questions about ski touring routes listed on camptocamp.org.
        
        You should never answer a question with a question, and you should always respond with the most relevant camptocamp.org page.

        Do not answer questions that are not about ski touring.

        Given a question, you should respond with the most relevant content page by following the relevant context below:\n
        {context}
        """
    )
    human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")
    
    vector_store = get_vector_store()

    chain = get_conversation_chain(
        vector_store, system_message_prompt, human_message_prompt
    )
    
    user_input = input("Describe the mountain adventure are you looking for\n>>> ")
    while True:
        response = chain.invoke(user_input)
        user_input = input(response["answer"] + "\n>>> ")



if __name__ == "__main__":
    load_dotenv()
    cli()
    
