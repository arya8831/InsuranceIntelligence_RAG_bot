import streamlit as st
import os
from utils.db_utils import (
    get_db_session, User, Conversation, Message, Document,
    get_all_documents, mark_document_as_processed
)

# Page configuration
st.set_page_config(
    page_title="Insurance Policy Assistant - Admin",
    page_icon="🤖",
    layout="wide"
)

st.title("Database Administration")

# Create tabs for different admin functions
tab1, tab2, tab3 = st.tabs(["Users & Conversations", "Documents", "System Status"])

with tab1:
    st.header("Users and Conversations")
    
    # Get all users and conversations
    try:
        session = get_db_session()
        users = session.query(User).all()
        
        if users:
            for user in users:
                st.subheader(f"User: {user.name} ({user.email})")
                st.text(f"Created: {user.created_at}")
                
                conversations = session.query(Conversation).filter(Conversation.user_id == user.id).all()
                
                if conversations:
                    for conversation in conversations:
                        with st.expander(f"Conversation: {conversation.title} (ID: {conversation.id})"):
                            st.text(f"Created: {conversation.created_at}")
                            
                            messages = session.query(Message).filter(Message.conversation_id == conversation.id).order_by(Message.created_at).all()
                            
                            if messages:
                                for message in messages:
                                    if message.role == "user":
                                        st.markdown(f"**User** ({message.created_at}):")
                                    else:
                                        st.markdown(f"**Assistant** ({message.created_at}):")
                                    st.markdown(f"> {message.content}")
                                    st.markdown("---")
                            else:
                                st.info("No messages in this conversation.")
                else:
                    st.info("No conversations for this user.")
        else:
            st.info("No users in the database.")
    except Exception as e:
        st.error(f"Error querying database: {e}")
    finally:
        session.close()

with tab2:
    st.header("Document Management")
    
    try:
        documents = get_all_documents()
        
        if documents:
            st.text(f"Total documents: {len(documents)}")
            
            # Create a table of documents
            doc_data = []
            for doc in documents:
                doc_data.append({
                    "ID": doc.id,
                    "Filename": doc.filename,
                    "Path": doc.file_path,
                    "Type": doc.content_type,
                    "Processed": "✅" if doc.processed else "❌",
                    "Added": doc.created_at
                })
            
            st.dataframe(doc_data)
            
            # Add a section to mark documents as processed
            st.subheader("Mark Document as Processed")
            
            unprocessed_docs = [doc for doc in documents if not doc.processed]
            if unprocessed_docs:
                doc_id = st.selectbox(
                    "Select a document to mark as processed:",
                    options=[doc.id for doc in unprocessed_docs],
                    format_func=lambda x: f"ID: {x} - {next((doc.filename for doc in unprocessed_docs if doc.id == x), 'Unknown')}"
                )
                
                if st.button("Mark as Processed"):
                    updated_doc = mark_document_as_processed(doc_id)
                    if updated_doc:
                        st.success(f"Document '{updated_doc.filename}' marked as processed.")
                        st.rerun()
                    else:
                        st.error("Failed to update document status.")
            else:
                st.info("All documents are already processed.")
        else:
            st.info("No documents in the database.")
    except Exception as e:
        st.error(f"Error accessing documents: {e}")

with tab3:
    st.header("System Status")
    
    # Database connection status
    try:
        session = get_db_session()
        db_status = session.execute("SELECT 1").scalar() == 1
        if db_status:
            st.success("✅ Database connection is active")
        else:
            st.error("❌ Database connection is not functioning properly")
    except Exception as e:
        st.error(f"❌ Database error: {e}")
    finally:
        session.close()
    
    # Environment variables (hiding sensitive values)
    st.subheader("Environment Variables")
    env_vars = {
        "DATABASE_URL": "***" if os.environ.get("DATABASE_URL") else "Not set",
        "PGDATABASE": os.environ.get("PGDATABASE", "Not set"),
        "PGHOST": os.environ.get("PGHOST", "Not set"),
        "PGPORT": os.environ.get("PGPORT", "Not set"),
        "PGUSER": "***" if os.environ.get("PGUSER") else "Not set",
        "PGPASSWORD": "***" if os.environ.get("PGPASSWORD") else "Not set",
    }
    
    for key, value in env_vars.items():
        st.text(f"{key}: {value}")
    
    # Application paths
    st.subheader("Application Paths")
    app_paths = {
        "Current directory": os.getcwd(),
        "Data directory": os.path.join(os.getcwd(), "data"),
        "Sample PDFs directory": os.path.join(os.getcwd(), "sample_pdfs"),
        "Vector store directory": os.path.join(os.getcwd(), "simple_index"),
    }
    
    for key, value in app_paths.items():
        exists = os.path.exists(value)
        st.text(f"{key}: {value} {'(exists)' if exists else '(does not exist)'}")