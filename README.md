Gemini
write a github readme file for the project
Conversation with Gemini
write a github readme file for the project

Here is a professionally structured GitHub README.md file tailored specifically for your project based on the documentation and hackathon presentation details.  
+1

AI-Powered Insurance Policy Chatbot using Gemini LLM and RAG Architecture
Developed for the BFSI Launchpad 2025 hackathon under the theme Smart Automation using AI in BFSI sector.  
+1

📌 Project Overview
In the insurance industry, customers frequently face difficulties navigating complex policy documents to find specific details regarding health, life, auto, and home coverage options, premiums, and claim processes.  

This project is an intelligent, automated RAG (Retrieval-Augmented Generation) chatbot system that securely ingests unstructured PDF insurance policies. By combining semantic vector search with Large Language Models (LLMs), it yields contextually precise, highly accurate answers grounded entirely in the local policy repository, successfully mitigating model hallucinations.  
+4

🎥 Watch the Video Demonstration   : https://www.youtube.com/watch?v=SsOPdWvoYIs


✨ Key Features
Chat & Admin Interface
<img width="1054" height="575" alt="image" src="https://github.com/user-attachments/assets/3cd93750-6334-4f15-aefd-367120965c5a" />

Database & Connectivity <img width="1012" height="540" alt="image" src="https://github.com/user-attachments/assets/f2a38f59-e743-4579-aad5-f95b7311fb2c" />

Document Upload & Processing



Automated Document Ingestion: Efficiently loads and page-extracts raw data from policy PDFs using LangChain utilities.  
+2
<img width="1006" height="574" alt="image" src="https://github.com/user-attachments/assets/4cea439d-b4c6-403a-a69c-0739cb8c2f02" />
<img width="1016" height="607" alt="image" src="https://github.com/user-attachments/assets/b6d972cd-33c1-40c8-8ffe-7869d4bc0643" />


Semantic Query Understanding: Utilizes high-dimensional vector representations to match complex natural language queries against policy text.  
+3
<img width="940" height="434" alt="image" src="https://github.com/user-attachments/assets/99b00b0d-bea4-4f8d-9424-4a72cfa8df06" />


Context-Aware Conversations: Tracks and injects the past 2–3 interactions per session to handle seamless follow-up user inputs without context loss.  
+1


Hybrid QA with Intelligent Fallback: Implements a fallback route via full conversation history direct to the Gemini API if semantic index answers return weak or vague snippets.  
+3


Multi-Format Interfaces: Includes support for Jupyter-style HTML rendered local terminal outputs as well as a rich web administrative dashboard for file uploads.  
+3<img width="1056" height="582" alt="image" src="https://github.com/user-attachments/assets/438bfa66-cfd2-4dd5-8da5-cce99bf506f4" />


Multimodal Extensibility: Built-in foundational components for Whisper speech-to-text inputs, language translators (T5/GPT-2), and Google Text-to-Speech (gTTS) audio responses.  
+2

🏗️ System Architecture
The application runs on a standardized Retrieval-Augmented Generation (RAG) pipeline:  

[ Unstructured PDF ] ──> [ PyPDFLoader ] ──> [ Text Splitter (1000/200) ]
                                                            │
                                                            ▼
[ FAISS / Astra DB ] <── [ Indexing Store ] <── [ Google Embedding API ]
        │
        ▼ (Semantic Similarity Match)
[ Ranked Document Context ] ──┐
                              ├─> [ RetrievalQA Chain ] ──> [ Gemini 2.0 Flash ] ──> [ Structured UI Answer ]
[ User Natural Query ] ───────┘

Preprocessing: Documents are converted into overlapping 1000-character chunks to maintain semantic integrity across boundaries.  
+1


Indexing: Chunks transform into vectors using models/embedding-001 and settle into local FAISS vector spaces or serverless Astra DB setups.  
+3


Generation: Merged query variables pass straight to models/gemini-2.0-flash for crisp language generation.  
+2

🛠️ Technology Stack

Language: Python   


Orchestration Framework: LangChain   


Document Parsing: PyPDFLoader   


Chunking Layer: RecursiveCharacterTextSplitter (Size: 1000, Overlap: 200)   
+1


Vector Vector Embeddings: GoogleGenerativeAIEmbeddings (models/embedding-001)   
+1


Vector Store Index: FAISS & DataStax Astra DB   
+1


