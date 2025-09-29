import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.title("Leave Feedback 💬")

scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],  \
    scopes=scope
)
client = gspread.authorize(creds)

SHEET_NAME = "feedback"
worksheet = client.open(SHEET_NAME).sheet1

with st.form("feedback_form"):
    email = st.text_input("Email Address")
    feedback = st.text_area("Your Feedback")
    submitted = st.form_submit_button("Submit")

if submitted:
    if not email.strip() or not feedback.strip():
        st.warning("Please enter your and email and your feedback.")
    else:
        worksheet.append_row([email.strip(), feedback.strip()])
        st.success("Thank you! Your feedback was submitted.")

