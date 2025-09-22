import streamlit as st
import smtplib
import time
import datetime

from email_validator import validate_email, EmailNotValidError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(layout="wide", page_title="Contact Us", page_icon="👋")

st.title("👋 Contact Us")
st.markdown("Have questions or comments? Contact us at ai.cybershield@gmail.com or through the contact form below!")

# Initialize form fields in session state
if 'email_value' not in st.session_state:
    st.session_state.email_value = ''
if 'message_value' not in st.session_state:
    st.session_state.message_value = ''

col1, col2 = st.columns([4, 1]) 

with col1:
    # Contact form
    email = st.text_input("**Your email***", value=st.session_state.email_value, key='email_input')
    message = st.text_area("**Your message***", value=st.session_state.message_value, key='message_input')

    st.markdown('<p style="font-size: 13px;">*Required fields</p>', unsafe_allow_html=True)

    if st.button("Send", type="primary"):
        if not email or not message:
            st.error("Please fill out all required fields.")
        else:
            try:
                # Check if email is valid
                valid = validate_email(email, check_deliverability=True)
                validated_email = valid.email

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
                
            except EmailNotValidError as e:
                st.error(f"Invalid email address: {str(e)}")
            except Exception as e:
                st.error(f"An error occurred while validating the email: {str(e)}")