Foundation LLM: ChatGoogleGenerativeAI (models/gemini-2.0-flash)   
+1


Frontend/UI: Command-line wrapper + IPython.display (Ready for Streamlit implementation)   
+1

🚀 Getting Started
Prerequisites
Python 3.9 or higher

A Google AI Studio API Key (for Gemini and its embeddings)

(Optional) Astra DB Connection Endpoint & Application Token   

Installation
Clone the repository:

Bash
git clone https://github.com/your-username/bfsi-insurance-chatbot.git
cd bfsi-insurance-chatbot
Create and activate a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install required dependencies:

Bash
pip install langchain langchain-google-genai faiss-cpu pypdf astrapy ipython
Set your environment variables:

Bash
export GOOGLE_API_KEY="your-gemini-api-key-here"
# If utilizing remote cloud databases:
export ASTRA_DB_API_ENDPOINT="your-endpoint"
export ASTRA_DB_APPLICATION_TOKEN="your-token"
💻 Usage
Local CLI & Conversation Ingestion
To launch the semantic parser along with the chat environment loop, execute the primary execution file:

Bash
python main.py

To exit the conversation: Simply type exit, quit, or bye at any time.  

Code Snippet Example
Python
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
📊 Challenges Faced & Resolutions

Short/Generic Context Responses: Fixed by designing custom evaluation fallback logic. Whenever the QA chain retrieves sparse or generic fallback matches, the prompt contextualizes history natively via the LLM API.  
+4


Context Loss Across Conversations: Handled dynamically via a sliding memory manager window capturing the last 3 user statements.  
+1

👥 Contributor

Arya Chatterjee - Meghnad Saha Institute of Technology   
+1

Project developed for the BFSI Launchpad 2025.  

i am giving you the images that i want in the readme section

Here is your updated GitHub README.md file, seamlessly integrating the architectural flow diagram image you provided into the System Architecture section.

You can copy and paste this markdown directly into your repository.

AI-Powered Insurance Policy Chatbot using Gemini LLM and RAG Architecture
Developed for the BFSI Launchpad 2025 hackathon under the theme Smart Automation using AI in BFSI sector.

📌 Project Overview
In the insurance industry, customers frequently face difficulties navigating complex policy documents to find specific details regarding health, life, auto, and home coverage options, premiums, and claim processes.

This project is an intelligent, automated RAG (Retrieval-Augmented Generation) chatbot system that securely ingests unstructured PDF insurance policies. By combining semantic vector search with Large Language Models (LLMs), it yields contextually precise, highly accurate answers grounded entirely in the local policy repository, successfully mitigating model hallucinations.

🎥 Watch the Video Demonstration

✨ Key Features
Automated Document Ingestion: Efficiently loads and extracts data page-by-page from policy PDFs using LangChain utilities.

Semantic Query Understanding: Utilizes high-dimensional vector representations to match complex natural language queries against policy text.

Context-Aware Conversations: Tracks and injects the past 2–3 interactions per session to handle seamless follow-up user inputs without context loss.

Hybrid QA with Intelligent Fallback: Implements a fallback route via full conversation history direct to the Gemini API if semantic index answers return weak or vague snippets.

Multi-Format Interfaces: Includes support for Jupyter-style HTML rendered local terminal outputs as well as a rich web administrative dashboard for file uploads.

Multimodal Extensibility: Built-in foundational components for Whisper speech-to-text inputs, language translators (32 different languages supported), and Google Text-to-Speech (gTTS) audio responses.

🏗️ System Architecture
The pipeline processes user queries and policy ingestion through a structured Retrieval-Augmented Generation layout:

Pipeline Workflow
[ Unstructured PDF ] ──> [ PyPDFLoader ] ──> [ Text Splitter (1000/200) ]
                                                            │
                                                            ▼
[ FAISS / Astra DB ] <── [ Indexing Store ] <── [ Google Embedding API ]
        │
        ▼ (Semantic Similarity Match)
[ Ranked Document Context ] ──┐
                              ├─> [ RetrievalQA Chain ] ──> [ Gemini 2.0 Flash ] ──> [ Structured UI Answer ]
[ User Natural Query ] ───────┘
Retrieval & Generation Architecture
To display your system architecture flow visually, save your architecture diagram as architecture.png in your root or asset directory and reference it like this:

Preprocessing: Documents are converted into overlapping 1000-character chunks to maintain semantic integrity across boundaries using RecursiveCharacterTextSplitter.

