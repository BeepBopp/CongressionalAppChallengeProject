import streamlit as st
import pandas as pd
import os

st.title("Leave Feedback 💬")

with st.form("user_input_form"):
    email = st.text_input("Email Address")
    feedback = st.text_area("Your Feedback")
    submitted = st.form_submit_button("Submit")
    
csv_file_path = "feedback.csv"

data = pd.DataFrame(columns=["Email", "Feedback"])

if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
    data = pd.read_csv(csv_file_path)

if submitted:
    new_entry = pd.DataFrame([[email, feedback]], columns=["Email", "Feedback"])
    data = pd.concat([data, new_entry], ignore_index=True)
    data.to_csv(csv_file_path, index=False)
    st.success("Thank you! Your feedback is submitted.")
