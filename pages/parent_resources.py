import streamlit as st

st.set_page_config(
    page_title="Resources for Parents",
    page_icon="👪",
    layout="centered"
)

st.title("👪 Resources for Parents")

st.markdown("""
### Helping Your Child Navigate Cyberbullying

Cyberbullying can be confusing and emotionally painful—for both kids and their parents. If you suspect your child is facing online bullying, these strategies and resources can help guide you through steps to support them wisely.
""")

st.header("🛡️ What Can Parents Do?")
st.markdown("""
- **Listen and validate** — Give your child space to share at their own pace and avoid jumping to conclusions.
- **Document clearly** — Save screenshots and context (time/date/platform).
- **Block and report** together — If they’re comfortable, assist in blocking users and filing reports.
- **Partner with school or community** — Engage trusted adults or institutions where bullying may be occurring.
- **Model healthy digital behavior** — Teach empathy and respectful online habits.
""")

st.header("📚 Example Scenarios")
with st.expander("Scenario 1: You sense your child is hiding their phone"):
    st.markdown("""
    - Gently ask open questions like, “Is something online worrying you?”
    - Offer to look together only if they agree.
    - Reassure them the goal is support, not punishment.
    """)

with st.expander("Scenario 2: Another parent reports that your child’s peer is targeting your child"):
    st.markdown("""
    - Thank them for sharing and follow up privately with your child.
    - Pose neutral questions like, “Has anyone online been unkind recently?”
    - Keep the dialogue open—don’t pressure.
    """)

with st.expander("Scenario 3: You see hurtful comments on your child’s posts"):
    st.markdown("""
    - Take screenshots immediately.
    - Help your child report or hide the content.
    - Discuss how they feel and whether to involve their school.
    """)

st.header("🌐 Trusted Resources for Parents")
st.markdown("""
Here are reliable websites designed to help parents support their children through cyberbullying situations:

- [**StopBullying.gov – Get Help Now**](https://www.stopbullying.gov/resources/get-help-now)  
  Official U.S. government guidance for recognizing, preventing, and responding to cyberbullying, including how to involve schools and authorities.

- [**National Cybersecurity Alliance – Parents & Educators**](https://staysafeonline.org/online-safety-privacy-basics/cyberbullying-parents/)  
  Offers step-by-step advice for talking to kids, setting boundaries, and handling digital conflict safely.

- [**National Children’s Alliance – Cyberbullying Resources**](https://www.nationalchildrensalliance.org/cyberbullying/)  
  Focused on trauma-informed guidance, this resource includes educational tools for caregivers and how to respond to serious cases like sextortion.

- [**HEARD Alliance – Family Resources**](https://www.heardalliance.org/families-cyber-bullying/)  
  Mental health–focused tips and support on how cyberbullying affects emotional wellbeing and how families can help.

- [**Cybersmile – Who to Call**](https://www.cybersmile.org/advice-help/category/who-to-call)  
  A global nonprofit with hotlines and reporting options categorized by country, perfect for urgent support.

- [**Echo Movement – Family Support Hub**](https://echomovement.org/resources/)  
  Lists anti-bullying organizations, school guides, and national help services for both digital and real-world bullying.
""")

st.header("🧠 Tools in this App")
st.markdown("These tools can help your child directly and give guidance tailored to your situation:")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔍 Detect Harmful Language"):
        st.switch_page("pages/cyberbullying_detector.py")

with col2:
    if st.button("❤️ Receive Support"):
        st.switch_page("pages/therapist.py")

with col3:
    if st.button("💡 Get Advice"):
        st.switch_page("pages/recommendations.py")

st.markdown("""
---

👪 *Your calm presence and informed guidance are powerful to your child. You’re not alone, and help is available every step of the way.*  
""")
