import streamlit as st
import smtplib
import datetime

from email_validator import validate_email, EmailNotValidError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.title("👋 Contact Us")
st.markdown("Contact us at ai.cybershield@gmail.com or through the contact form below!")

if 'email_value' not in st.session_state:
    st.session_state.email_value = ''
if 'message_value' not in st.session_state:
    st.session_state.message_value = ''

with st.form("contact_us_form"):
    st.session_state.email_value = st.text_input("**Your email***", value=st.session_state.email_value, key='email_input')
    st.session_state.message_value = st.text_area("**Your message***", value=st.session_state.message_value, key='message_input')

    email = st.session_state.email_value
    message = st.session_state.message_value

    st.markdown('<p style="font-size: 13px;">*Required fields</p>', unsafe_allow_html=True)

    if st.form_submit_button("Send"):
        if not email or not message:
            st.error("Please fill out all required fields.")
        else:
            try:
                valid = validate_email(email, check_deliverability=False)
                validated_email = valid.email

                smtp_server = "smtp.gmail.com"
                smtp_port = 587
                smtp_username = "ai.cybershield@gmail.com"
                smtp_password = st.secrets["SMTP_PASSWORD"]
                recipient_email = "ai.cybershield@gmail.com"

                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_username, smtp_password)

                    subject = "Contact Form Submission"
                    body = f"New contact form submission:\n\nEmail: {validated_email}\nMessage: {message}"
                    msg = MIMEMultipart()
                    msg['From'] = smtp_username
                    msg['To'] = recipient_email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(body, 'plain'))
                    server.sendmail(smtp_username, recipient_email, msg.as_string())

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

                st.session_state.email_value = ''
                st.session_state.message_value = ''

                st.rerun()

            except EmailNotValidError as e:
                st.error(f"Invalid email address: {str(e)}")
            except smtplib.SMTPAuthenticationError:
                st.error("Authentication failed. Please check your email credentials.")
            except smtplib.SMTPException as e:
                st.error(f"Failed to send email. Please try again later. Error: {str(e)}")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
