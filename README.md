# 🚑 AI Emergency Medical Chatbot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](#)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/🦜🔗-LangChain-green)](#)
[![Gemini](https://img.shields.io/badge/Google-Gemini_2.5_Flash-orange)](#)

A sophisticated, context-aware AI medical assistant built with **Streamlit**, **LangChain**, and **Google Gemini 2.5 Flash**.

This application serves as a comprehensive health companion capable of parsing personal medical documents, analyzing medical images through OCR, answering general health queries, and—most importantly—triggering a life-saving **Emergency Protocol**.

---

## ✨ Features

### 🧠 Intelligent Multi-Agent Architecture
The system utilizes a custom Router Agent to dynamically classify user intent and direct conversations to the appropriate specialized backend agent:

*   **🚨 Emergency Agent**: Activated when the user reports feeling unwell or requests immediate assistance.
    *   **Live Geolocation**: Captures the user's precise GPS location directly from the browser instance.
    *   **Reverse Geocoding**: Converts raw GPS coordinates into a structured street address using the open-source **Nominatim API**.
    *   **Hospital Locator**: Scans a 5-kilometer radius using the **Overpass API** to identify the single nearest medical facility.
    *   **Automated Dispatch**: Rapidly summarizes the patient's known medical history from the vector database and drafts actionable emergency SMS notifications for both family members and emergency medical services (EMS).
*   **📄 RAG Agent (Retrieval-Augmented Generation)**: Handles queries regarding the patient's specific health data.
    *   **Document Ingestion**: Users can upload medical reports (PDF). The text is chunked and embedded into a persistent local **FAISS Vector Database** using `sentence-transformers/all-MiniLM-L6-v2`.
    *   **Image OCR**: Users can upload prescription labels or medical images. **Gemini Vision** extracts the text and seamlessly merges the findings into the existing medical knowledge base.
    *   **Verified Answers**: The agent answers questions strictly based on the provided medical history and explicitly cites the source chunks used to generate the response, preventing hallucinations.
*   **🌐 Search Agent**: Functions as a medical encyclopedia for general knowledge.
    *   **Google Search Grounding**: Equipped with Google Search tools to fetch factual, real-time information from the web when answering broad medical or pharmaceutical questions.

---

## 🛠️ Technology Stack

*   **Frontend**: [Streamlit](https://streamlit.io/) with `streamlit-geolocation`
*   **Large Language Model (LLM)**: Google Gemini 2.5 Flash (`langchain-google-genai`)
*   **Framework**: [LangChain](https://python.langchain.com/) for agent routing, memory, and RAG pipelines.
*   **Vector Store**: [FAISS](https://faiss.ai/) (Facebook AI Similarity Search)
*   **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
*   **Location Services**: OpenStreetMap (OSM), Nominatim, Overpass API (Free/No API Key Required)
*   **Observability**: [LangSmith](https://smith.langchain.com/) support for tracing API calls.

---

## 🚀 Getting Started

### Prerequisites

*   Python 3.10 or higher.
*   A Google Gemini API Key.
*   (Optional) A LangSmith API Key for tracing and debugging LLM outputs.


### Running the Application

Start the Streamlit development server locally:
```bash
python -m streamlit run frontend/streamlit_app.py
```
*The web interface will automatically open in your default browser at `http://localhost:8501`.*

---

## 📁 Project Structure

```text
chatbot-project/
├── backend/
│   ├── agents/
│   │   ├── emergency_agent.py   # Emergency protocol, location parsing, and SMS drafting
│   │   ├── rag_agent.py         # Query handler for internal vector database
│   │   └── search_agent.py      # Standard LLM handler with Google Search grounding
│   ├── llm/
│   │   └── model_loader.py      # LLM initialization parameters
│   ├── rag/
│   │   ├── pdf_ingest.py        # Pipeline for chunking, embedding, and saving to FAISS
│   │   └── retriever.py         # Utility to load the persistent FAISS index
│   ├── router/
│   │   └── router_agent.py      # LangChain conditional router for intent classification
│   └── tools/
│       ├── maps_tool.py         # Reverse geocoding and OSM Overpass hospital lookup
│       └── ocr_tool.py          # Gemini Vision integration for image text extraction
├── frontend/
│   └── streamlit_app.py         # Application UI, state management, and file upload handlers
├── data/                        # Local temp directory for pdf uploads (Git-ignored)
├── vector_db/                   # Local binary FAISS index (Git-ignored)
├── .env.example                 # Template for required environment variables
├── .gitignore                   # Security exclusions
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---



---

> **Disclaimer**: This is an AI-powered technical demonstration designed for educational purposes. It is absolutely not a replacement for professional medical advice, diagnosis, or treatment. In the event of a real medical emergency, you must contact your local emergency services (e.g., 911, 999, 112) immediately.
