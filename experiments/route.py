import os

import streamlit as st
from dotenv import load_dotenv
from routellm.controller import Controller

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv('GROQ_API_KEY')
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

client = Controller(
    routers=["mf"],
    strong_model="gpt-4o",
    weak_model="groq/llama3-8b-8192",
)

st.title("Chatbot using RouteLLM")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "model" in message:
            st.caption(f"Model: {message['model']}")

if prompt := st.chat_input("Ask a question?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    api_messages = [
                       {"role": "system", "content": "You are a helpful assistant."}
                   ] + [
                       {"role": m["role"].lower(), "content": m["content"]}
                       for m in st.session_state.messages
                   ]

    try:
        response = client.chat.completions.create(
            model="router-mf-0.11593",
            messages=api_messages
        )

        with st.chat_message("assistant"):++
            st.markdown(response.choices[0].message.content)
            st.caption(f"Model: {response.model}")

        st.session_state.messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content,
            "model": response.model
        })
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
