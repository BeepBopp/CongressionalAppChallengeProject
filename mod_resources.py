import streamlit as st

st.set_page_config(
    page_title="Resources for Moderators",
    page_icon="🤝",
    layout="centered"
)

st.title("🤝 Resources for Moderators")

st.markdown("""
### Supporting Safe and Respectful Online Communities

As a moderator, you play a vital role in protecting users—especially youth—from cyberbullying and harmful content. This page offers guidance, resources, and tools to help you moderate effectively and compassionately.
""")

st.header("🛠️ Key Responsibilities")
st.markdown("""
- **Monitor user content** for harassment, hate speech, and bullying behavior.  
- **Respond quickly** to reports or signs of cyberbullying.  
- **Enforce community guidelines** consistently and fairly.  
- **Support vulnerable users** by providing resources or escalation paths.  
- **Collaborate with platform teams** for serious incidents or repeat offenders.
""")

st.header("🚩 Common Moderator Scenarios")
with st.expander("Scenario 1: Identifying subtle or coded bullying"):
    st.markdown("""
    - Watch for repeated negative comments or exclusion tactics.  
    - Use keyword filters but be aware of slang or variations.  
    - Consider context and intent before acting.
    """)

with st.expander("Scenario 2: Handling false reports"):
    st.markdown("""
    - Investigate the context fully before removing content or sanctioning users.  
    - Communicate transparently with involved parties.  
    - Educate users on appropriate reporting behavior.
    """)

with st.expander("Scenario 3: Supporting a user who reports bullying"):
    st.markdown("""
    - Acknowledge their report and thank them for helping keep the community safe.  
    - Provide resources or links to support services.  
    - If needed, escalate serious cases to platform safety teams or legal authorities.
    """)

st.header("🌐 Trusted Moderator Resources")
st.markdown("""
- [**Community Moderation Guide - Mozilla**](https://mozilla.github.io/network-pulse/community-moderation-guide/)  
  Practical advice on creating welcoming online spaces and handling conflicts.

- [**Center for Humane Technology – Digital Civility**](https://www.humanetech.com/digital-civility)  
  Resources focused on promoting respectful online interactions and reducing toxicity.

- [**The Trust & Safety Professional Association (TSPA)**](https://www.tspa.org/resources)  
  A community and resource hub for moderators and safety professionals worldwide.

- [**Better Internet for Kids – Moderators**](https://www.betterinternetforkids.eu/web/portal/helpline)  
  Tools and best practices to manage reports and protect children online.

- [**Tech & Learning – Online Safety Tools**](https://www.techlearning.com/resources/online-safety-tools)  
  Educational resources and tools for moderators to support safe digital environments.
""")

st.header("🧰 Moderator Tools in This App")
col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Detect Harmful Language"):
        st.switch_page("cyberbullying_detector.py")
with col2:
    if st.button("💡 Recommendations for Victims"):
        st.switch_page("recommendations.py")

st.markdown("""
---

🤝 *Thank you for helping keep online spaces safe, inclusive, and respectful for everyone — especially our youth.*  
""")
