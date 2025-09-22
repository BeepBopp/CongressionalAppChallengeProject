import streamlit as st
import smtplib
import random
import string
import time
import datetime

from email_validator import validate_email, EmailNotValidError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from captcha.image import ImageCaptcha

st.set_page_config(layout="wide", page_title="Contact Us", page_icon="👋")

st.title("👋 Contact Us")
st.markdown("Have questions or comments? Contact us at ai.cybershield@gmail.com or through the contact form below!")

# CAPTCHA options
CAPTCHA_OPTIONS = string.ascii_uppercase + string.digits

def generate_captcha():
    captcha_text = "".join(random.choices(CAPTCHA_OPTIONS, k=6)) 
    image = ImageCaptcha(width=400, height=100).generate(captcha_text)
    return captcha_text, image

# Initialize CAPTCHA in session state
if 'captcha_text' not in st.session_state:
    st.session_state.captcha_text, st.session_state.captcha_image = generate_captcha()

# Initialize form fields in session state
if 'email_value' not in st.session_state:
    st.session_state.email_value = ''
if 'message_value' not in st.session_state:
    st.session_state.message_value = ''

col1, col2, col3, col4 = st.columns([3, 0.25, 1, 0.25]) 

with col3:
    st.markdown('<p style="text-align: justify; font-size: 12px;">CAPTCHAs are active to prevent automated submissions. <br> Thank you for your understanding.</p>', unsafe_allow_html=True)
    
    # Display current CAPTCHA
    st.image(st.session_state.captcha_image, use_column_width=True)

    if st.button("Refresh CAPTCHA", type="secondary", use_container_width=True): 
        st.session_state.captcha_text, st.session_state.captcha_image = generate_captcha()
        st.rerun()

    captcha_input = st.text_input("Enter the CAPTCHA", key="captcha_input")

with col1:
    # Fixed the syntax error by removing the extra =
    email = st.text_input("**Your email***", value=st.session_state.email_value, key='email_input')
    message = st.text_area("**Your message***", value=st.session_state.message_value, key='message_input')

    st.markdown('<p style="font-size: 13px;">*Required fields</p>', unsafe_allow_html=True)

    if st.button("Send", type="primary"):
        if not email or not message:
            st.error("Please fill out all required fields.")
        elif not captcha_input:
            st.error("Please enter the CAPTCHA.")
        else:
            try:
                # Validate email
                valid = validate_email(email, check_deliverability=True)
                validated_email = valid.email

                # Check CAPTCHA
                if captcha_input.upper() == st.session_state.captcha_text:
                    try:
                        # SMTP configuration - you'll need to set your Gmail App Password here
                        smtp_server = "smtp.gmail.com"
                        smtp_port = 587
                        smtp_username = "ai.cybershield@gmail.com"
                        smtp_password = "your_gmail_app_password_here"  # Replace with your actual App Password
                        recipient_email = "ai.cybershield@gmail.com"

                        # Create SMTP connection
                        with smtplib.SMTP(smtp_server, smtp_port) as server:
                            server.starttls()
                            server.login(smtp_username, smtp_password)

                            # Send notification email to you
                            subject = "Contact Form Submission"
                            body = f"New contact form submission:\n\nEmail: {validated_email}\nMessage: {message}"
                            msg = MIMEMultipart()
                            msg['From'] = smtp_username
                            msg['To'] = recipient_email
                            msg['Subject'] = subject
                            msg.attach(MIMEText(body, 'plain'))
                            server.sendmail(smtp_username, recipient_email, msg.as_string())

                            # Send confirmation email to user
                            current_datetime = datetime.datetime.now()
                            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                            confirmation_subject = f"Confirmation of Contact Form Submission ({formatted_datetime})"
                            confirmation_body = f"Thank you for contacting us! Your message has been received and we'll respond within a couple of business days.\n\nYour message:\n{message}"
                            confirmation_msg = MIMEMultipart()
                            confirmation_msg['From'] = smtp_username
                            confirmation_msg['To'] = validated_email
                            confirmation_msg['Subject'] = confirmation_subject
                            confirmation_msg.attach(MIMEText(confirmation_body, 'plain'))
                            server.sendmail(smtp_username, validated_email, confirmation_msg.as_string())

                        st.success("Message sent successfully! We'll respond within a couple of business days.")
                        
                        # Generate new CAPTCHA
                        st.session_state.captcha_text, st.session_state.captcha_image = generate_captcha()
                        
                        # Clear form fields
                        st.session_state.email_value = ''
                        st.session_state.message_value = ''
                        
                        # Wait a moment then rerun to refresh the page
                        time.sleep(2)
                        st.rerun()

                    except smtplib.SMTPAuthenticationError:
                        st.error("Authentication failed. Please check your email credentials.")
                    except smtplib.SMTPException as e:
                        st.error(f"Failed to send email. Please try again later. Error: {str(e)}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {str(e)}")
                
                else:
                    st.error("CAPTCHA text does not match. Please try again.") 

            except EmailNotValidError as e:
                st.error(f"Invalid email address: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred while validating the email: {str(e)}")
