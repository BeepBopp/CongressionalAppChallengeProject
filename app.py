import streamlit as st
cyberbullying_detector = st.Page("Cyberbullying_Detector.py", title="Cyberbullying Detector", icon="🚨")

pg = st.navigation([cyberbullying_detector])
st.set_page_config(page_title="CyberShield", page_icon="🛡️")
pg.run()
