import streamlit as st
import smtplib
import random
import os
import time
import datetime

from email_validator import validate_email, EmailNotValidError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from captcha.image import ImageCaptcha
from io import BytesIO
from PIL import Image
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(layout="wide")

st.title("👋 Contact Us")
st.markdown("Have questions or comments? Contact us at ai.cybershield@gmail.com or through the contact form below!")

options = os.getenv("OPTIONS")
server = os.getenv("SERVER")
port = os.getenv("PORT")
u = os.getenv("U")
secret = os.getenv("SECRET")
recipient = os.getenv("RECIPIENT")

def generate_captcha():
    captcha_text = "".join(random.choices(options, k=6)) 
    image = ImageCaptcha(width=400, height=100).generate(captcha_text)
    return captcha_text, image

if 'captcha_text' not in st.session_state:
    st.session_state.captcha_text = generate_captcha()

captcha_text, captcha_image = st.session_state.captcha_text

col1, col2, col3, col4 =  st.columns([3, 0.25, 1, 0.25]) 
captcha_input = None 

with col3:
    st.markdown('<p style="text-align: justify; font-size: 12px;">CAPTCHAs are active to prevent automated submissions. <br> Thank you for your understanding.</p>', unsafe_allow_html=True)
    captcha_placeholder = st.empty()
    captcha_placeholder.image(captcha_image, use_column_width=True)

    if st.button("Refresh", type="secondary", use_container_width=True): 
        st.session_state.captcha_text = generate_captcha()
        captcha_text, captcha_image = st.session_state.captcha_text
        captcha_placeholder.image(captcha_image, use_column_width=True)

    captcha_input = st.text_input("Enter the CAPTCHA")

with col1:
    email = st.text_input("**Your email***", value=st.session_state.get('email', ''), key='email')=
    message = st.text_area("**Your message***", value=st.session_state.get('message', ''), key='message')

    st.markdown('<p style="font-size: 13px;">*Required fields</p>', unsafe_allow_html=True)

    if st.button("Send", type="primary"):
        if not email or not message:
            st.error("Please fill out all required fields.") # error for any blank field
        else:
            try:
                valid = validate_email(email, check_deliverability=True)

                if captcha_input.upper() == captcha_text:
                    
                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587
                    smtp_username = ai.cybershield@gmail.com
                    smtp_password = cybershield123
                    recipient_email = ai@cybershield@gmail.com

                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    server.login(smtp_username, smtp_password)

                    subject = "Contact Form Submission" 
                    body = f"Email: {email}\nMessage: {message}"
                    msg = MIMEMultipart()
                    msg['From'] = smtp_username
                    msg['To'] = recipient_email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))
                    server.sendmail(smtp_username, recipient_email, msg.as_string())

                    current_datetime = datetime.datetime.now()
                    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    confirmation_subject = f"Confirmation of Contact Form Submission ({formatted_datetime})"
                    confirmation_body = f"Thank you for contacting us! Your message has been received.\n\nYour message: {message}"
                    confirmation_msg = MIMEMultipart()
                    confirmation_msg['From'] = smtp_username
                    confirmation_msg['To'] = email  # Use the sender's email address here
                    confirmation_msg['Subject'] = confirmation_subject
                    confirmation_msg.attach(MIMEText(confirmation_body, 'plain'))
                    server.sendmail(smtp_username, email, confirmation_msg.as_string())

                    server.quit()

                    st.success("Sent successfully! We'll reach out in a couple of business days.") 
                
                    st.session_state.captcha_text = generate_captcha()
                    captcha_text, captcha_image = st.session_state.captcha_text

                    captcha_placeholder.image(captcha_image, use_column_width=True)

                    time.sleep(3)
                    streamlit_js_eval(js_expressions="parent.window.location.reload()")

                else:
                    st.error("Text does not match the CAPTCHA.") 

            except EmailNotValidError as e:
                st.error(f"Invalid email address. {e}") 
