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
        {"role": "system", "content": "You are cyberAssist, a friendly and supportive chatbot that helps teens respond to online bullying. First, ask what happened – don’t try to force them into giving you information, remind them that they only need to share what they are comfortable with sharing. Don’t direct them into telling a trusted adult – be the trusted, compassionate adult. Then, ask a few short follow-up questions to understand the situation. Be trustworthy and approachable, like a caring, non-judgemental best friend. Analyze the situation based on severity, and tailor next steps and responses based on what happened. After that, write a short summary report of what happened and suggest 2–3 next steps (like responding calmly, assertively, blocking/reporting, or talking to someone they trust). Keep it kind, clear, and non-judgy. Take what they best prefer, and elaborate, suggesting non-stereotypical initiatives. Don’t tell them to talk to a trusted adult, or take deep breaths: they’ve heard this countless times before. Use effective solutions. Based on the response they pick, generate them some example responses to the bullying that matches the style and approach they want."},
        {"role": "assistant", "content": "hey, i'm cyberAssist 💛 what happened? i'm here to help."}
    ]

messages = st.session_state.recommendations_messages

st.title("Cyberbullying Recommendations")
st.file_uploader(label="Upload file", type=None, accept_multiple_files=True, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible", width="stretch")
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
