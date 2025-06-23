import streamlit as st
from openai import OpenAI

# Set your OpenAI API key using Streamlit secrets
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("⚠️ OpenAI API key not found. Please add your API key to the secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# Start with a system prompt
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are CyberShield, a kind and caring chatbot who helps people deal with online bullying."},
        {"role": "assistant", "content": "hey, i'm cybershield 💛 what happened? i'm here to help."}
    ]

st.title("CyberShield – Your Cyberbully Support Friend")

# Show past messages
for msg in st.session_state.messages:
    if msg["role"] != "system":  # Don't show system messages to users
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# User input
if user_prompt := st.chat_input("what's on your mind?"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Or gpt-4 if you have access
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.error("Please check your API key and try again.")
