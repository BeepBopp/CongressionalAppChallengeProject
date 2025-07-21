import streamlit as st

st.set_page_config(
    page_title="Resources for Parents",
    page_icon="👪",
    layout="centered"
)

# Page Title
st.title("👪 Resources for Parents")

st.markdown("""
### Helping Your Child Navigate Cyberbullying

Cyberbullying can be hidden, confusing, and painful—for both kids and parents. If you suspect your child is being targeted online, these resources and strategies can help you support them effectively.
""")

# What parents can do
st.header("🛡️ What Can I Do as a Parent?")
st.markdown("""
- **Stay calm and listen** — Let your child open up at their pace. Avoid reacting with anger or punishment.
- **Document everything** — Take screenshots of messages or posts as evidence.
- **Help block and report** the bully on the platform where the abuse happened.
- **Talk to your child’s school** if classmates are involved.
- **Model good digital habits** — Be kind online, respect privacy, and practice empathy.

📌 *Your support can make the biggest difference. Children often suffer silently—being available and calm helps them feel safe.*
""")

# Parent-specific scenarios
st.header("📚 Realistic Scenarios Parents Face")
with st.expander("Scenario 1: Your child becomes withdrawn after using their phone"):
    st.markdown("""
    **What to do:**  
    - Gently ask if something online has upset them  
    - Check their social media together if they're comfortable  
    - Offer support without judgment  
    - Reassure them you're there to help, not punish  
    """)

with st.expander("Scenario 2: Another parent tells you your child might be a victim"):
    st.markdown("""
    **What to do:**  
    - Thank them and talk to your child privately  
    - Ask open-ended questions like, "Has anything online made you feel uncomfortable lately?"  
    - Don’t force the conversation — keep the door open  
    """)

with st.expander("Scenario 3: You find mean comments on your child's public posts"):
    st.markdown("""
    **What to do:**  
    - Take screenshots and save links  
    - Help them report or remove the content  
    - Discuss how it made them feel  
    - Consider reaching out to the school if classmates are involved  
    """)

# Trusted websites for parents
st.header("🌐 Recommended Websites for Parents")
st.markdown("""
- [**StopBullying.gov – For Parents**](https://www.stopbullying.gov/resources/parents)  
  U.S. government advice on signs to watch for, what to do, and how to work with schools and law enforcement.

- [**Common Sense Media**](https://www.commonsensemedia.org/articles/what-is-cyberbullying)  
  Expert reviews and advice for parents on apps, games, and how to help children manage online risks.

- [**ConnectSafely**](https://www.connectsafely.org/)  
  A nonprofit with quick guides for parents on online safety, apps, privacy, and cyberbullying.

- [**National PTA – Cyberbullying**](https://www.pta.org/home/family-resources/safety/cyberbullying)  
  A parent-focused resource on understanding cyberbullying and engaging in proactive conversations.

- [**Bark**](https://www.bark.us/blog/what-is-cyberbullying/)  
  A monitoring tool for families, with a blog that shares tips and signs of digital distress in children.

- [**Family Online Safety Institute**](https://www.fosi.org/)  
  Offers digital parenting tips and policy-focused insight on keeping kids safe online.

- [**The Trevor Project – For Parents**](https://www.thetrevorproject.org/resources/guide/a-guide-to-being-an-ally-to-transgender-and-nonbinary-youth/)  
  Especially helpful if your child is LGBTQ+ and may be facing identity-based cyberbullying.
""")

# Call to explore app features
st.header("🧠 Try Our Tools")
st.markdown("Explore these features to support your child directly:")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Detect Harmful Language"):
        st.switch_page("cyberbullying_detector.py")

with col2:
    if st.button("💡 Get Situation-Based Advice"):
        st.switch_page("victim_rec.py")  

# Closing message
st.markdown("""
---

👪 *Your involvement matters. Being a calm, informed, and compassionate parent is one of the best ways to help your child through tough online experiences.*  
""")
