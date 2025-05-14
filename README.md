# Export Research Assistant

The **Export Research Assistant** is a powerful AI-driven tool that helps exporters gather actionable insights from market research reports and datasets related to international trade. It allows users to upload reports, query for specific export-related information, and get answers based on data extracted from the reports and other trade datasets.

## Features
- **Upload Market Research Reports**: Upload PDF reports related to exports and have them processed for querying.
- **Export Queries**: Ask specific questions about export data, such as top buyer countries, product trends, tariffs, etc.
- **Interactive Chat Interface**: Use a conversational interface to interact with the assistant and get instant answers.
- **Recommendation Engine**: Get export recommendations, like the top countries for your product or the best regions to target.
  
## Tech Stack
- **Backend**: Python, Flask, FAISS (for document indexing), LangChain or LlamaIndex (for LLM integration).
- **Frontend**: React (for the main UI) or Streamlit (for quick deployment).
- **Data Sources**:
  - **Terra Sourcing Market Reports** (PDF, CSV, DOC).
  - **ITC Trade Map**, **DGFT**, **APEDA** for trade data.
  - Open APIs like **Google Trends**, **ImportYeti**, **Alibaba** for export trends and buyer data.

---

## **Getting Started**

### **Prerequisites**
- Python 3.x
- Node.js and npm (for frontend)
- Required Python libraries:
  - Flask
  - Flask-CORS
  - FAISS or ChromaDB
  - LangChain or LlamaIndex
  - Requests (for communication between frontend and backend)
  - PyMuPDF (for document parsing)

---

### **Setup Instructions**

#### **1. Clone the Repository**
Clone the repository to your local machine.

```bash
git clone https://github.com/yourusername/export-research-assistant.git
cd export-research-assistant
