import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Youth Cyberbullying Resources",
    page_icon="🫂",
    layout="centered"
)

# Title and introduction
st.title("🫂 Resources for Youth")
st.markdown("""
### You're Not Alone

If you're facing online bullying, we're here for you. This page offers trusted advice, examples, and helpful tools to support you.
""")

# What to do section
st.header("🚨 What To Do If You're Being Cyberbullied")
st.markdown("""
- **Don't respond** to the bully. It can escalate things.
- **Take screenshots** of the messages or posts as evidence.
- **Block or mute** the person on the platform.
- **Report** the behavior to the platform or trusted adults.
- **Talk to someone** you trust — a parent, teacher, or counselor.

🧠 *Remember: It's not your fault. You deserve to feel safe online.*
""")

# Example scenarios
st.header("🎭 Example Scenarios and How to Handle Them")
with st.expander("Scenario 1: Getting mean messages in a group chat"):
    st.markdown("""
    **What you can do:**  
    - Leave the group chat if possible  
    - Block the sender(s)  
    - Save the messages and talk to an adult  
    - Report the group to the app/platform  
    """)

with st.expander("Scenario 2: Someone made a fake profile of you"):
    st.markdown("""
    **What you can do:**  
    - Report the profile to the app  
    - Ask friends to report it too  
    - Collect screenshots as proof  
    - Tell a trusted adult or guardian  
    """)

with st.expander("Scenario 3: A classmate is spreading rumors online"):
    st.markdown("""
    **What you can do:**  
    - Don't engage with them publicly  
    - Report the content  
    - Ask a school counselor or parent for help  
    """)

# Helpful websites with descriptions
st.header("🌐 Helpful Websites")
st.markdown("""
Here are some trusted websites that offer support, tools, and advice for dealing with cyberbullying:

- [**StopBullying.gov**](https://www.stopbullying.gov/)  
  A U.S. government site with clear advice for kids, teens, and parents on how to recognize, stop, and prevent bullying.

- [**Stomp Out Bullying**](https://www.stompoutbullying.org/)  
  A national nonprofit that focuses on reducing and preventing bullying, cyberbullying, and digital abuse. They also have a **HelpChat Line** for teens.

- [**Cyberbullying Research Center**](https://cyberbullying.org/)  
  Offers real stories, facts, and tips based on research from experts in teen online safety.

- [**PACER's National Bullying Prevention Center**](https://www.pacer.org/bullying/)  
  Created by a nonprofit that helps kids with disabilities, this site has videos, stories, and kid-friendly tools to speak up against bullying.

- [**Child Mind Institute**](https://childmind.org/topics/concerns/bullying/)  
  Offers mental health guidance for kids and families, including how to deal with the emotional effects of cyberbullying.

- [**Common Sense Media**](https://www.commonsensemedia.org/articles/what-is-cyberbullying)  
  Helps kids and families make smart choices about media and tech — including how to stay safe from cyberbullying online.

- [**Kids Helpline (AU)**](https://kidshelpline.com.au/)  
  A 24/7 free and private counseling service for young people. While based in Australia, many resources apply globally.

- [**The Trevor Project**](https://www.thetrevorproject.org/)  
  A support and crisis hotline focused on LGBTQ+ youth — if bullying is related to identity, this is a safe and affirming place to turn.
""")

# Suggest using other tools
st.header("🛠️ Try Other Tools")
st.markdown("You can get support through these tools we've made:")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔍 Detect Cyberbullying"):
        st.switch_page("pages/cyberbullying_detector.py")

with col2:
    if st.button("❤️ Receive Support"):
        st.switch_page("pages/therapist.py")

with col3:
    if st.button("💡 Get Personalized Help"):
        st.switch_page("pages/recommendations.py")

# Comforting outro
st.markdown("""
---

❤️ *No matter what you're going through, help is always available. You are strong, you are valued, and you are not alone.*  
""")
