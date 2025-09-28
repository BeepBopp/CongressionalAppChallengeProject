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
if os.path.exists(csv_file_path):
    data = pd.read_csv(csv_file_path)
if submitted:
    data.to_csv(csv_file_path, index=False)
    st.success("Thank you! Your feedback is submitted.")
st.write("Current data:")
st.write(data)
st.download_button(
        label="Download CSV File",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name="user_answers.csv",
        mime="text/csv",
    )
