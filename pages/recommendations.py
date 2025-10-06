import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io

try:
    api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("⚠️ OpenAI API key not found. Please add your API key to the secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

def encode_image(image_file):
    try:
        image = Image.open(image_file)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        return base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

if "recommendations_messages" not in st.session_state:
    st.session_state.recommendations_messages = [
        {"role": "system", "content": "You are cyberAssist, a friendly and supportive chatbot that helps teens respond to online bullying..."},
        {"role": "assistant", "content": "hey, i'm cyberAssist 💛 what happened? you can tell me about it or share a screenshot if that's easier for you."}
    ]

messages = st.session_state.recommendations_messages

st.title("💡 Cyberassist")

col_main, col_spacer, col_right = st.columns([4, 0.5, 2])

with col_right:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.header("📎 Share Evidence")
    evidence_tab = st.selectbox(
        "How would you like to share?",
        ["Upload Files", "Text Evidence", "URL/Link"],
        help="Choose the best way to share what happened"
    )
    
    uploaded_file = None
    text_evidence = None
    url_evidence = None
    additional_context = None
    
    if evidence_tab == "Upload Files":
        st.markdown("*Upload screenshots, images, or documents*")
        uploaded_file = st.file_uploader(
            "Choose files",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'txt', 'pdf'],
            help="Screenshots of messages, posts, or other evidence"
        )
        if uploaded_file:
            file_type = uploaded_file.type.split('/')[0]
            if file_type == 'image':
                st.image(uploaded_file, caption="Evidence Screenshot", use_container_width=True)
                st.success("Screenshot ready to analyze")
            else:
                st.success(f"File '{uploaded_file.name}' ready to analyze")
    
    elif evidence_tab == "Text Evidence":
        st.markdown("*Copy and paste messages, comments, or posts*")
        text_evidence = st.text_area(
            "Paste the harmful content here:",
            placeholder="Copy and paste messages, comments, or posts...",
            height=150
        )
        if text_evidence:
            st.success(f"Text evidence captured ({len(text_evidence.split())} words)")
    
    else:
        st.markdown("*Share links to posts, profiles, or conversations*")
        url_evidence = st.text_input("Paste URL or link:", placeholder="https://...")
        additional_context = st.text_area(
            "What should I know about this link?",
            placeholder="Describe what's at this link and what happened...",
            height=100
        )
        if url_evidence:
            st.success("Link captured for context")
    
    st.markdown("---")
    st.markdown("Everything you share is private and secure. Only share what you're comfortable with.")

with col_main:
    for msg in messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if user_prompt := st.chat_input("What's on your mind?"):
        message_content = user_prompt
        if uploaded_file:
            file_type = uploaded_file.type.split('/')[0]
            if file_type == 'image':
                base64_image = encode_image(uploaded_file)
                if base64_image:
                    message_content += " [Screenshot attached]"
            elif file_type == 'text':
                try:
                    text_content = uploaded_file.read().decode('utf-8')
                    message_content += f"\n\n[Text file content: {text_content}]"
                except Exception as e:
                    st.error(f"Error reading text file: {str(e)}")
            else:
                message_content += f" [File '{uploaded_file.name}' attached]"
        elif text_evidence:
            message_content += f"\n\n[Text evidence: {text_evidence}]"
        elif url_evidence:
            message_content += f"\n\n[URL: {url_evidence} | Context: {additional_context}]"
        
        messages.append({"role": "user", "content": message_content})
        
        with st.chat_message("user"):
            st.markdown(user_prompt)
        
        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=800,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Error: {str(e)}")
