import streamlit as st

pages = {
  "Welcome": [
    st.Page("home_page.py", title="Home", icon="🛡️"),
    # How to use this app
  ],
  "Tools": [
    st.Page("cyberbullying_detector.py", title="Cyberbullying Detector", icon="🚨")
    # Support Therapist
    # Victim Recommendations
    # Moderator Recommendations
  ],
  "Resources": [
    st.Page("youth_resources.py", title="Youth Resources", icon="🫂")
    st.Page("parent_resources.py", title="Parent Resources", icon="👪")
    st.Page("mod_resources.py", title="Moderator Resources", icon="🤝")
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
