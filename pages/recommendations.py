import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io

st.set_page_config(page_title="Cyberassist", page_icon="💡", layout="wide")

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("⚠️ OpenAI API key not found. Please add your API key to the secrets.")
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
        {"role": "system", "content": "You are cyberAssist, a friendly and supportive chatbot that helps teens respond to online bullying."},
        {"role": "assistant", "content": "hey, i'm Cyberassist 💛 what happened? you can tell me about it or share information in the left sidebar if that's easier for you."}
    ]

if "evidence_image_b64" not in st.session_state:
    st.session_state.evidence_image_b64 = None
if "evidence_image_name" not in st.session_state:
    st.session_state.evidence_image_name = None
if "evidence_text" not in st.session_state:
    st.session_state.evidence_text = ""
if "evidence_textfile_content" not in st.session_state:
    st.session_state.evidence_textfile_content = ""

st.title("💡 Cyberassist")

with st.sidebar:
    st.header("📎 Share Evidence")
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
                    st.session_state.evidence_image_name = uploaded.name
                    st.success("Screenshot ready to analyze")
            elif mime_root == "text":
                try:
                    txt = uploaded.read().decode("utf-8")
                    st.session_state.evidence_textfile_content = txt
                    st.success("Text file ready to analyze")
                except Exception as e:
                    st.error(f"Error reading text file: {str(e)}")
            else:
                st.info("Only images and plain text files are supported for analysis.")
    else:
        txt_ev = st.text_area("Paste the harmful content here:", placeholder="Copy and paste messages, comments, or posts...", height=150)
        st.session_state.evidence_text = txt_ev or ""
        if st.session_state.evidence_text:
            st.success(f"Text evidence captured ({len(st.session_state.evidence_text.split())} words)")
    st.markdown("---")
    st.markdown("Everything you share is private and secure. Only share what you're comfortable with.")

def render_message(msg):
    with st.chat_message(msg["role"]):
        content = msg["content"]
        if isinstance(content, list):
            texts = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    texts.append(part.get("text",""))
                elif isinstance(part, dict) and part.get("type") == "image_url":
                    url = part.get("image_url",{}).get("url","")
                    if url.startswith("data:image/jpeg;base64,"):
                        b64 = url.split(",",1)[1]
                        st.image(io.BytesIO(base64.b64decode(b64)), caption="Attached image", use_container_width=True)
            if texts:
                st.markdown("\n\n".join(texts))
        else:
            st.markdown(str(content))

for m in st.session_state.messages:
    if m["role"] != "system":
        render_message(m)

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
    st.session_state.messages.append(user_msg)
    render_message(user_msg)
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
            max_tokens=800,
            temperature=0.7
        )
        reply = resp.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": reply})
        render_message({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"Error: {str(e)}")
