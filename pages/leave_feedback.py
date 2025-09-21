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
