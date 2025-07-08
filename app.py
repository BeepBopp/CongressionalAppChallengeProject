import streamlit as st

# Set page configuration first
st.set_page_config(page_title="Jon Tutor", page_icon="📖")

# Define the pages using st.page_link
pages = [
    st.page_link("assignment.py", label="Assignment", icon="✍️"),
    st.page_link("calendar.py", label="Calendar", icon="📆"),
    st.page_link("writing_tips.py", label="Writing Tips", icon="💡"),
]

# Create navigation object
nav = st.navigation(pages)

# Run the selected page
nav.run()
