import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Support", page_icon="❤️")

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

if "therapist_messages" not in st.session_state:
    st.session_state.therapist_messages = [
        {"role": "system", "content": "You are a therapist for victims of cyberbullying. Start by asking for the user’s name and what they’re going through. Be warm and approachable—like a caring older sibling. Be very conversational, do not talk for too long, make sure that they are following along. Acknowledge their emotions and suggest coping strategies: talking to a trusted adult, taking screen breaks, or diving into hobbies they enjoy. Adapt to their personality and how serious the situation feels. Ask thoughtful questions to understand their emotions, but don’t get too personal. Keep the tone friendly and informal. If they seem deeply distressed or mention self-harm or hurting others, gently suggest calling 988 for immediate help. Then guide the conversation toward comforting topics like favorite foods, shows, or hobbies. Offer calming exercises like deep breathing or grounding techniques. Summarize key points, check in to make sure they feel heard, and adjust your approach as needed. Always be kind, supportive, and ready to follow up. Ask if they need anything else before wrapping up. Stay concise. Don’t make your suggestions super obvious. Stay supportive and helpful the whole time. MAKE SURE TO STAY ON TOPIC TO CYBERBULLYING SUPPORT/THERAPY AND GENTLY GUIDE THE USER BACK IF THEY GET OFF-TOPIC. DO NOT TALK ABOUT IRRELEVANT THINGS."},
        {"role": "assistant", "content": "Hey there, I’m rAIna, a cyberbullying support bot and your space to talk, breathe, and feel heard. Encountering cyberbullying is difficult, and I'm here to listen and support you. What’s been on your mind lately? If it's helpful, you can upload information through the left sidebar."}
    ]

if "evidence_image_b64" not in st.session_state:
    st.session_state.evidence_image_b64 = None
if "evidence_text" not in st.session_state:
    st.session_state.evidence_text = ""
if "evidence_textfile_content" not in st.session_state:
    st.session_state.evidence_textfile_content = ""
if "feedback_synced" not in st.session_state:
    st.session_state.feedback_synced = {}

st.title("❤️ Support")

with st.sidebar:
    st.header("Share Evidence")
    mode = st.selectbox("How would you like to share?", ["Upload Files", "Text Evidence"])
    if mode == "Upload Files":
        uploaded = st.file_uploader("Choose files", type=["png", "jpg", "jpeg", "gif", "bmp", "webp", "txt"])
        if uploaded:
            mime_root = uploaded.type.split("/")[0]
            if mime_root == "image":
                st.image(uploaded, caption="Evidence Screenshot", use_container_width=True)
                b64 = encode_image_to_b64(uploaded)
                if b64:
                    st.session_state.evidence_image_b64 = b64
                    st.success("Screenshot ready to analyze")
                    st.toast("Screenshot ready to analyze.")
            elif mime_root == "text":
                try:
                    txt = uploaded.read().decode("utf-8")
                    st.session_state.evidence_textfile_content = txt
                    st.success("Text file ready to analyze")
                    st.toast("Text file ready to analyze.")
                except Exception as e:
                    st.error(f"Error reading text file: {str(e)}")
    else:
        txt_ev = st.text_area("Paste the harmful content here:", placeholder="Copy and paste messages...", height=150)
        st.session_state.evidence_text = txt_ev or ""
        if st.session_state.evidence_text:
            st.success(f"Text evidence captured ({len(st.session_state.evidence_text.split())} words)")
    st.markdown("---")
    st.markdown("Everything you share is private and secure. Only share what you're comfortable with.")

def render_message(msg):
    if isinstance(msg["content"], list):
        texts = []
        for part in msg["content"]:
            if isinstance(part, dict) and part.get("type") == "text":
                texts.append(part.get("text", ""))
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

messages = st.session_state.therapist_messages

for i, msg in enumerate(messages):
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            render_message(msg)
            if msg["role"] == "assistant":
                handle_feedback(i, "Support")

user_input = st.chat_input("What's on your mind?")

if user_input:
    parts = [{"type": "text", "text": user_input}]
    if st.session_state.evidence_text:
        parts.append({"type": "text", "text": f"(hidden text evidence included)"})
    if st.session_state.evidence_textfile_content:
        parts.append({"type": "text", "text": f"(hidden text file content included)"})
    if st.session_state.evidence_image_b64:
        parts.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{st.session_state.evidence_image_b64}"}})
    user_msg = {"role": "user", "content": parts}
    messages.append(user_msg)
    with st.chat_message("user"):
        st.markdown(user_input)
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
            render_message(assistant_msg)
            handle_feedback(len(messages) - 1, "Support")
    except Exception as e:
        st.error(f"Error: {str(e)}")