Indexing: Chunks transform into vectors using models/embedding-001 and settle into local FAISS vector spaces or serverless DataStax Astra DB setups.

Generation: Merged query variables pass straight to models/gemini-2.0-flash for crisp language generation.

🛠️ Technology Stack
Language: Python

Orchestration Framework: LangChain

Document Parsing: PyPDFLoader

Embedding Model: GoogleGenerativeAIEmbeddings (models/embedding-001)

Vector Store Index: FAISS & DataStax Astra DB

Foundation LLM: ChatGoogleGenerativeAI (models/gemini-2.0-flash)

Frontend/UI: Command-line wrapper + IPython.display (Ready for Streamlit implementation)

🚀 Getting Started
Prerequisites
Python 3.9 or higher

A Google AI Studio API Key (for Gemini and its embeddings)

(Optional) Astra DB Connection Endpoint & Application Token

Installation
Clone the repository:

Bash
git clone https://github.com/your-username/bfsi-insurance-chatbot.git
cd bfsi-insurance-chatbot
Create and activate a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install required dependencies:

Bash
pip install langchain langchain-google-genai faiss-cpu pypdf astrapy ipython
Set your environment variables:

Bash
export GOOGLE_API_KEY="your-gemini-api-key-here"
# If utilizing remote cloud databases:
export ASTRA_DB_API_ENDPOINT="your-endpoint"
export ASTRA_DB_APPLICATION_TOKEN="your-token"
💻 Usage
Local CLI & Conversation Ingestion
To launch the semantic parser along with the chat environment loop, execute the primary execution file:

Bash
python main.py
To exit the conversation: Simply type exit, quit, or bye at any time.

Code Snippet Example
Python
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
📊 Challenges Faced & Resolutions
Short/Generic Context Responses: Fixed by designing custom evaluation fallback logic. Whenever the QA chain retrieves sparse or generic fallback matches, the prompt contextualizes history natively via the LLM API.

Context Loss Across Conversations: Handled dynamically via a sliding memory manager window capturing the last 3 user statements.

👥 Contributor
Arya Chatterjee - Meghnad Saha Institute of Technology

Project developed for the BFSI Launchpad 2025.

Chat

& Admin Interface

 

 

 

Database & Connectivity

 

 



Document Upload & Processing

Here is the fully completed, comprehensive GitHub README.md for your repository. It organizes your project details beautifully and structures all your uploaded screenshots into clear, categorized sections (User & Admin Interface, Database, and Document Ingestion) to show off your working model.

AI-Powered Insurance Policy Chatbot using Gemini LLM and RAG Architecture
Developed for the BFSI Launchpad 2025 hackathon under the theme Smart Automation using AI in BFSI sector.

📌 Project Overview
In the insurance industry, customers frequently face difficulties navigating complex policy documents to find specific details regarding health, life, auto, and home coverage options, premiums, and claim processes.

This project is an intelligent, automated RAG (Retrieval-Augmented Generation) chatbot system that securely ingests unstructured PDF insurance policies. By combining semantic vector search with Large Language Models (LLMs), it yields contextually precise, highly accurate answers grounded entirely in the local policy repository, successfully mitigating model hallucinations.

🎥 Watch the Video Demonstration

✨ Key Features
Automated Document Ingestion: Efficiently loads and extracts data page-by-page from policy PDFs using LangChain utilities.

Semantic Query Understanding: Utilizes high-dimensional vector representations to match complex natural language queries against policy text.

Context-Aware Conversations: Tracks and injects the past 2–3 interactions per session to handle seamless follow-up user inputs without context loss.

Hybrid QA with Intelligent Fallback: Implements a fallback route via full conversation history direct to the Gemini API if semantic index answers return weak or vague snippets.

Multi-Format Interfaces: Includes support for Jupyter-style HTML rendered local terminal outputs as well as a rich web administrative dashboard for file uploads.

Multimodal Extensibility: Built-in foundational components for Whisper speech-to-text inputs, language translators (32 different languages supported), and Google Text-to-Speech (gTTS) audio responses.

🏗️ System Architecture
The pipeline processes user queries and policy ingestion through a structured Retrieval-Augmented Generation layout:

Pipeline Workflow
[ Unstructured PDF ] ──> [ PyPDFLoader ] ──> [ Text Splitter (1000/200) ]
                                                            │
                                                            ▼
