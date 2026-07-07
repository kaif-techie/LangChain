# 📚 AI Competitive Exam Tutor & Syllabus Analyzer

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-Fast_Inference-f55036)

An intelligent, multi-phase AI agent designed to revolutionize how students prepare for competitive exams. By leveraging **LangChain**, **Groq (Llama 3)**, and a **Retrieval-Augmented Generation (RAG)** architecture, this application transforms static, unstructured syllabus PDFs into personalized, interactive study roadmaps.

## ✨ Features

* **Intelligent PDF Parsing:** Uses `pypdf` to extract raw, complex text from dense syllabus documents (multi-column, tables, etc.).
* **Structured Data Extraction:** Forces LLM outputs into strict, predictable JSON schemas using `Pydantic` and LangChain's structured output tools.
* **Lightning-Fast Inference:** Powered by Groq's API (`llama3-70b-8192`) for near-instantaneous syllabus analysis.
* **Interactive UI:** A stateful **Streamlit** dashboard that allows users to upload documents, view their personalized roadmap, and track study progress via interactive checklists.
* **Local RAG Pipeline (Phase 2):** Integrates local vector search using `ChromaDB` and HuggingFace embeddings to retrieve factual answers directly from standard textbooks.

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Orchestration:** LangChain
* **LLM Engine:** Groq (Llama-3-70B)
* **Embeddings:** HuggingFace (`all-MiniLM-L6-v2`)
* **Vector Database:** ChromaDB
* **Data Handling:** PyPDF, Pydantic

## 📂 Project Structure

```text
ai-exam-tutor/
├── app.py                  # Main Streamlit application & UI
├── phase2_retriever.py     # Script to build and query the local Vector DB
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules (protects API keys & databases)
└── README.md               # Project documentation
