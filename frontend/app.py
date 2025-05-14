import streamlit as st
import requests

# Streamlit UI setup
st.set_page_config(page_title="Export Research Assistant", layout="wide")
st.title("Export Research Assistant")

# Sidebar for file upload and user input
st.sidebar.header("Upload Export Report")
uploaded_file = st.sidebar.file_uploader("Upload your market research report (PDF)", type="pdf")

# Allow users to select a product
product = st.sidebar.selectbox("Select the Product", ["Honey", "Turmeric", "Jaggery", "Millet", "Cotton"])

# Handle file upload
if uploaded_file:
    st.sidebar.subheader("Processing your file...")
    files = {'file': uploaded_file}
    try:
        response = requests.post("http://localhost:5000/upload", files=files)
        if response.status_code == 200:
            st.sidebar.success("File uploaded and indexed successfully!")
        else:
            st.sidebar.error(f"Failed to upload file: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Error connecting to backend: {e}")

# Main chat interface for users
st.header("Ask Your Question")
user_query = st.text_input("Enter your query about export data (e.g., 'Which countries import honey?')")

if user_query:
    try:
        # Send the query to backend
        query_data = {"query": user_query}
        response = requests.post("http://localhost:5000/query", json=query_data)
        
        if response.status_code == 200:
            answer = response.json().get("answer")
            st.write(f"**Answer:** {answer}")
        else:
            st.write("Sorry, couldn't process your query. Please try again later.")
    except requests.exceptions.RequestException as e:
        st.write(f"Error connecting to backend: {e}")
