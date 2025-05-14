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

# Show the first question (if the product is not yet selected)
if not st.session_state.get("product_selected", False):
    st.write("Welcome! Please tell us which product you are interested in.")
    user_query = st.text_input("Enter your product query (e.g., 'I export Honey')")

    if user_query:
        st.session_state.product_selected = True
        # Send the selected product to backend
        query_data = {"query": user_query}
        response = requests.post("http://localhost:5000/query", json=query_data)
        st.write(f"**Assistant:** {response.json().get('question')}")
else:
    user_query = st.text_input("Enter your query (e.g., 'buyer countries' or 'export trends')")

    if user_query:
        # Send the user query to backend
        query_data = {"query": user_query}
        response = requests.post("http://localhost:5000/query", json=query_data)
        
        if response.status_code == 200:
            assistant_response = response.json()
            st.write(f"**Assistant:** {assistant_response.get('answer')}")
            st.write(f"**Assistant Next:** {assistant_response.get('next_question')}")
        else:
            st.write("Sorry, couldn't process your query. Please try again later.")
