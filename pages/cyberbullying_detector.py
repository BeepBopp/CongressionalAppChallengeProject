import streamlit as st
from openai import OpenAI
from datetime import datetime
import os
import base64
from PIL import Image
import io
import pandas as pd

api_key = st.secrets["OPENAI_API_KEY"]

GPT_MODEL = "gpt-4.1-mini"
VISION_MODEL = "gpt-4.1-mini"

def classify_with_gpt(text):
    """Use ChatGPT to classify text and provide explanation."""
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
    """Encode the image to base64"""
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

def extract_text_from_image(image_file):
    """Use OpenAI's Vision capabilities to extract text from an image"""
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
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
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
                
            if label == "cyberbullying":
                st.error("**Prediction: Cyberbullying**")
            elif label == "not cyberbullying":
                st.success("**Prediction: Not Cyberbullying**")
            else:
                st.warning("**Prediction: Could not determine**")
                
            st.subheader("Explanation")
            st.write(explanation)

            if label == "cyberbullying":
            st.write("\nWould you like to check out our other features to cope with this possible cyberbullying?")
            
            if "page_to_switch" not in st.session_state:
                st.session_state.page_to_switch = None
        
            if st.button("Chat with our AI Therapist to receive help with this situation"):
                st.session_state.page_to_switch = "Cyberbullying Support"
            elif st.button("Generate potential responses and next steps with our AI Recommendations Bot"):
                st.session_state.page_to_switch = "Cyberbullying Recommendations"
            elif st.button("Moderator Assistant"):       
                st.session_state.page_to_switch = "Moderators: Use our AI Moderator Assistant for possible courses of action"
        
            if st.session_state.page_to_switch:
                st.switch_page(st.session_state.page_to_switch)


            # display_feedback_system("text")
        else:
            st.warning("Please enter some text to analyze.")

with tab2:
    st.subheader("📸 Analyze a Screenshot")
    uploaded_file = st.file_uploader("Upload a screenshot containing text to analyze", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, width=400, caption="Uploaded Screenshot")
        
        if st.button("Extract & Analyze"):
            with st.spinner("Processing image..."):
                uploaded_file.seek(0)

                extracted_text = extract_text_from_image(uploaded_file)
                
                if extracted_text:
                    st.subheader("Extracted Text")
                    st.text(extracted_text)
                    
                    st.subheader("Analysis Results")
                    with st.spinner("Analyzing extracted text..."):
                        label, explanation = classify_with_gpt(extracted_text)
                        
                    if label == "cyberbullying":
                        st.error("**Prediction: Cyberbullying**")
                    elif label == "not cyberbullying":
                        st.success("**Prediction: Not Cyberbullying**")
                    else:
                        st.warning("**Prediction: Could not determine**")
                        
                    st.subheader("Explanation")
                    st.write(explanation)

                    # display_feedback_system("image")
                else:
                    st.error("Failed to extract text from the image. Please try a clearer image.")
