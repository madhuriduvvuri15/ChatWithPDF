import streamlit as st # type: ignore
from fileingestor import FileIngestor # type: ignore

# Set the title for the Streamlit app
st.title("Chat with PDF - 🦙 🔗")
st.text('Hello')

# Create a file uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload File", type="pdf")

if uploaded_file:
    file_ingestor = FileIngestor(uploaded_file)
    file_ingestor.handlefileandingest()