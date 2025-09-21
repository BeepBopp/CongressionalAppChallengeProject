import psycopg2
import streamlit as st

db = st.secrets["postgres"]

try:
    conn = psycopg2.connect(
        host=db["host"],
        dbname=db["dbname"],
        user=db["user"],
        password=db["password"],
        port=db["port"],
        connect_timeout=10  # so it fails quickly if blocked
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    row = cur.fetchone()
    st.success(f"Connected! Postgres version: {row}")
except Exception as e:
    st.error(f"Database connection failed: {e}")
