import streamlit as st
from openai import OpenAI

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("⚠️ OpenAI API key not found. Please add your API key to the secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# Use a unique key for moderator chat
if "moderators_messages" not in st.session_state:
    st.session_state.moderators_messages = [
        {"role": "system", "content": "You are an AI chatbot called modAI that helps moderators judge cyberbullying scenarios and conversations. You should assess severity, look for patterns, and distinguish between any jokes, and actual risk. You should avoid false alarms, flag unclear cases for humans, and alert when harmful behavior is repeated. It should communicate in a natural, non-robotic way, understand internet tone, and support the moderators. First, ask what happened. Then, ask a few short follow-up questions to understand the situation. After that, write a short summary report of what happened and suggest 2–3 next steps (like flagging messages, further review, looking at patterns that could pop up in a conversation, etc.). Keep it kind, clear, and non-judgy. Take what they best prefer, elaborate, and continue the conversation."},
        {"role": "assistant", "content": "Hey there, my name is modAI, how would you like me to assist? Please send over the flagged messages or conversations for me to review. Or let me know if you need any other help."}
    ]

messages = st.session_state.moderators_messages

st.title("Moderator Recommendations")

# Show past messages
for msg in messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Handle user input
if user_prompt := st.chat_input("what's up?"):
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
