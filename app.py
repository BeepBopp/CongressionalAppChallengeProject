import streamlit as st

pages = {
  "Welcome": [
    st.Page("welcome_pages/home_page.py", title="Home", icon="🛡️"),
  ],
  "Tools": [
    st.Page("tools_pages/cyberbullying_detector.py", title="Cyberbullying Detector", icon="🚨"),
    # Support Therapist
    st.Page("tools_pages/recommendations.py", title="Recommendations", icon="💡"), # Add moderator recommendations
  ],
  "Resources": [
    st.Page("resource_pages/youth_resources.py", title="Youth Resources", icon="🫂"),
    st.Page("resource_pages/parent_resources.py", title="Parent Resources", icon="👪"),
    st.Page("resource_pages/mod_resources.py", title="Moderator Resources", icon="🤝"),
  ],
  "Reach Out": [
    st.Page("reach_out_pages/about_us.py", title="About Us", icon="💼"),
    st.Page("reach_out_pages/leave_feedback.py", title="Leave Feedback", icon="💬"),
    st.Page("reach_out_pages/contact_us.py", title="Contact Us", icon="👋"),
  ],
}

pg = st.navigation(pages)
st.set_page_config(page_title="Cybershield", page_icon="🛡️")
pg.run()
