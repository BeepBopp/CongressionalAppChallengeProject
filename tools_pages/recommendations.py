import streamlit as st
from openai import OpenAI

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("⚠️ OpenAI API key not found. Please add your API key to the secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# Use a unique key for recommendations chat
if "recommendations_messages" not in st.session_state:
    st.session_state.recommendations_messages = [
        {"role": "system", "content": "You are CyberAssist, a friendly and supportive chatbot that helps teens respond to online bullying. First, ask what happened. Then, ask a few short follow-up questions to understand the situation. After that, write a short summary report of what happened and suggest 2–3 next steps (like responding calmly, assertively, blocking/reporting, talking to someone they trust, etc.). Keep it kind, clear, and non-judgy. Take what they best prefer, elaborate, and continue the conversation. Keep text non-capitalized so it is more welcoming."},
        {"role": "assistant", "content": "hey, i'm cyberAssist 💛 what happened? i'm here to help."}
    ]

messages = st.session_state.recommendations_messages

st.title("Cyberbullying Recommendations")

# Show past messages
for msg in messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Handle user input
if user_prompt := st.chat_input("what's on your mind?"):
    messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.error("Please check your API key and try again.")
