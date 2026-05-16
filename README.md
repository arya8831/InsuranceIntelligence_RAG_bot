# AI-Powered Insurance Policy Chatbot using Gemini LLM and RAG Architecture

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-LangChain-orange.svg)](https://github.com/langchain-ai/langchain)
[![LLM](https://img.shields.io/badge/LLM-Gemini%202.0%20Flash-brightgreen.svg)](https://deepmind.google/technologies/gemini/)
[![VectorDB](https://img.shields.io/badge/VectorStore-FAISS%20%2F%20AstraDB-red.svg)](https://github.com/facebookresearch/faiss)

Developed for the **BFSI Launchpad 2025** hackathon under the theme **Smart Automation using AI in BFSI sector**.

---

## 📌 Project Overview

In the insurance industry, customers frequently face difficulties navigating complex policy documents to find specific details regarding health, life, auto, and home coverage options, premiums, and claim processes. 

This project is an intelligent, automated RAG (Retrieval-Augmented Generation) chatbot system that securely ingests unstructured PDF insurance policies. By combining semantic vector search with Large Language Models (LLMs), it yields contextually precise, highly accurate answers grounded entirely in the local policy repository, successfully mitigating model hallucinations.

🎥 **[Watch the Video Demonstration](https://www.youtube.com/watch?v=SsOPdWvoYIs)**

---

## ✨ Key Features

* **Automated Document Ingestion:** Efficiently loads and extracts data page-by-page from policy PDFs using LangChain utilities.
* **Semantic Query Understanding:** Utilizes high-dimensional vector representations to match complex natural language queries against policy text.
* **Context-Aware Conversations:** Tracks and injects the past 2–3 interactions per session to handle seamless follow-up user inputs without context loss.
* **Hybrid QA with Intelligent Fallback:** Implements a fallback route via full conversation history direct to the Gemini API if semantic index answers return weak or vague snippets.
* **Multi-Format Interfaces:** Includes support for Jupyter-style HTML rendered local terminal outputs as well as a rich web administrative dashboard for file uploads.
* **Multilingual Capabilities:** A translation-ready layer supporting up to 32 different languages to maximize user accessibility.

---

## 🏗️ System Architecture

The pipeline processes user queries and policy ingestion through a structured Retrieval-Augmented Generation layout:

### Pipeline Workflow

```
[ Unstructured PDF ] ──> [ PyPDFLoader ] ──> [ Text Splitter (1000/200) ]
                                                            │
                                                            ▼
[ FAISS / Astra DB ] <── [ Indexing Store ] <── [ Google Embedding API ]
        │
        ▼ (Semantic Similarity Match)
[ Ranked Document Context ] ──┐
                              ├─> [ RetrievalQA Chain ] ──> [ Gemini 2.0 Flash ] ──> [ Structured UI Answer ]
[ User Natural Query ] ───────┘
```

### Retrieval & Generation Architecture

Below is the architectural flow illustrating the parsing, vectorization, indexing, and retrieval mechanics of the RAG system:

<p align="center">
  <img src="https://github.com/user-attachments/assets/65e90ea2-bdff-4b8c-b02f-519782800d36" alt="System Architecture Diagram" width="85%" />
</p>

1. **Preprocessing:** Documents are converted into overlapping 1000-character chunks to maintain semantic integrity across boundaries using `RecursiveCharacterTextSplitter`.
2. **Indexing:** Chunks transform into vectors using `models/embedding-001` and settle into local FAISS vector spaces or serverless DataStax Astra DB setups.
3. **Generation:** Merged query variables pass straight to `models/gemini-2.0-flash` for crisp language generation.

---

## 📸 Application Screenshots & UI Gallery

### 🛠️ Chat & Admin Interface

The system offers an intuitive, easy-to-navigate dashboard for policy interaction and continuous conversation management.

<p align="center">
  <img src="https://github.com/user-attachments/assets/3cd93750-6334-4f15-aefd-367120965c5a" alt="Chat UI Baseline" width="48%" />
  &nbsp;
  <img src="https://github.com/user-attachments/assets/1567baeb-2d4e-4f16-acb1-4f151528659d" alt="Active Conversation" width="48%" />
</p>

### 🗄️ Database & Connectivity

Secure cloud vector persistence layer managed remotely via DataStax Astra DB utilizing automated API client integration routines.

<p align="center">
  <img src="https://github.com/user-attachments/assets/f2a38f59-e743-4579-aad5-f95b731174ee" alt="Astra DB Dashboard" width="48%" />
  &nbsp;
  <img src="https://github.com/user-attachments/assets/94824707-cda4-44b4-84c6-43b23c28df79" alt="Client Python Connection" width="48%" />
</p>

### 📂 Document Upload & Processing

Administrators can drop files straight into the workspace pipeline, instantly converting long-form legal contracts into structured vectors.

<p align="center">
  <img src="https://github.com/user-attachments/assets/969641ea-e8ce-4bc9-930f-b258673a5a87" alt="Upload Portal" width="48%" />
  &nbsp;
  <img src="https://github.com/user-attachments/assets/bd2da259-7ff0-48e2-9f37-d2ce0c13ee4c" alt="Processing Pipeline Engine" width="48%" />
</p>

---

## 🛠️ Technology Stack

* **Language:** Python 3.9+
* **Orchestration Framework:** LangChain
* **Document Parsing:** `PyPDFLoader`
* **Embedding Model:** `GoogleGenerativeAIEmbeddings` (`models/embedding-001`)
* **Vector Store Index:** FAISS & DataStax Astra DB
* **Foundation LLM:** `ChatGoogleGenerativeAI` (`models/gemini-2.0-flash`)
* **Frontend/UI:** Command-line wrapper + `IPython.display` (Ready for Streamlit implementation)

---

## 🚀 Getting Started

### Prerequisites

* Python 3.9 or higher
* A Google AI Studio API Key (for Gemini and its embeddings)
* *(Optional)* Astra DB Connection Endpoint & Application Token

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/bfsi-insurance-chatbot.git
   cd bfsi-insurance-chatbot
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install required dependencies:**
   ```bash
   pip install langchain langchain-google-genai faiss-cpu pypdf astrapy ipython
   ```

4. **Set your environment variables:**
   ```bash
   export GOOGLE_API_KEY="your-gemini-api-key-here"
   # If utilizing remote cloud databases:
   export ASTRA_DB_API_ENDPOINT="your-endpoint"
   export ASTRA_DB_APPLICATION_TOKEN="your-token"
   ```

---

## 💻 Usage

### Local CLI & Conversation Ingestion

To launch the semantic parser along with the chat environment loop, execute the primary execution file:
```bash
python main.py
```
* **To exit the conversation:** Simply type `exit`, `quit`, or `bye` at any time.

### Code Snippet Example

```python
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Initialize components
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = FAISS.load_local("faiss_index", embeddings)

llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash", temperature=0.3)
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

response = qa_chain.run("What coverage limits apply to pre-existing conditions?")
print(response)
```

---

## 📊 Challenges Faced & Resolutions

* **Short/Generic Context Responses:** Fixed by designing custom evaluation fallback logic. Whenever the QA chain retrieves sparse or generic fallback matches, the prompt contextualizes history natively via the LLM API.
* **Context Loss Across Conversations:** Handled dynamically via a sliding memory manager window capturing the last 3 user statements.

---

## 👥 Contributor

* **Arya Chatterjee** - *Meghnad Saha Institute of Technology*
* Project developed for the **BFSI Launchpad 2025**.
