import os
import pickle
from langchain_core.documents import Document

def create_or_load_vector_store(documents, persist_directory="simple_index"):
    """
    Create a new simple vector store or load an existing one.
    
    This is a very simplified implementation for demo purposes that doesn't require 
    external embedding libraries. In a production environment, you would use 
    proper vector stores like FAISS, Chroma, or Pinecone.
    
    Args:
        documents: List of documents to index
        persist_directory: Directory to save the vector store
        
    Returns:
        A simple vector retriever object that mimics the retriever interface
    """
    # Create directory if it doesn't exist
    os.makedirs(persist_directory, exist_ok=True)
    index_path = os.path.join(persist_directory, "simple_index.pkl")
    
    # Create SimpleVectorStore class
    class SimpleVectorStore:
        def __init__(self, docs=None):
            self.documents = docs or []
        
        def save(self, path):
            with open(path, 'wb') as f:
                pickle.dump(self.documents, f)
        
        @classmethod
        def load(cls, path):
            try:
                with open(path, 'rb') as f:
                    docs = pickle.load(f)
                return cls(docs)
            except Exception as e:
                print(f"Error loading index: {e}")
                return cls()
        
        def add_documents(self, docs):
            self.documents.extend(docs)
        
        def as_retriever(self, search_kwargs=None):
            search_kwargs = search_kwargs or {"k": 3}
            
            # Create a simple retriever that searches for keywords
            class SimpleRetriever:
                def __init__(self, store, search_kwargs):
                    self.store = store
                    self.k = search_kwargs.get("k", 3)
                
                def get_relevant_documents(self, query):
                    # Very simple keyword-based retrieval (not semantic)
                    query_terms = set(query.lower().split())
                    
                    # Score documents by number of matching terms
                    scored_docs = []
                    for doc in self.store.documents:
                        content = doc.page_content.lower()
                        score = sum(1 for term in query_terms if term in content)
                        scored_docs.append((score, doc))
                    
                    # Sort by score and return top k
                    scored_docs.sort(reverse=True, key=lambda x: x[0])
                    return [doc for _, doc in scored_docs[:self.k]]
                
                def invoke(self, query):
                    return self.get_relevant_documents(query)
            
            return SimpleRetriever(self, search_kwargs)
    
    # Check if the vector store already exists
    if os.path.exists(index_path):
        print(f"Loading existing simple index from {index_path}")
        vector_store = SimpleVectorStore.load(index_path)
        
        # Add new documents if provided
        if documents:
            print(f"Adding {len(documents)} new documents to the index")
            vector_store.add_documents(documents)
            vector_store.save(index_path)
    else:
        print(f"Creating new simple index in {persist_directory}")
        # Create new vector store
        vector_store = SimpleVectorStore(documents)
        
        # Save the vector store
        vector_store.save(index_path)
    
    return vector_store