[ FAISS / Astra DB ] <── [ Indexing Store ] <── [ Google Embedding API ]
        │
        ▼ (Semantic Similarity Match)
[ Ranked Document Context ] ──┐
                              ├─> [ RetrievalQA Chain ] ──> [ Gemini 2.0 Flash ] ──> [ Structured UI Answer ]
[ User Natural Query ] ───────┘
Retrieval & Generation Architecture
Below is the architectural flow illustrating the parsing, vectorization, indexing, and retrieval mechanics of the RAG system:

Preprocessing: Documents are converted into overlapping 1000-character chunks to maintain semantic integrity across boundaries using RecursiveCharacterTextSplitter.

Indexing: Chunks transform into vectors using models/embedding-001 and settle into local FAISS vector spaces or serverless DataStax Astra DB setups.

Generation: Merged query variables pass straight to models/gemini-2.0-flash for crisp language generation.

📸 Application Screenshots & Interface
💡 Note: To render these images correctly on your GitHub profile page, rename your uploaded files to match the names in the brackets below (e.g., chat_ui.png, astra_db.png) and place them in an /assets or root folder inside your repository.

🛠️ Chat & Admin Interface
The system offers an intuitive, easy-to-navigate dashboard for policy interaction and continuous conversation management.

Chat Interface Baseline	Active Dialogue Session

Empty Chat Context & Initialization


Contextual Streaming QA Session

🗄️ Database & Connectivity
Secure cloud vector persistence layer managed remotely via DataStax Astra DB utilizing automated API client integration routines.

Astra DB Vector Console	Client Initialization Setup

Vector Database Status & Active Tokens


AstraPy Integration Framework Code

📂 Document Upload & Processing
Administrators can drop files straight into the workspace pipeline, instantly converting long-form legal contracts into structured data.

Dropzone Document Ingestion	Document Parser Runtime

Drag-and-Drop Insurance Document Portal


Tokenization & Storage Pipeline Activation

🛠️ Technology Stack
Language: Python

Orchestration Framework: LangChain

Document Parsing: PyPDFLoader

Embedding Model: GoogleGenerativeAIEmbeddings (models/embedding-001)

Vector Store Index: FAISS & DataStax Astra DB

Foundation LLM: ChatGoogleGenerativeAI (models/gemini-2.0-flash)

Frontend/UI: Command-line wrapper + IPython.display (Ready for Streamlit implementation)

🚀 Getting Started
Prerequisites
Python 3.9 or higher

A Google AI Studio API Key (for Gemini and its embeddings)

(Optional) Astra DB Connection Endpoint & Application Token

Installation
Clone the repository:

Bash
git clone https://github.com/your-username/bfsi-insurance-chatbot.git
cd bfsi-insurance-chatbot
Create and activate a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install required dependencies:

Bash
pip install langchain langchain-google-genai faiss-cpu pypdf astrapy ipython
Set your environment variables:

Bash
export GOOGLE_API_KEY="your-gemini-api-key-here"
# If utilizing remote cloud databases:
export ASTRA_DB_API_ENDPOINT="your-endpoint"
export ASTRA_DB_APPLICATION_TOKEN="your-token"
💻 Usage
Local CLI & Conversation Ingestion
To launch the semantic parser along with the chat environment loop, execute the primary execution file:

Bash
python main.py
To exit the conversation: Simply type exit, quit, or bye at any time.

Code Snippet Example
Python
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
📊 Challenges Faced & Resolutions
Short/Generic Context Responses: Fixed by designing custom evaluation fallback logic. Whenever the QA chain retrieves sparse or generic fallback matches, the prompt contextualizes history natively via the LLM API.

Context Loss Across Conversations: Handled dynamically via a sliding memory manager window capturing the last 3 user statements.

👥 Contributor
Arya Chatterjee - Meghnad Saha Institute of Technology

Project developed for the BFSI Launchpad 2025.

give me a .md file to download

[ Unstructured PDF ] ──> [ PyPDFLoader ] ──> [ Text Splitter (1000/200) ]
│
▼
[ FAISS / Astra DB ] <── [ Indexing Store ] <── [ Google Embedding API ]
│
▼ (Semantic Similarity Match)
[ Ranked Document Context ] ──┐
├─> [ RetrievalQA Chain ] ──> [ Gemini 2.0 Flash ] ──> [ Structured UI Answer ]
[ User Natural Query ] ───────┘


