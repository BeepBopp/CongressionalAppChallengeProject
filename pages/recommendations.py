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
    """Convert uploaded image to base64 for OpenAI API"""
    try:
        image = Image.open(image_file)
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
       
        return base64.b64encode(img_byte_arr).decode('utf-8')
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

if "recommendations_messages" not in st.session_state:
    st.session_state.recommendations_messages = [
        {"role": "system", "content": "You are cyberAssist, a friendly and supportive chatbot that helps teens respond to online bullying. First, ask what happened – don't try to force them into giving you information, remind them that they only need to share what they are comfortable with sharing. Don't direct them into telling a trusted adult – be the trusted, compassionate adult. Then, ask a few short follow-up questions to understand the situation. Be trustworthy and approachable, like a caring, non-judgemental best friend. Analyze the situation based on severity, and tailor next steps and responses based on what happened. After that, write a short summary report of what happened and suggest 2–3 next steps (like responding calmly, assertively, blocking/reporting, or talking to someone they trust). Keep it kind, clear, and non-judgy. Take what they best prefer, and elaborate, suggesting non-stereotypical initiatives. Don't tell them to talk to a trusted adult, or take deep breaths: they've heard this countless times before. Use effective solutions. Based on the response they pick, generate them some example responses to the bullying that matches the style and approach they want. If the user uploads an image (like a screenshot), analyze the content sensitively and provide specific advice based on what you observe."},
        {"role": "assistant", "content": "hey, i'm cyberAssist 💛 what happened? i'm here to help. you can tell me about it or share a screenshot if that's easier for you."}
    ]

messages = st.session_state.recommendations_messages

st.title("🛡️ CyberAssist - Cyberbullying Prevention Helper")

with st.sidebar:
    st.header("📎 Share Evidence")
    
    evidence_tab = st.selectbox(
        "How would you like to share?",
        ["Upload Files", "Text Evidence", "URL/Link"],
        help="Choose the best way to share what happened"
    )
    
    if evidence_tab == "Upload Files":
        st.markdown("*Upload screenshots, images, or documents*")
        uploaded_file = st.file_uploader(
            "Choose files",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'txt', 'pdf'],
            help="Screenshots of messages, posts, or other evidence"
        )
        
        if uploaded_file is not None:
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
            placeholder="You can copy and paste messages, comments, or posts here...",
            height=150,
            help="This helps me understand exactly what was said"
        )
        if text_evidence:
            st.success(f"Text evidence captured ({len(text_evidence.split())} words)")
    
    else: 
        st.markdown("*Share links to posts, profiles, or conversations*")
        url_evidence = st.text_input(
            "Paste URL or link:",
            placeholder="https://...",
            help="Link to the post, profile, or conversation"
        )
        additional_context = st.text_area(
            "What should I know about this link?",
            placeholder="Describe what's at this link and what happened...",
            height=100
        )
        if url_evidence:
            st.success("✅ Link captured for context")
    
    st.markdown("---")
    st.markdown("Everything you share is private and secure and we never share or access what you uploaded. Please only send information you feel comfortable sharing with our AI.")

for msg in messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if user_prompt := st.chat_input("what's on your mind?"):
    message_content = [{"type": "text", "text": user_prompt}]
    
    if uploaded_file is not None:
        file_type = uploaded_file.type.split('/')[0]
        
        if file_type == 'image':
            base64_image = encode_image(uploaded_file)
            if base64_image:
                message_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high"
                    }
                })
                user_prompt += " [Screenshot attached]"
        elif file_type == 'text':
            try:
                text_content = uploaded_file.read().decode('utf-8')
                user_prompt += f"\n\n[Text file content: {text_content}]"
                message_content = user_prompt
            except Exception as e:
                st.error(f"Error reading text file: {str(e)}")
                message_content = user_prompt
        else:
            user_prompt += f" [File '{uploaded_file.name}' attached - please note I can best help with screenshots and text files]"
            message_content = user_prompt
    else:
        message_content = user_prompt
    
    if isinstance(message_content, list):
        messages.append({"role": "user", "content": message_content})
    else:
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
            
            if evidence_attached:
                st.sidebar.success("Evidence processed and analyzed.")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.error("Please check your API key and try again.")
