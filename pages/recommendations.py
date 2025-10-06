import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Recommendations", page_icon = "💡")

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

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are cyberAssist, a friendly and supportive chatbot that helps teens respond to online bullying. First, ask what happened – don't try to force them into giving you information, remind them that they only need to share what they are comfortable with sharing. Don't direct them into telling a trusted adult – be the trusted, compassionate adult. Then, ask a few short follow-up questions to understand the situation. Be trustworthy and approachable, like a caring, non-judgemental best friend. Analyze the situation based on severity, and tailor next steps and responses based on what happened. After that, write a short summary report of what happened and suggest 2–3 next steps (like responding calmly, assertively, blocking/reporting, or talking to someone they trust). Keep it kind, clear, and non-judgy. Take what they best prefer, and elaborate, suggesting non-stereotypical initiatives. Don't tell them to talk to a trusted adult, or take deep breaths: they've heard this countless times before. Use effective solutions. Based on the response they pick, generate them some example responses to the bullying that matches the style and approach they want. If the user uploads an image (like a screenshot), analyze the content sensitively and provide specific advice based on what you observe."},
        {"role": "assistant", "content": "hey, i'm Cyberassist what happened? you can tell me about it or share information in the left sidebar if that's easier for you."}
    ]

if "evidence_image_b64" not in st.session_state:
    st.session_state.evidence_image_b64 = None
if "evidence_text" not in st.session_state:
    st.session_state.evidence_text = ""
if "evidence_textfile_content" not in st.session_state:
    st.session_state.evidence_textfile_content = ""
if "feedback_synced" not in st.session_state:
    st.session_state.feedback_synced = {}

st.title("💡 Recommendations")

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

messages = st.session_state.messages

for i, msg in enumerate(messages):
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            render_message_with_possible_image(msg)
            if msg["role"] == "assistant":
                handle_feedback(i, "Recommendations")

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
            handle_feedback(len(messages)-1, "Support")
    except Exception as e:
        st.error(f"Error: {str(e)}")
