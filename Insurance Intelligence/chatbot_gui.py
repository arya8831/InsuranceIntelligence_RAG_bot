import os
import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA

# Set your Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyByIdxyX9efBoFQjA_VMJu3usKIUqnZPWs"

# PDF folder path
pdf_folder_path = "D:/onedrive work/OneDrive - MSFT/Desktop/new app1/uploaded_pdfs"
pdf_files = [f for f in os.listdir(pdf_folder_path) if f.endswith('.pdf')]

# Load and split PDFs into chunks
documents = []
for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder_path, pdf_file)
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    documents.extend(docs)

# Split the documents into smaller chunks for embedding
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# Create embeddings using Google Generative AI
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create the vectorstore
vectorstore = FAISS.from_documents(chunks, embedding=embeddings)

# Initialize the Gemini LLM for answering questions
llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash")

# Initialize the QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Function to ask the bot a question with output length limitation
def ask_bot(query, context):
    result = qa_chain({"query": query})
    
    # Get the response and limit to 1000 characters
    bot_response = result['result'][:1000]
    
    # Update conversation context
    context.append({"role": "User", "text": query})
    context.append({"role": "Bot", "text": bot_response})
    
    # Ensure only the last 3 exchanges are kept in context (2-3 messages)
    if len(context) > 6:  # Each exchange is two messages (user + bot)
        context = context[-6:]
    
    return bot_response, context

# Streamlit app setup
st.title("AI Insurance Policy Chatbot")

# Create a session state to hold previous conversation context
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Display conversation history
for i, msg in enumerate(st.session_state.conversation):
    st.write(f"**{msg['role']}**: {msg['text']}")

# User input and response handling
user_input = st.text_input("Ask me anything about insurance!")

if user_input:
    # Get the response from the chatbot and update the conversation context
    response, updated_conversation = ask_bot(user_input, st.session_state.conversation)
    
    # Update session state with the new conversation history
    st.session_state.conversation = updated_conversation
    
    # Display the response
    st.write(f"**Bot**: {response}")