### Retrieval & Generation Architecture
Below is the architectural flow illustrating the parsing, vectorization, indexing, and retrieval mechanics of the RAG system:

![System Architecture](./architecture.png)

1. **Preprocessing:** Documents are converted into overlapping 1000-character chunks to maintain semantic integrity across boundaries using `RecursiveCharacterTextSplitter`.
2. **Indexing:** Chunks transform into vectors using `models/embedding-001` and settle into local FAISS vector spaces or serverless DataStax Astra DB setups.
3. **Generation:** Merged query variables pass straight to `models/gemini-2.0-flash` for crisp language generation.

---

## 📸 Application Screenshots & Interface

> 💡 *Note: To render these images correctly on your GitHub profile page, rename your uploaded files to match the names in the brackets below (e.g., `chat_ui.png`, `astra_db.png`) and place them in an `/assets` or root folder inside your repository.*

### 🛠️ Chat & Admin Interface
The system offers an intuitive, easy-to-navigate dashboard for policy interaction and continuous conversation management.

| Chat Interface Baseline | Active Dialogue Session |
| :---: | :---: |
| ![Chat UI Placeholder](./chat_ui.png) <br> *Empty Chat Context & Initialization* | ![Active Conversation](./active_chat.png) <br> *Contextual Streaming QA Session* |

### 🗄️ Database & Connectivity
Secure cloud vector persistence layer managed remotely via DataStax Astra DB utilizing automated API client integration routines.

| Astra DB Vector Console | Client Initialization Setup |
| :---: | :---: |
| ![Astra DB Token Status](./astra_dashboard.png) <br> *Vector Database Status & Active Tokens* | ![Client Python Connection](./db_connection.png) <br> *AstraPy Integration Framework Code* |

### 📂 Document Upload & Processing
Administrators can drop files straight into the workspace pipeline, instantly converting long-form legal contracts into structured data.

| Dropzone Document Ingestion | Document Parser Runtime |
| :---: | :---: |
| ![Upload Area](./upload_zone.png) <br> *Drag-and-Drop Insurance Document Portal* | ![Processing Engine](./processing_view.png) <br> *Tokenization & Storage Pipeline Activation* |

---

## 🛠️ Technology Stack
* **Language:** Python
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
* (Optional) Astra DB Connection Endpoint & Application Token

### Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/bfsi-insurance-chatbot.git](https://github.com/your-username/bfsi-insurance-chatbot.git)
   cd bfsi-insurance-chatbot
Create and activate a virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
Install required dependencies:

Bash
pip install langchain langchain-google-genai faiss-cpu pypdf astrapy ipython
Set your environment variables:

Bash
export GOOGLE_API_KEY="your-gemini-api-key-here"
# If utilizing remote cloud databases:
export ASTRA_DB_API_ENDPOINT="your-endpoint"
export ASTRA_DB_APPLICATION_TOKEN="your-token"
💻 Usage
Local CLI & Conversation Ingestion
To launch the semantic parser along with the chat environment loop, execute the primary execution file:

Bash
python main.py
To exit the conversation: Simply type exit, quit, or bye at any time.

Code Snippet Example
Python
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
📊 Challenges Faced & Resolutions
Short/Generic Context Responses: Fixed by designing custom evaluation fallback logic. Whenever the QA chain retrieves sparse or generic fallback matches, the prompt contextualizes history natively via the LLM API.

Context Loss Across Conversations: Handled dynamically via a sliding memory manager window capturing the last 3 user statements.

👥 Contributor
Arya Chatterjee - Meghnad Saha Institute of Technology

