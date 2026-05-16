import os
import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file or text file.
    
    Args:
        pdf_path: Path to the PDF or text file
        
    Returns:
        A string containing the text extracted from the file
    """
    try:
        if pdf_path.lower().endswith('.pdf'):
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                # Extract text from each page
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n\n"
            return text
        elif pdf_path.lower().endswith('.txt'):
            # Handle text files for demo purposes
            with open(pdf_path, 'r') as file:
                return file.read()
        else:
            print(f"Unsupported file format: {pdf_path}")
            return ""
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return ""

def process_pdf_documents(directory_path):
    """
    Process all PDF documents in a directory.
    
    Args:
        directory_path: Path to the directory containing PDF files
        
    Returns:
        A list of Document objects with text chunks and metadata
    """
    documents = []
    
    # Check if directory exists
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist")
        return documents
    
    # Get list of supported document files in directory
    doc_files = [f for f in os.listdir(directory_path) if f.lower().endswith(('.pdf', '.txt'))]
    
    if not doc_files:
        print(f"No supported document files found in {directory_path}")
        return documents
    
    # Process each document file
    for doc_file in doc_files:
        doc_path = os.path.join(directory_path, doc_file)
        text = extract_text_from_pdf(doc_path)
        
        if text:
            # Create text splitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            
            # Split text into chunks
            chunks = text_splitter.split_text(text)
            
            # Create Document objects with metadata
            for i, chunk in enumerate(chunks):
                # Try to determine which page this chunk is from based on its position
                estimated_page = i // 2 + 1  # A rough estimate - 2 chunks per page on average
                
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": doc_path,
                        "page": estimated_page,
                        "document": doc_file,
                    }
                )
                documents.append(doc)
    
    return documents
