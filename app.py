from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import extract_text_from_pdf, create_faiss_index, handle_user_query

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize global variables
reports = []
index = None
vectorizer = None

@app.route("/upload", methods=["POST"])
def upload_file():
    print("Upload route hit")  # Debugging log
    global reports, index, vectorizer
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"error": "No file uploaded"}), 400
        
        # Extract text from PDF file
        report_text = extract_text_from_pdf(file)
        if not report_text:
            return jsonify({"error": "Failed to extract text from PDF"}), 500
        
        # Create FAISS index from the extracted report text
        reports = [report_text]
        index, vectorizer = create_faiss_index(reports)
        return jsonify({"message": "File uploaded and indexed successfully"}), 200
    except Exception as e:
        print(f"Error uploading file: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/query", methods=["POST"])
def query():
    print("Query route hit")  # Debugging log
    data = request.json
    user_query = data.get("query")
    
    if not user_query:
        return jsonify({"error": "Query missing"}), 400
    
    try:
        response = handle_user_query(user_query, reports, index, vectorizer)
        if not response:
            return jsonify({"answer": "Sorry, I couldn't find an answer to your query."}), 200
        return jsonify({"answer": response}), 200
    except Exception as e:
        print(f"Error handling query: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
