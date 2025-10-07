import streamlit as st
from openai import OpenAI
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("OpenAI API key not found.")
    st.stop()

openai_client = OpenAI(api_key=api_key)

scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)
gs_client = gspread.authorize(creds)

SHEET_NAME = "feedback"
worksheet = gs_client.open(SHEET_NAME).sheet1

if "moderator_messages" not in st.session_state:
    st.session_state.moderator_messages = [
        {"role": "system", "content": "You are an AI chatbot that helps moderators judge cyberbullying scenarios and conversations. You should assess severity, look for patterns, and distinguish between any jokes, and actual risk. DO NOT ASK TOO MANY QUESTIONS. It should communicate in a natural, non-robotic way, understand internet tone, and support the moderators. First, ask what happened. Then, ask a few short follow-up questions to understand the situation. After that, write a short summary report of what happened and suggest 2–3 next steps (like flagging messages, further review, looking at patterns that could pop up in a conversation, etc.). Change what is asked to the person every time and don't repeat questions. Sometimes don't ask questions that might be difficult or sad to answer. Take what they best prefer, elaborate, and continue the conversation. Overall, be helpful and not have too many unnecessary details for the moderators. Do not ask all questions at once, ask gradually over the course of multiple messages but DO NOT ASK TOO MANY QUESTIONS. Make sure to include summary in appropriate place. Your summary should be DETAILED and include insights the moderator otherwise wouldn't have thought of. DO NOT ENGAGE IN OFF TOPIC CONVERSATION."},
        {"role": "assistant", "content": "Hey there, my name is modAI, how would you like me to assist? Please send over the flagged messages or conversations for me to review. Or let me know if you need any other help."}
    ]

if "feedback_synced" not in st.session_state:
    st.session_state.feedback_synced = {}

messages = st.session_state.moderator_messages

st.title("Moderator Recommendations")

for i, msg in enumerate(messages):
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                fb_key = f"fb_{i}"
                selected = st.feedback("thumbs", key = fb_key)
                if selected is not None:
                    prev = st.session_state.feedback_synced.get(fb_key)
                    if prev != selected:
                        email = "ModeratorRecs"
                        feedback = "thumbs up" if selected == 1 else "thumbs down"
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        worksheet.append_row(timestamp, email, feedback)
                        st.session_state.feedback_synced[fb_key] = selected
                        st.toast("Feedback submitted! Thank you!")

if user_prompt := st.chat_input("what's on your mind?"):
    messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.feedback("thumbs", key=f"fb_{len(messages)}")
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {str(e)}")
