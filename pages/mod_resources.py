import streamlit as st

st.set_page_config(
    page_title="Resources for Moderators",
    page_icon="🤝",
    layout="centered"
)

st.title("🤝 Resources for Moderators")
st.markdown("""
### Supporting Safe and Respectful Online Communities
As a moderator, you play an extremely important role to protect users from cyberbullying and harmful content. This page offers guidance, resources, and tools to help you moderate effectively and respectively.
""")

st.header("🛠️ Key Responsibilities")
st.markdown("""
- Monitor messages and conversations for bullying or hate speech.
- Immediately respond to signs or reports of cyberbullying. 
- Create clear community guidelines and enfore them appropriately.
- Offer suppot and resources to those targeted by cyberbullying.
- Utilize tools and support made available by the platform to combat cyberbullying.
""")

st.header("🚩 Example Scenarios")
with st.expander("Scenario 1: Identifying subtle cyberbullying"):
    st.markdown("""
    **What you can do:**  
    - Keep an eye out for a pattern of negative comments.
    - Use a keyword search functionality (stay aware of slang or abbreviations)
    - Make sure to understand the context and intent of the situation.
    """)

with st.expander("Scenario 2: Handling false reports"):
    st.markdown("""
    **What you can do:**  
    - Investigate the context fully before removing content or sanctioning users.  
    - Discuss the matter with all parties involved.
    - Keep users aware on how and when to report.
    """)

with st.expander("Scenario 3: Supporting a user who reports bullying"):
    st.markdown("""
    **What you can do:**  
    - Acknowledge their report and thank them for helping keep the community safe.  
    - Offer support and resources to those affected.
    - If needed, escalate serious cases to platform safety teams or legal authorities.
    """)

st.header("🌐 Trusted Resources")
st.markdown("""
- [**Mozilla Community Participation Guidelines**](https://www.mozilla.org/en-US/about/governance/policies/participation/)  
  Mozilla's guidelines for welcoming online spaces and handling conflicts.
- [**Center for Humane Technology**](https://www.humanetech.com/)  
  Resources focused on respectful online interactions and reducing the negative effects of social media and relevant technology.
- [**The Trust & Safety Professional Association (TSPA)**](https://www.tspa.org/curriculum/ts-curriculum/)  
  A resource hub for moderators and safety professionals.
- [**Better Internet for Kids – Moderators**](https://www.betterinternetforkids.eu/web/portal/helpline)  
  Tools and best practices to manage reports and protect children online.
- [**Mozilla Content Moderation Practices**](https://www.mozilla.org/en-US/about/legal/content-moderation/)  
  Mozilla's approach to content moderation and policy enforcement.
""")

st.header("🧰 Try other toools")
col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Detect Harmful Language"):
        st.switch_page("pages/cyberbullying_detector.py")  
with col2:
    if st.button("💡 Get Situation-Based Advice"):
        st.switch_page("pages/moderators.py")

st.markdown("""
---
🤝 *Thank you for helping keep online spaces safe and respectful!*  
""")
