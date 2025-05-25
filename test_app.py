import streamlit as st

# Set page config
st.set_page_config(
    page_title="Test App",
    page_icon="🧪",
    layout="wide"
)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "page1"

# Sidebar navigation
st.sidebar.title("Navigation")

if st.sidebar.button("Page 1"):
    st.session_state.current_page = "page1"
    st.experimental_rerun()

if st.sidebar.button("Page 2"):
    st.session_state.current_page = "page2"
    st.experimental_rerun()

# Define page functions
def render_page1():
    st.title("Page 1")
    st.write("This is the first page.")

def render_page2():
    st.title("Page 2")
    st.write("This is the second page.")

# Main content
if st.session_state.current_page == "page1":
    render_page1()
elif st.session_state.current_page == "page2":
    render_page2() 