import streamlit as st

pages = {
  "Welcome": [
    st.Page("pages/home_page.py", title="Home", icon="🛡️"),
  ],
  "Tools": [
    st.Page("pages/cyberbullying_detector.py", title="Cyberbullying Detector", icon="🚨"),
    st.Page("pages/therapist.py", title="Support", icon="❤️"),
    st.Page("pages/recommendations.py", title="Recommendations", icon="💡"), 
    st.Page("pages/moderators.py", title="Moderators", icon="🔨"), # combine with victim
  ],
  "Resources": [
    st.Page("pages/youth_resources.py", title="Youth Resources", icon="🫂"),
    st.Page("pages/parent_resources.py", title="Parent Resources", icon="👪"),
    st.Page("pages/mod_resources.py", title="Moderator Resources", icon="🤝"),
  ],
  "Reach Out": [
    st.Page("pages/about_us.py", title="About Us", icon="💼"),
    st.Page("pages/leave_feedback.py", title="Leave Feedback", icon="💬"),
    st.Page("pages/contact_us.py", title="Contact Us", icon="👋"),
  ],
}

pg = st.navigation(pages)
st.set_page_config(page_title="Cybershield", page_icon="🛡️")
pg.run()
