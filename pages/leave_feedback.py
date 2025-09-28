import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor

st.title("💬 Leave Feedback")

db = st.secrets["postgres"]

def get_connection():
    return psycopg2.connect(
        host=db["host"],
        port=db["port"],
        dbname=db["dbname"],
        user=db["user"],
        password=db["password"],
        sslmode="require", 
        cursor_factory=RealDictCursor
    )

with st.form("feedback_form"):
    email = st.text_input("Email Address")
    feedback = st.text_area("Your Feedback")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not email or not feedback:
            st.error("Please fill in both fields before submitting!")
        else:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS feedback (id SERIAL PRIMARY KEY, email TEXT, feedback TEXT)"
                )
                cur.execute(
                    "INSERT INTO feedback (email, feedback) VALUES (%s, %s)",
                    (email, feedback),
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success("Thanks! Your feedback is submitted!")
            except Exception as e:
                st.error("Could not submit feedback. Please try again!")
                st.exception(e)

import streamlit as st
import pandas as pd
import os

st.title("Leave Feedback 💬")
with st.form("user_input_form"):
    email = st.text_input("Email Address")
    feedback = st.text_area("Your Feedback")
    submitted = st.form_submit_button("Submit")
csv_file_path = "user_answers.csv"
data = pd.DataFrame(columns=["Email", "Feedback"])
if os.path.exists(csv_file_path):
    data = pd.read_csv(csv_file_path)
if submit_button:
    data.to_csv(csv_file_path, index=False)
    st.success("Thank you! Your feedback is submitted.")

    except Exception as e:
                st.error("Could not submit feedback. Please try again!")
                st.exception(e)
st.write("Current data:")
st.write(data)
st.download_button(
        label="Download CSV File",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name="user_answers.csv",
        mime="text/csv",
    )
