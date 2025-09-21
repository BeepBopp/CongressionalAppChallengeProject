import psycopg2
import socket
import streamlit as st

db = st.secrets["postgres"]

# Force IPv4
ipv4_host = socket.gethostbyname(db["host"])

try:
    conn = psycopg2.connect(
        host=ipv4_host,  # IPv4 only
        dbname=db["dbname"],
        user=db["user"],
        password=db["password"],
        port=db["port"],
        connect_timeout=10
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    row = cur.fetchone()
    st.success(f"Connected! PostgreSQL version: {row}")
except Exception as e:
    st.error(f"Database connection failed: {e}")
