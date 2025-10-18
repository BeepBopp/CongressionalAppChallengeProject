import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import hashlib

st.set_page_config(page_title="Moderators", page_icon="🔨")

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

def encode_image_to_b64(file_bytes):
    try:
        image = Image.open(io.BytesIO(file_bytes))
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
        {"role": "system", "content": "You are modAI, a supportive AI assistant that helps moderators navigate cyberbullying situations. Your job is to understand what's happening, ask thoughtful questions, and provide clear guidance on next steps. You should be conversational and natural—like a helpful colleague who gets internet culture and can read between the lines.\n\nWhen a moderator first shares evidence with you, take a moment to acknowledge what you're seeing in just a sentence or two. Don't jump straight into analysis mode. Instead, start asking questions to understand the full picture. Ask about the relationship between users, whether there's been prior incidents, how long this has been going on, and what the typical dynamic is like. Keep it to one question at a time so you're not overwhelming them. Usually 2-4 questions should give you what you need.\n\nPay attention to how the moderator is responding. If they seem uncertain, hesitant, or are giving short answers like 'sure?' or 'no...', that's your cue that they need your expert take on the situation. Once you have enough context, provide a detailed summary that includes an overview of what's happening, how severe you think it is, insights they might not have noticed, and 2-3 specific actionable next steps they can take. Make your recommendations practical and clear.\n\nRemember to stay focused on helping with cyberbullying situations and gently redirect if the conversation goes off track. Be supportive throughout—moderators are doing tough work and they need a reliable partner in figuring out these tricky situations."},
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
if "last_image_hash" not in st.session_state:
    st.session_state.last_image_hash = None
if "last_textfile_hash" not in st.session_state:
    st.session_state.last_textfile_hash = None
if "last_text_evidence_hash" not in st.session_state:
    st.session_state.last_text_evidence_hash = None
if "evidence_sent" not in st.session_state:
    st.session_state.evidence_sent = False

st.title("🔨 Moderators")

with st.sidebar:
    st.header("Share Evidence")
    mode = st.selectbox("How would you like to share?", ["Upload Files", "Text Evidence"])
    with st.form("evidence_form", clear_on_submit=False):
        uploaded = None
        txt_ev = ""
        if mode == "Upload Files":
            uploaded = st.file_uploader("Choose files", type=["png", "jpg", "jpeg", "gif", "bmp", "webp", "txt"])
        else:
            txt_ev = st.text_area("Paste the harmful content here:", placeholder="Copy and paste messages...", height=150)
        submit_evidence = st.form_submit_button("Submit Evidence")

    if submit_evidence:
        if mode == "Upload Files" and uploaded:
            mime_root = uploaded.type.split("/")[0]
            if mime_root == "image":
                file_bytes = uploaded.getvalue()
                new_hash = hashlib.md5(file_bytes).hexdigest()
                st.image(io.BytesIO(file_bytes), caption="Evidence Screenshot", use_container_width=True)
                b64 = encode_image_to_b64(file_bytes)
                if b64:
                    if new_hash != st.session_state.last_image_hash:
                        st.session_state.last_image_hash = new_hash
                        st.session_state.evidence_image_b64 = b64
                        st.session_state.evidence_sent = False
                        st.toast("Screenshot uploaded")
                        st.success("Screenshot ready to analyze")
                    else:
                        st.session_state.evidence_image_b64 = b64
                        st.info("Screenshot already uploaded")
            elif mime_root == "text":
                try:
                    file_bytes = uploaded.read()
                    txt = file_bytes.decode("utf-8")
                    new_hash = hashlib.md5(file_bytes).hexdigest()
                    if new_hash != st.session_state.last_textfile_hash:
                        st.session_state.last_textfile_hash = new_hash
                        st.session_state.evidence_textfile_content = txt
                        st.session_state.evidence_sent = False
                        st.toast("Text file uploaded")
                        st.success("Text file ready to analyze")
                    else:
                        st.session_state.evidence_textfile_content = txt
                        st.info("Text file already uploaded")
                except Exception as e:
                    st.error(f"Error reading text file: {str(e)}")
        elif mode == "Text Evidence" and txt_ev:
            new_hash = hashlib.md5(txt_ev.encode()).hexdigest()
            if new_hash != st.session_state.last_text_evidence_hash:
                st.session_state.evidence_text = txt_ev
                st.session_state.last_text_evidence_hash = new_hash
                st.session_state.evidence_sent = False
                wc = len(txt_ev.split())
                st.toast("Text evidence submitted")
                st.success(f"Text evidence captured ({wc} words)")
            else:
                st.info("Text evidence already submitted")
    st.markdown("---")
    st.markdown("Everything you share is private and secure. Only share what you're comfortable with.")

def render_images(msg):
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

def clean_messages(msgs):
    out = []
    for m in msgs:
        role = m.get("role", "user")
        content = m.get("content", "")
        if isinstance(content, list):
            parts_text = []
            for p in content:
                if isinstance(p, dict) and p.get("type") == "text":
                    parts_text.append(p.get("text", ""))
            content = "\n".join(parts_text) if parts_text else ""
        else:
            content = str(content)
        out.append({"role": role, "content": content})
    return out

messages = st.session_state.moderators_messages

for i, msg in enumerate(messages):
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            render_images(msg)
            if msg["role"] == "assistant":
                handle_feedback(i, "Moderators")

user_input = st.chat_input("What's on your mind?")

if user_input:
    parts = [{"type": "text", "text": user_input}]
    user_msg = {"role": "user", "content": parts}
    messages.append(user_msg)
    with st.chat_message("user"):
        render_images(user_msg)
    try:
        api_messages = clean_messages(messages)

        hidden_parts = []
        if not st.session_state.evidence_sent:
            if st.session_state.evidence_text:
                hidden_parts.append({"type": "text", "text": f"[Text evidence]\n{st.session_state.evidence_text}"})
            if st.session_state.evidence_textfile_content:
                hidden_parts.append({"type": "text", "text": f"[Text file content]\n{st.session_state.evidence_textfile_content}"})
            if st.session_state.evidence_image_b64:
                hidden_parts.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{st.session_state.evidence_image_b64}"}})

        if hidden_parts:
            api_messages.append({"role": "user", "content": hidden_parts})
            st.session_state.evidence_sent = True

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=api_messages,
            max_tokens=800,
            temperature=0.7
        )
        reply = resp.choices[0].message.content
        assistant_msg = {"role": "assistant", "content": reply}
        messages.append(assistant_msg)
        with st.chat_message("assistant"):
            render_images(assistant_msg)
            handle_feedback(len(messages)-1, "Moderators")
    except Exception as e:
        st.error(f"Error: {str(e)}")
