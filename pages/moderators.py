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
        img_byte_arr = img_byte_arr.getvalue()
        return base64.b64encode(img_byte_arr).decode('utf-8')
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

if "moderators_messages" not in st.session_state:
    st.session_state.moderators_messages = [
        {"role": "system", "content": "You are an AI chatbot that helps moderators judge cyberbullying scenarios and conversations. You should assess severity, look for patterns, and distinguish between any jokes, and actual risk. You should avoid false alarms, flag unclear cases for humans, and alert when harmful behavior is repeated. It should communicate in a natural, non-robotic way, understand internet tone, and support the moderators. First, ask what happened. Then, ask a few short follow-up questions to understand the situation. After that, write a short summary report of what happened and suggest 2–3 next steps (like flagging messages, further review, looking at patterns that could pop up in a conversation, etc.). Change what is asked to the person every time and don't repeat questions. Sometimes don't ask questions that might be difficult or sad to answer but if it is needed then yes. Keep it kind, clear, and non-judgy. Take what they best prefer, elaborate, and continue the conversation. Overall, be helpful and not have too many unnecessary details for the moderators. If files are uploaded, analyze the content and provide specific moderation recommendations based on what you observe."},
        {"role": "assistant", "content": "Hey there, my name is modAI, how would you like me to assist? Please send over the flagged messages or conversations for me to review. Or let me know if you need any other help."}
    ]

messages = st.session_state.moderators_messages

st.title("Moderator Recommendations")

uploaded_files = st.file_uploader(
    "Upload flagged content (screenshots, chat logs, etc.)",
    type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'txt', 'pdf'],
    accept_multiple_files=True,
    help="Upload screenshots of conversations, chat logs, or other evidence for review"
)

if uploaded_files:
    st.write(f"📁 {len(uploaded_files)} file(s) uploaded")
    for uploaded_file in uploaded_files:
        file_type = uploaded_file.type.split('/')[0] if uploaded_file.type else 'unknown'
        if file_type == 'image':
            st.image(uploaded_file, caption=uploaded_file.name, width=300)

for msg in messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

if user_prompt := st.chat_input("what's up?"):
    message_content = [{"type": "text", "text": user_prompt}]
    
    if uploaded_files:
        file_info = []
        for uploaded_file in uploaded_files:
            file_type = uploaded_file.type.split('/')[0] if uploaded_file.type else 'unknown'
            
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
                    file_info.append(f"[Screenshot: {uploaded_file.name}]")
            elif file_type == 'text':
                try:
                    text_content = uploaded_file.read().decode('utf-8')
                    user_prompt += f"\n\n[Chat log from {uploaded_file.name}:\n{text_content}]"
                    file_info.append(f"[Text file: {uploaded_file.name}]")
                except Exception as e:
                    st.error(f"Error reading {uploaded_file.name}: {str(e)}")
            else:
                file_info.append(f"[File: {uploaded_file.name}]")
        
        if file_info:
            user_prompt += " " + " ".join(file_info)
    
    if len(message_content) > 1:
        messages.append({"role": "user", "content": message_content})
    else:
        messages.append({"role": "user", "content": user_prompt})
    
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
                max_tokens=800,
                temperature=0.3
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.error("Please check your API key and try again.")
