import PyPDF2
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Create FAISS index from reports
def create_faiss_index(reports):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(reports).toarray()
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)  # Using L2 distance
    faiss_index = faiss.IndexIDMap2(index)
    faiss_index.add_with_ids(np.array(vectors), np.arange(len(reports)))
    return faiss_index, vectorizer

# Handle the query by retrieving relevant information
def handle_user_query(query, reports, index, vectorizer):
    query_vec = vectorizer.transform([query]).toarray()
    _, I = index.search(query_vec, 1)  # Retrieve the most similar document
    return reports[I[0][0]]  # Return the most similar document's content
