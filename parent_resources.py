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

st.header("📚 Typical Parent Scenarios")
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
- **StopBullying.gov – Get Help Now**  
  Official U.S. government guidance for parents, including documentation tips and escalation steps, with mental health and school‑reporting support :contentReference[oaicite:1]{index=1}

- **National Cybersecurity Alliance – Parents & Educators**  
  Offers clear advice on how to block, report, and avoid escalation, plus guidance on legal or school intervention :contentReference[oaicite:2]{index=2}

- **National Children’s Alliance – Cyberbullying Resources**  
  Tip sheets and videos specifically for parents on spotting signs, talking safely, and addressing sextortion or online abuse :contentReference[oaicite:3]{index=3}

- **HEARD Alliance – Resources for Families**  
  Focuses on understanding cyberbullying dynamics and offers curated links and family support tools :contentReference[oaicite:4]{index=4}

- **Cybersmile – Who to Call**  
  A global list of free helplines including US and international support for bullying and digital abuse :contentReference[oaicite:5]{index=5}

- **Echo Movement – Bullying Support Resources**  
  Aggregates national hotlines and support services, including chat, text, and legal help resources :contentReference[oaicite:6]{index=6}
""")

st.header("🧠 Try Our App Tools")
st.markdown("These tools can help your child directly and give guidance tailored to your situation:")

col1, col2 = st.columns(2)
with col1:
    if st.button("🔍 Detect Harmful Language"):
        st.switch_page("cyberbullying_detector.py")

with col2:
    if st.button("💡 Get Situation-Based Advice"):
        st.switch_page("recommendations.py")

st.markdown("""
---

👪 *Your calm presence and informed guidance are powerful to your child. You’re not alone, and help is available every step of the way.*  
""")
