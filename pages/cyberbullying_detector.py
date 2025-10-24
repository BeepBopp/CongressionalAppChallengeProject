import streamlit as st
from openai import OpenAI
from datetime import datetime
import base64
from PIL import Image
import gspread
from google.oauth2.service_account import Credentials

api_key = st.secrets["OPENAI_API_KEY"]

GPT_MODEL = "gpt-4.1-mini"
VISION_MODEL = "gpt-4o-mini"

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
gs_client = gspread.authorize(creds)
SHEET_NAME = "identifier-feedback"
worksheet = gs_client.open(SHEET_NAME).sheet1

if "feedback_synced" not in st.session_state:
    st.session_state.feedback_synced = {}
if "results" not in st.session_state:
    st.session_state.results = {"text": {}, "image": {}}

def classify_with_gpt(text):
    try:
        prompt = f"""
You are a content moderation assistant. Given a user message, determine if it contains cyberbullying or harmful content.
Respond in the following format:
Label: <cyberbullying / not cyberbullying>
Explanation: <1-3 sentence explanation why you chose that label>
Message: \"{text}\"
"""
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a content moderation assistant trained to detect cyberbullying."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        reply = response.choices[0].message.content
        lines = reply.strip().split("\n")
        label = "unknown"
        explanation = ""
        for line in lines:
            if line.lower().startswith("label:"):
                label = line.split(":", 1)[1].strip().lower()
            if line.lower().startswith("explanation:"):
                explanation = line.split(":", 1)[1].strip()
        return label, explanation
    except Exception as e:
        st.error(f"OpenAI API Error: {e}")
        return "error", "Failed to get a response from the model."

def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def extract_text_from_image(image_file):
    base64_image = encode_image(image_file)
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract all text visible in this image. Return only the exact text found, maintaining line breaks where appropriate."},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                    ]
                }
            ],
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        return None

st.title("🚨 Cyberbullying Detection")

tab1, tab2 = st.tabs(["Text Input", "Screenshot Upload"])

with tab1:
    st.subheader("🔍 Analyze a Text Message")
    user_input = st.text_area("Enter a message or comment to analyze:", height=150)
    if st.button("Analyze Text"):
        if user_input:
            with st.spinner("Analyzing..."):
                label, explanation = classify_with_gpt(user_input)
            st.session_state.results["text"] = {
                "label": label,
                "explanation": explanation,
                "input": user_input
            }
        else:
            st.warning("Please enter some text to analyze.")

    if st.session_state.results["text"]:
        result = st.session_state.results["text"]
        label, explanation, user_input = result["label"], result["explanation"], result["input"]

        if label == "cyberbullying":
            st.error("**Prediction: Cyberbullying**")
        elif label == "not cyberbullying":
            st.success("**Prediction: Not Cyberbullying**")
        else:
            st.warning("**Prediction: Could not determine**")

        st.subheader("Explanation")
        st.write(explanation)

        if label == "cyberbullying":
            st.write("\nCyberbullying can be especially hard to deal with. Would you like to check out our other features to cope with this possible cyberbullying?")
            st.link_button("Chat with our AI Support Bot to receive help with this situation", "https://cybershield.streamlit.app/therapist")
            st.link_button("Generate potential responses and next steps with our AI Recommendations Bot", "https://cybershield.streamlit.app/recommendations")
            st.link_button("Moderators: Use our AI Moderator Assistant for possible courses of action", "https://cybershield.streamlit.app/moderators")

        st.write("\nWas our classification accurate? (Only share feedback if you are comfortable with sharing your message with us)")
        fb_key = "feedback_text"
        selected = st.feedback("thumbs", key=fb_key)
        if selected is not None:
            prev = st.session_state.feedback_synced.get(fb_key)
            if prev != selected:
                correct = "thumbs up" if selected == 1 else "thumbs down"
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                worksheet.append_row([timestamp, correct, label, user_input])
                st.session_state.feedback_synced[fb_key] = selected
                st.toast("Feedback submitted! Thank you!")

with tab2:
    st.subheader("📸 Analyze a Screenshot")
    uploaded_file = st.file_uploader("Upload a screenshot containing text to analyze", type=["png", "jpg", "jpeg"])
    if st.button("Extract & Analyze") and uploaded_file is not None:
        with st.spinner("Processing image..."):
            uploaded_file.seek(0)
            extracted_text = extract_text_from_image(uploaded_file)
            if extracted_text:
                label, explanation = classify_with_gpt(extracted_text)
                st.session_state.results["image"] = {
                    "label": label,
                    "explanation": explanation,
                    "input": extracted_text
                }
            else:
                st.error("Failed to extract text from the image. Please try a clearer image.")

    if st.session_state.results["image"]:
        result = st.session_state.results["image"]
        label, explanation, extracted_text = result["label"], result["explanation"], result["input"]

        st.subheader("Extracted Text")
        st.text(extracted_text)

        if label == "cyberbullying":
            st.error("**Prediction: Cyberbullying**")
        elif label == "not cyberbullying":
            st.success("**Prediction: Not Cyberbullying**")
        else:
            st.warning("**Prediction: Could not determine**")

        st.subheader("Explanation")
        st.write(explanation)

        st.write("\nWas our classification accurate? (Only share feedback if you are comfortable with sharing your message with us)")
        fb_key = "feedback_image"
        selected = st.feedback("thumbs", key=fb_key)
        if selected is not None:
            prev = st.session_state.feedback_synced.get(fb_key)
            if prev != selected:
                correct = "thumbs up" if selected == 1 else "thumbs down"
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                worksheet.append_row([timestamp, correct, label, extracted_text])
                st.session_state.feedback_synced[fb_key] = selected
                st.toast("Feedback submitted! Thank you!")
