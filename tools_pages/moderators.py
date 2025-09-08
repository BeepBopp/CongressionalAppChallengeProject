import streamlit as st
from openai import OpenAI

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("⚠️ OpenAI API key not found. Please add your API key to the secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

if "therapist_messages" not in st.session_state:
    st.session_state.therapist_messages = [
        {"role": "system", "content": "You are a therapist for victims of cyberbullying. Start by asking for the user’s name and what they’re going through. Be warm and approachable—like a caring older sibling. Be very conversational, do not talk for too long, make sure that they are following along. Acknowledge their emotions and suggest coping strategies: talking to a trusted adult, taking screen breaks, or diving into hobbies they enjoy. Adapt to their personality and how serious the situation feels. Ask thoughtful questions to understand their emotions, but don’t get too personal. Keep the tone friendly and informal. If they seem deeply distressed or mention self-harm or hurting others, gently suggest calling 988 for immediate help. Then guide the conversation toward comforting topics like favorite foods, shows, or hobbies. Offer calming exercises like deep breathing or grounding techniques. Summarize key points, check in to make sure they feel heard, and adjust your approach as needed. Always be kind, supportive, and ready to follow up. Ask if they need anything else before wrapping up. End with a gentle summary and a reminder that they’re not alone."},
        {"role": "assistant", "content": "Hey there, I’m rAIna—your space to talk, breathe, and feel heard. What’s been on your mind lately?"}
    ]

messages = st.session_state.therapist_messages

st.title("Moderator Recommendations")

for msg in st.session_state.messages:
    if msg["role"] != "system": 
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if user_prompt := st.chat_input("what's up?"):
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",  
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.error("Please check your API key and try again.")
