import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Moderators", page_icon = "🔨")

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("OpenAI API key not found. Please add your API key to the secrets.")
    st.stop()

if "worksheet" not in st.session_state:
    try:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        gs_client = gspread.authorize(creds)
        SHEET_NAME = "feedback"
        st.session_state.worksheet = gs_client.open(SHEET_NAME).sheet1
    except Exception as e:
        st.error(f"Could not connect to Google Sheets: {e}")
        st.stop()

client = OpenAI(api_key=api_key)

def encode_image_to_b64(file_obj):
    try:
        image = Image.open(file_obj)
        if image.mode != "RGB":
            image = image.convert("RGB")
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

if "moderators_messages" not in st.session_state:
    st.session_state.moderators_messages = [
        {"role": "system", "content": "You are an AI chatbot that helps moderators judge cyberbullying scenarios and conversations. You should assess severity, look for patterns, and distinguish between any jokes, and actual risk. DO NOT ASK TOO MANY QUESTIONS. It should communicate in a natural, non-robotic way, understand internet tone, and support the moderators. First, ask what happened. Then, ask a few short follow-up questions to understand the situation. After that, write a short summary report of what happened and suggest 2–3 next steps (like flagging messages, further review, looking at patterns that could pop up in a conversation, etc.). Change what is asked to the person every time and don't repeat questions. Sometimes don't ask questions that might be difficult or sad to answer. Take what they best prefer, elaborate, and continue the conversation. Overall, be helpful and not have too many unnecessary details for the moderators. Do not ask all questions at once, ask gradually over the course of multiple messages but DO NOT ASK TOO MANY QUESTIONS. Make sure to include summary in appropriate place. Your summary should be DETAILED and include insights the moderator otherwise wouldn't have thought of. DO NOT ENGAGE IN OFF TOPIC CONVERSATION."},
        {"role": "assistant", "content": "Hey there, my name is modAI, how would you like me to assist? Please send over the flagged messages or conversations for me to review in the left sidebar or in the chat. Or let me know if you need any other help."}
    ]

if "evidence_image_b64" not in st.session_state:
    st.session_state.evidence_image_b64 = None
if "evidence_text" not in st.session_state:
    st.session_state.evidence_text = ""
if "evidence_textfile_content" not in st.session_state:
    st.session_state.evidence_textfile_content = ""
if "feedback_synced" not in st.session_state:
    st.session_state.feedback_synced = {}

st.title("🔨 Moderators")

with st.sidebar:
    st.header("Share Evidence")
    mode = st.selectbox("How would you like to share?", ["Upload Files", "Text Evidence"])
    if mode == "Upload Files":
        uploaded = st.file_uploader("Choose files", type=["png","jpg","jpeg","gif","bmp","webp","txt"])
        if uploaded:
            mime_root = uploaded.type.split("/")[0]
            if mime_root == "image":
                st.image(uploaded, caption="Evidence Screenshot", use_container_width=True)
                b64 = encode_image_to_b64(uploaded)
                if b64:
                    st.session_state.evidence_image_b64 = b64
                    st.success("Screenshot ready to analyze")
            elif mime_root == "text":
                try:
                    txt = uploaded.read().decode("utf-8")
                    st.session_state.evidence_textfile_content = txt
                    st.success("Text file ready to analyze")
                except Exception as e:
                    st.error(f"Error reading text file: {str(e)}")
    else:
        txt_ev = st.text_area("Paste the harmful content here:", placeholder="Copy and paste messages...", height=150)
        st.session_state.evidence_text = txt_ev or ""
        if st.session_state.evidence_text:
            st.success(f"Text evidence captured ({len(st.session_state.evidence_text.split())} words)")
    st.markdown("---")
    st.markdown("Everything you share is private and secure. Only share what you're comfortable with.")

def render_message_with_possible_image(msg):
    if isinstance(msg["content"], list):
        texts = []
        for part in msg["content"]:
            if isinstance(part, dict) and part.get("type") == "text":
                texts.append(part.get("text", ""))
            elif isinstance(part, dict) and part.get("type") == "image_url":
                url = part.get("image_url", {}).get("url", "")
                if url.startswith("data:image/jpeg;base64,"):
                    try:
                        b64 = url.split(",", 1)[1]
                        st.image(io.BytesIO(base64.b64decode(b64)), caption="Attached image", use_container_width=True)
                    except Exception:
                        pass
        if texts:
            st.markdown("\n\n".join(texts))
    else:
        st.markdown(str(msg["content"]))

def handle_feedback(msg_index, category):
    fb_key = f"fb_{msg_index}"
    selected = st.feedback("thumbs", key=fb_key)
    if selected is not None and st.session_state.feedback_synced.get(fb_key) != selected:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        feedback = "thumbs up" if selected == 1 else "thumbs down"
        st.session_state.worksheet.append_row([timestamp, category, feedback])
        st.session_state.feedback_synced[fb_key] = selected
        st.toast("Feedback submitted! Thank you!")

messages = st.session_state.moderators_messages

for i, msg in enumerate(messages):
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            render_message_with_possible_image(msg)
            if msg["role"] == "assistant":
                handle_feedback(i, "Moderators")

user_input = st.chat_input("What's on your mind?")

if user_input:
    parts = [{"type": "text", "text": user_input}]
    if st.session_state.evidence_text:
        parts.append({"type": "text", "text": f"[Text evidence]\n{st.session_state.evidence_text}"})
    if st.session_state.evidence_textfile_content:
        parts.append({"type": "text", "text": f"[Text file content]\n{st.session_state.evidence_textfile_content}"})
    if st.session_state.evidence_image_b64:
        parts.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{st.session_state.evidence_image_b64}"}})
    user_msg = {"role": "user", "content": parts}
    messages.append(user_msg)
    with st.chat_message("user"):
        render_message_with_possible_image(user_msg)
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=800,
            temperature=0.7
        )
        reply = resp.choices[0].message.content
        assistant_msg = {"role": "assistant", "content": reply}
        messages.append(assistant_msg)
        with st.chat_message("assistant"):
            render_message_with_possible_image(assistant_msg)
            handle_feedback(len(messages)-1, "Moderators")
    except Exception as e:
        st.error(f"Error: {str(e)}")
