import os
import shutil
import streamlit as st
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Set Gemini API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyByIdxyX9efBoFQjA_VMJu3usKIUqnZPWs"

# Folder to store uploaded PDFs
PDF_FOLDER = "uploaded_pdfs"
os.makedirs(PDF_FOLDER, exist_ok=True)

# Streamlit Page Setup
st.set_page_config(page_title="📄 Gemini PDF QA Bot", layout="centered")
st.title("📄 AI Insurance PDF Chatbot")
st.markdown("Upload your insurance PDFs, then ask questions based on the content.")

# --- 1. PDF Upload ---
uploaded_files = st.file_uploader("Upload PDF(s)", type=["pdf"], accept_multiple_files=True)
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(PDF_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(uploaded_file, f)
    st.success(f"Uploaded {len(uploaded_files)} file(s). Please refresh to load them.")

# --- 2. Load PDFs + Create Vectorstore ---
@st.cache_resource
def load_vectorstore(pdf_dir):
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    if not pdf_files:
        return None, []

    all_docs = []
    for pdf in pdf_files:
        loader = PyPDFLoader(os.path.join(pdf_dir, pdf))
        all_docs.extend(loader.load())

    # Better chunking for improved context
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
    chunks = splitter.split_documents(all_docs)

    # Create vectorstore with Gemini embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
    return vectorstore, pdf_files

vectorstore, pdf_names = load_vectorstore(PDF_FOLDER)

# --- 3. Q&A Section ---
if not pdf_names:
    st.warning("Please upload PDF files to begin.")
else:
    st.success(f"Loaded {len(pdf_names)} PDFs: {', '.join(pdf_names)}")

    # Initialize Gemini Pro + Custom Prompt
    llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash")
    
    custom_prompt = PromptTemplate.from_template("""
You are an intelligent insurance assistant.
Answer the user's question using only the context from the documents provided below.

Context:
{context}

Question: {question}
""")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff",
        chain_type_kwargs={"prompt": custom_prompt},
        return_source_documents=True
    )

    # Store chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Ask a question
    with st.form("qa_form", clear_on_submit=True):
        question = st.text_input("💬 Ask a question about your PDFs:")
        submit = st.form_submit_button("Get Answer")

    if submit and question:
        result = qa_chain({"query": question})
        response = result['result']

        # Save chat
        st.session_state.chat_history.append((question, response))
        st.session_state.chat_history = st.session_state.chat_history[-5:]

        # Show retrieved context (debug)
        with st.expander("📄 Retrieved Chunks (for debugging)", expanded=False):
            for i, doc in enumerate(result['source_documents']):
                st.markdown(f"**Chunk {i+1}:**")
                st.markdown(doc.page_content[:1000])  # Preview first 1000 characters

    # Display chat
    for q, a in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant"):
            st.markdown(a.replace("*", "•").replace("\n", "<br>"), unsafe_allow_html=True)