Project developed for the BFSI Launchpad 2025.
"""

file_path = "README.md"
with open(file_path, "w", encoding="utf-8") as f:
f.write(readme_content)

print(f"File successfully created: {file_path}")

Your markdown file is ready
[file-tag: code-generated-file-0-1778927723913176904]

I have generated the finalized `README.md` file including all structured project fields, architectural flows, technical documentation steps, and references for the UI interface dashboards. You can download and place it directly into the root folder of your project repository.
no no give me the file i will download and upload

Your Markdown file is ready for download:
MD icon
 README 
MD

You can save this file directly as README.md and upload it straight to your GitHub repository! All your project details, images, code sections, and architecture layouts have been properly formatted inside it.





Gemini is AI and can make mistakes.

# AI-Powered Insurance Policy Chatbot using Gemini LLM and RAG Architecture

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-LangChain-orange.svg)](https://github.com/langchain-ai/langchain)
[![LLM](https://img.shields.io/badge/LLM-Gemini%202.0%20Flash-brightgreen.svg)](https://deepmind.google/technologies/gemini/)
[![VectorDB](https://img.shields.io/badge/VectorStore-FAISS%20%2F%20AstraDB-red.svg)](https://github.com/facebookresearch/faiss)

Developed for the **BFSI Launchpad 2025** hackathon under the theme *Smart Automation using AI in BFSI sector*.

## 📌 Project Overview
In the insurance industry, customers frequently face difficulties navigating complex policy documents to find specific details regarding health, life, auto, and home coverage options, premiums, and claim processes. 

This project is an intelligent, automated RAG (Retrieval-Augmented Generation) chatbot system that securely ingests unstructured PDF insurance policies. By combining semantic vector search with Large Language Models (LLMs), it yields contextually precise, highly accurate answers grounded entirely in the local policy repository, successfully mitigating model hallucinations.

🎥 **[Watch the Video Demonstration](https://youtu.be/SsOPdWvoYIs)**

---

## ✨ Key Features
* **Automated Document Ingestion:** Efficiently loads and extracts data page-by-page from policy PDFs using LangChain utilities.
* **Semantic Query Understanding:** Utilizes high-dimensional vector representations to match complex natural language queries against policy text.
* **Context-Aware Conversations:** Tracks and injects the past 2–3 interactions per session to handle seamless follow-up user inputs without context loss.
* **Hybrid QA with Intelligent Fallback:** Implements a fallback route via full conversation history direct to the Gemini API if semantic index answers return weak or vague snippets.
* **Multi-Format Interfaces:** Includes support for Jupyter-style HTML rendered local terminal outputs as well as a rich web administrative dashboard for file uploads.
* **Multimodal Extensibility:** Built-in foundational components for Whisper speech-to-text inputs, language translators (32 different languages supported), and Google Text-to-Speech (gTTS) audio responses.

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

![System Architecture](./architecture.png)

1. **Preprocessing:** Documents are converted into overlapping 1000-character chunks to maintain semantic integrity across boundaries using `RecursiveCharacterTextSplitter`.
2. **Indexing:** Chunks transform into vectors using `models/embedding-001` and settle into local FAISS vector spaces or serverless DataStax Astra DB setups.
3. **Generation:** Merged query variables pass straight to `models/gemini-2.0-flash` for crisp language generation.

---

## 📸 Application Screenshots & Interface

> 💡 *Note: To render these images correctly on your GitHub profile page, rename your uploaded files to match the names in the brackets below (e.g., `chat_ui.png`, `astra_db.png`) and place them in an `/assets` or root folder inside your repository.*

### 🛠️ Chat & Admin Interface
The system offers an intuitive, easy-to-navigate dashboard for policy interaction and continuous conversation management.

| Chat Interface Baseline | Active Dialogue Session |
| :---: | :---: |
| ![Chat UI Placeholder](./chat_ui.png) <br> *Empty Chat Context & Initialization* | ![Active Conversation](./active_chat.png) <br> *Contextual Streaming QA Session* |

### 🗄️ Database & Connectivity
Secure cloud vector persistence layer managed remotely via DataStax Astra DB utilizing automated API client integration routines.

| Astra DB Vector Console | Client Initialization Setup |
| :---: | :---: |
| ![Astra DB Token Status](./astra_dashboard.png) <br> *Vector Database Status & Active Tokens* | ![Client Python Connection](./db_connection.png) <br> *AstraPy Integration Framework Code* |

### 📂 Document Upload & Processing
Administrators can drop files straight into the workspace pipeline, instantly converting long-form legal contracts into structured data.

| Dropzone Document Ingestion | Document Parser Runtime |
| :---: | :---: |
| ![Upload Area](./upload_zone.png) <br> *Drag-and-Drop Insurance Document Portal* | ![Processing Engine](./processing_view.png) <br> *Tokenization & Storage Pipeline Activation* |

---

## 🛠️ Technology Stack
* **Language:** Python
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
* (Optional) Astra DB Connection Endpoint & Application Token

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/bfsi-insurance-chatbot.git
   cd bfsi-insurance-chatbot
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts ctivate
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
* **Arya Chatterjee** 

