import streamlit as st

pages = {
  "Tools": [
    st.Page("cyberbullying_detector.py", title="Cyberbullying Detector", icon="🚨")
    # Support Therapist
    # Victim Recommendations
    # Moderator Recommendations
  ],
  "Resources": [
    # Resources for Victims
    # Resources for Teachers / Moderators
    # Resources for Parents
    # etc.
  ],
  "Reach Out": [
    # About Us
    # Leave Feedback
    # Contact Us
  ],
}

pg = st.navigation(pages)
st.set_page_config(page_title="CyberShield", page_icon="🛡️")
pg.run()
