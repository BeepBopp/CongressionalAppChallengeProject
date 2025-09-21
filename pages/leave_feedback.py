from sqlalchemy import create_engine
import streamlit as st

db_config = st.secrets["postgres"]

engine = create_engine(
    f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
)

with engine.connect() as conn:
    result = conn.execute("SELECT NOW();")
    for row in result:
        st.write(row)
