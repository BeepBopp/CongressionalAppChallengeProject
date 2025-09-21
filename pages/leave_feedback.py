import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor

st.title("💬 Leave Feedback")

# Load database connection settings from secrets
db = st.secrets["postgres"]

# Try to connect
def get_connection():
    return psycopg2.connect(
        host=db["host"],
        port=db["port"],
        dbname=db["dbname"],
        user=db["user"],
        password=db["password"],
        sslmode="require",  # Supabase requires SSL
        cursor_factory=RealDictCursor
    )

# Feedback form
with st.form("feedback_form"):
    name = st.text_input("Your Name")
    feedback = st.text_area("Your Feedback")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not name or not feedback:
            st.error("⚠️ Please fill in both fields before submitting.")
        else:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS feedback (id SERIAL PRIMARY KEY, name TEXT, feedback TEXT)"
                )
                cur.execute(
                    "INSERT INTO feedback (name, feedback) VALUES (%s, %s)",
                    (name, feedback),
                )
                conn.commit()
                cur.close()
                conn.close()
                st.success("✅ Thank you! Your feedback has been submitted.")
            except Exception as e:
                st.error("❌ Could not submit feedback.")
                st.exception(e)

# Display feedback entries
st.subheader("📋 Previous Feedback")
try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, feedback FROM feedback ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if rows:
        for row in rows:
            st.markdown(f"**{row['name']}**: {row['feedback']}")
    else:
        st.info("No feedback yet.")
except Exception as e:
    st.error("⚠️ Could not load feedback entries.")
    st.exception(e)
