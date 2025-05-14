from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import extract_text_from_pdf, create_faiss_index, handle_user_query, get_top_buyers, get_export_trends

app = Flask(__name__)
CORS(app)

# Initialize global variables
reports = []
index = None
vectorizer = None
conversation_context = {}

@app.route("/upload", methods=["POST"])
def upload_file():
    print("Upload route hit")
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
    print("Query route hit")
    data = request.json
    user_query = data.get("query")
    
    if not user_query:
        return jsonify({"error": "Query missing"}), 400

    # Check if the query matches a known step
    if "product" not in conversation_context:
        conversation_context["product"] = user_query
        return jsonify({
            "question": "Great! Now, are you looking for buyer countries or export trends for this product?",
            "next_step": "buyer_or_trends"
        })
    
    if "next_step" not in conversation_context:
        conversation_context["next_step"] = user_query
        if user_query.lower() in ["buyer countries", "buyers"]:
            return jsonify({
                "answer": get_top_buyers(conversation_context["product"]),
                "next_question": "Would you like more details or trends?"
            })
        elif user_query.lower() in ["export trends", "trends"]:
            return jsonify({
                "answer": get_export_trends(conversation_context["product"]),
                "next_question": "Would you like more details or top buyer countries?"
            })
        else:
            return jsonify({
                "answer": "Sorry, I didn't quite understand. Please choose 'buyer countries' or 'export trends'.",
                "next_question": "Please choose one: buyer countries or export trends?"
            })
    
    # Process queries dynamically based on steps
    response = handle_user_query(user_query, reports, index, vectorizer)
    return jsonify({"answer": response})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
