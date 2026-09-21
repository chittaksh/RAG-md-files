## simple streamlit app

import streamlit as st
from rag_chain import generate_answer

st.title("Document Retrieval and Question Answering (RAG) Application")

## Create a message history using session_state
## Streamlit will rerun this python script every time the user interacts with the application
## session_state will allow us to preserve the information between the reruns

if "messages" not in st.session_state:
    st.session_state.messages = []

## Input text box for the user
user_input = st.text_input("Enter your question:")

## execute the generate_answer function by passing user query if the user press "ask" button
if st.button("Ask"):
    ## make sure the user input has some msg
    if user_input:
        ## Store the user question in session_state
        ## we store each message as a dictionary containing
        ## role: who sent the msg
        ## content: actual msg
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        ## send the user question to the LLM
        response = generate_answer(user_input)

        ## Store the LLM response in session_state
        st.session_state.messages.append(
            {
                "role":"assistant",
                "content": response
            }
        )

        user_input = ""  ## clear the input text box after the user press "ask" button

## Display the chat history
st.subheader("Chat history")

## loop through the message stored in session_state
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.write(f"User: {msg['content']}")
    else:
        st.write(f"Output: {msg['content']}")