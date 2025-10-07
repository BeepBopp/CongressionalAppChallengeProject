import streamlit as st
from datetime import datetime
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
    category = st.text_input("Topic of Concern")
    feedback = st.text_area("Your Feedback")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    submitted = st.form_submit_button("Submit")

if submitted:
    if not category.strip() or not feedback.strip():
        st.warning("Please enter the topic your feedback concerns and your feedback.")
    else:
        worksheet.append_row([timestamp, category, feedback])
        st.success("Thank you! Your feedback was submitted.")

