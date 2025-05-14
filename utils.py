# utils.py
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Function to extract text from PDF (Placeholder - implement with actual code)
def extract_text_from_pdf(file):
    # Implement actual PDF extraction logic (use PyPDF2, pdfminer, etc.)
    return "Extracted text from the report"

# Function to create FAISS index (Placeholder - use real vectorization and indexing logic)
def create_faiss_index(reports):
    # Example: Convert reports to vectors using TF-IDF or other methods
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(reports).toarray()

    # Create a FAISS index
    index = faiss.IndexFlatL2(vectors.shape[1])  # L2 distance index
    faiss_index = faiss.IndexIDMap(index)
    
    # Add vectors to FAISS index
    faiss_index.add_with_ids(np.array(vectors), np.arange(len(reports)))
    return faiss_index, vectorizer

# Function to handle user query and return relevant info from FAISS index
def handle_user_query(query, reports, index, vectorizer):
    query_vector = vectorizer.transform([query]).toarray()
    distances, indices = index.search(np.array(query_vector), k=1)  # Top 1 result
    
    if indices[0][0] != -1:
        # If a result is found
        return reports[indices[0][0]]
    else:
        return "No relevant information found in the report."

# Function to get top buyers for a specific product (Mock data for now)
def get_top_buyers(product):
    # For now, mock some data
    buyers_data = {
        "Honey": ["Germany", "USA", "Japan", "France", "UK"],
        "Turmeric": ["USA", "China", "Australia", "Canada", "UK"],
        "Jaggery": ["USA", "Canada", "Middle East", "UK", "South Africa"],
        "Millet": ["Germany", "USA", "India", "China", "Canada"],
        "Cotton": ["China", "USA", "India", "Turkey", "Pakistan"]
    }
    return buyers_data.get(product, ["No data available for this product"])

# Function to get export trends for a specific product (Mock data for now)
def get_export_trends(product):
    # For now, mock some trends data
    trends_data = {
        "Honey": "Honey exports have increased by 10% year over year, with Germany being the top importer.",
        "Turmeric": "Turmeric exports have risen sharply, especially to the USA and China.",
        "Jaggery": "Jaggery exports to the Middle East have surged, with a steady demand in North America.",
        "Millet": "Millet exports are growing steadily, especially in Europe and the USA.",
        "Cotton": "Cotton exports remain strong with China as the primary market, followed by the USA and India."
    }
    return trends_data.get(product, "No trends data available for this product")
