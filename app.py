import streamlit as st

pages = {
  "Welcome": [
    st.Page("home_page.py", title="Home", icon="🛡️"),
    # How to use this app
  ],
  "Tools": [
    st.Page("cyberbullying_detector.py", title="Cyberbullying Detector", icon="🚨"),
    # Support Therapist
    st.Page("victim_rec.py", title="Recommendations", icon="💡"),
    # Moderator Recommendations
  ],
  "Resources": [
    st.Page("youth_resources.py", title="Youth Resources", icon="🫂"),
    st.Page("parent_resources.py", title="Parent Resources", icon="👪"),
    st.Page("mod_resources.py", title="Moderator Resources", icon="🤝"),
  ],
  "Reach Out": [
    st.Page("about_us.py", title="About Us", icon="💼"),
    st.Page("leave_feedback.py", title="Leave Feedback", icon="💬"),
  ],
}

pg = st.navigation(pages)
st.set_page_config(page_title="Cybershield", page_icon="🛡️")
pg.run()
