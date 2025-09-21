from sqlalchemy import create_engine
import streamlit as st

db = st.secrets["postgres"]

engine = create_engine(
    f"postgresql+psycopg2://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['dbname']}"
)

with engine.connect() as conn:
    result = conn.execute("SELECT NOW();")
    for row in result:
        st.write(row)
