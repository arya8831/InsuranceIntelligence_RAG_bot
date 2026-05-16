import os
import streamlit as st
from utils.document_processor import process_pdf_documents
from utils.vector_store import create_or_load_vector_store
#from utils.llm_utils import get_llm, get_conversation_chain, format_chat_history
from utils.db_utils import (
    initialize_database, create_user, create_conversation, 
    add_message, get_conversation_messages, add_document, 
    mark_document_as_processed, get_all_documents
)

# Page configuration
st.set_page_config(
    page_title="Insurance Policy Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize database
try:
    initialize_database()
except Exception as e:
    st.error(f"Error initializing database: {e}")
    print(f"Error initializing database: {e}")

# Initialize session state variables
if "conversation_chain" not in st.session_state:
    st.session_state.conversation_chain = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False
    
if "user_id" not in st.session_state:
    # Create a default user for demonstration
    try:
        user = create_user("Demo User", "demo@example.com")
        st.session_state.user_id = user.id
        print(f"Created demo user with ID: {user.id}")
    except Exception as e:
        # If error is duplicate user, try to get existing user
        from sqlalchemy.exc import IntegrityError # type: ignore
        if isinstance(e, IntegrityError) and "duplicate key" in str(e):
            from utils.db_utils import get_db_session, User
            session = get_db_session()
            user = session.query(User).filter(User.email == "demo@example.com").first()
            if user:
                st.session_state.user_id = user.id
                print(f"Using existing user with ID: {user.id}")
                session.close()
            else:
                st.session_state.user_id = None
                print(f"Could not find existing user")
        else:
            st.session_state.user_id = None
            print(f"Error creating user: {e}")
        
if "conversation_id" not in st.session_state:
    # Create a default conversation for the user
    if st.session_state.user_id:
        try:
            conversation = create_conversation(st.session_state.user_id, "Insurance Policy Chat")
            st.session_state.conversation_id = conversation.id
            print(f"Created conversation with ID: {conversation.id}")
        except Exception as e:
            st.session_state.conversation_id = None
            print(f"Error creating conversation: {e}")
    else:
        st.session_state.conversation_id = None

# Initialize messages - load from database if conversation exists
if "messages" not in st.session_state:
    st.session_state.messages = []
    
    # If we have a conversation ID, load messages from database
    if st.session_state.conversation_id:
        try:
            db_messages = get_conversation_messages(st.session_state.conversation_id)
            
            # Convert database messages to the format used in session state
            for msg in db_messages:
                st.session_state.messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            print(f"Loaded {len(db_messages)} messages from database for conversation {st.session_state.conversation_id}")
        except Exception as e:
            print(f"Error loading messages from database: {e}")
            # Initialize with empty messages if loading fails
            st.session_state.messages = []
            
# If messages were loaded and we have vector store, mark documents as processed
if len(st.session_state.messages) > 0 and st.session_state.vector_store is None:
    try:
        from utils.vector_store import create_or_load_vector_store
        # Try to load existing vector store
        example_docs = []
        st.session_state.vector_store = create_or_load_vector_store(example_docs)
        # If successful, mark documents as processed
        if st.session_state.vector_store:
            st.session_state.documents_processed = True
            print("Loaded existing vector store for continued conversation")
    except Exception as e:
        print(f"Could not load vector store: {e}")
        # Will need to process documents in the UI

# Function to create a sample insurance policy text file
def create_sample_policy():
    if not os.path.exists("data"):
        os.makedirs("data")
    
    sample_policy_path = "data/example_insurance_policy.pdf"
    
    # Only create if it doesn't already exist as a real PDF
    if not os.path.exists(sample_policy_path) or os.path.getsize(sample_policy_path) < 1000:
        sample_text = """# Sample Auto Insurance Policy

## COVERAGE SUMMARY
Policy Number: AUTO-12345-XYZ
Effective Date: January 1, 2025
Expiration Date: January 1, 2026

Policyholder: John Smith
Address: 123 Main Street, Anytown, USA 12345

## COVERAGE DETAILS

### Liability Coverage
- Bodily Injury: $100,000 per person / $300,000 per accident
- Property Damage: $50,000 per accident
- Medical Payments: $5,000 per person

### Vehicle Coverage
- Comprehensive Deductible: $500
- Collision Deductible: $1,000
- Uninsured/Underinsured Motorist: $100,000 per person / $300,000 per accident

### Additional Benefits
- Roadside Assistance: Included
- Rental Car Reimbursement: $30 per day, up to 30 days
- Glass Coverage: $0 deductible

## CLAIM PROCESS
1. Report the incident immediately by calling our 24/7 claims hotline at 1-800-555-CLAIM
2. Provide all required information about the incident, including:
   - Date, time, and location
   - Vehicles and parties involved
   - Police report number (if applicable)
3. A claims adjuster will contact you within 24 hours
4. Inspection of damages will be scheduled
5. Claim resolution typically occurs within 7-10 business days

## POLICY EXCLUSIONS
This policy does not cover:
- Intentional damage
- Racing or speed contests
- Using the vehicle for commercial purposes
- Damage occurring outside the United States and Canada
- Driving under the influence of alcohol or drugs

## PREMIUM INFORMATION
Annual Premium: $1,200
Payment Schedule: Monthly payments of $100
Discount Applied: Safe Driver Discount (15%)

## CANCELLATION POLICY
You may cancel this policy at any time. Refunds for unused premium will be calculated on a pro-rata basis. A cancellation fee of $50 may apply.

The insurer may cancel this policy for non-payment of premium with 10 days written notice, or for other reasons with 30 days written notice."""

        # Create a text file with the sample policy
        # In a real scenario, this would be a PDF, but for demo purposes we use a text file
        with open("data/example_insurance_policy.txt", "w") as f:
            f.write(sample_text)
        
        # Let the user know we're using a demo text file instead of a PDF
        print("Created sample insurance policy text file")

# Create sample policy if needed
create_sample_policy()

# Sidebar for document uploading and processing
with st.sidebar:
    st.title("Insurance Policy Assistant")
    st.markdown("---")
    
    st.subheader("Upload Policy Documents")
    uploaded_files = st.file_uploader(
        "Upload insurance policy documents",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )
    
    # Option to use example documents
    use_example = st.checkbox("Use example insurance documents", value=False)
    
    if st.button("Process Documents"):
        with st.spinner("Processing documents..."):
            # Create sample_pdfs directory if it doesn't exist
            if not os.path.exists("sample_pdfs"):
                os.makedirs("sample_pdfs")
            
            # Save uploaded files to sample_pdfs directory
            if uploaded_files:
                for file in uploaded_files:
                    file_path = f"sample_pdfs/{file.name}"
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
                    
                    # Add the document to the database
                    try:
                        content_type = "application/pdf" if file.name.lower().endswith('.pdf') else "text/plain"
                        add_document(file.name, file_path, content_type=content_type, processed=False)
                        print(f"Added document {file.name} to database")
                    except Exception as e:
                        print(f"Error adding document to database: {e}")
                
                # Process the uploaded documents
                documents = process_pdf_documents("sample_pdfs")
                if documents:
                    # Create or load vector store
                    st.session_state.vector_store = create_or_load_vector_store(documents)
                    st.session_state.documents_processed = True
                    
                    # Mark all documents as processed
                    try:
                        for doc in get_all_documents():
                            if not doc.processed:
                                mark_document_as_processed(doc.id)
                                print(f"Marked document {doc.filename} as processed")
                    except Exception as e:
                        print(f"Error updating document status: {e}")
                    
                    st.success(f"✅ {len(documents)} documents processed successfully!")
                else:
                    st.error("No valid documents found.")
            
            # Use example documents if selected
            elif use_example:
                # First, add the sample document to the database if it doesn't exist
                try:
                    sample_path = "data/example_insurance_policy.txt"
                    # Check if this document is already in the database
                    all_docs = get_all_documents()
                    existing_doc = next((doc for doc in all_docs if doc.file_path == sample_path), None)
                    
                    if not existing_doc:
                        add_document("example_insurance_policy.txt", sample_path, content_type="text/plain", processed=False)
                        print(f"Added example document to database")
                except Exception as e:
                    print(f"Error with example document in database: {e}")
                
                # Process the example documents
                example_docs = process_pdf_documents("data")
                if example_docs:
                    st.session_state.vector_store = create_or_load_vector_store(example_docs)
                    st.session_state.documents_processed = True
                    
                    # Mark the example document as processed
                    try:
                        for doc in get_all_documents():
                            if not doc.processed and "example" in doc.filename.lower():
                                mark_document_as_processed(doc.id)
                                print(f"Marked example document {doc.filename} as processed")
                    except Exception as e:
                        print(f"Error updating document status: {e}")
                    
                    st.success(f"✅ {len(example_docs)} example documents processed successfully!")
                else:
                    st.error("No example documents found.")
            else:
                st.error("Please upload documents or use the example documents.")
    
    st.markdown("---")
    
    # Add conversation history selector
    if st.session_state.user_id:
        st.subheader("Previous Conversations")
        try:
            from utils.db_utils import get_user_conversations, get_conversation_messages
            
            # Get all user conversations
            user_conversations = get_user_conversations(st.session_state.user_id)
            
            if user_conversations:
                # Format conversation options with date and title
                conversation_options = {}
                for conv in user_conversations:
                    # Format date nicely
                    date_str = conv.created_at.strftime("%m/%d/%Y %I:%M %p")
                    # Create a display name that includes date and title
                    display_name = f"{date_str} - {conv.title}"
                    # Use conversation ID as the value
                    conversation_options[display_name] = conv.id
                
                # Add a "Current conversation" option if we have one
                current_id = st.session_state.conversation_id
                current_conv = next((c for c in user_conversations if c.id == current_id), None)
                if current_conv:
                    current_date = current_conv.created_at.strftime("%m/%d/%Y %I:%M %p")
                    current_name = f"Current: {current_date} - {current_conv.title}"
                else:
                    current_name = "Current Conversation"
                
                # Convert to list for the selectbox with current conversation first
                conversation_items = list(conversation_options.items())
                
                # Create the selectbox with conversation options
                selected_conv = st.selectbox(
                    "Switch to a previous conversation:",
                    options=[current_name] + [name for name, _ in conversation_items],
                    index=0
                )
                
                # If user selected a different conversation
                if selected_conv != current_name and selected_conv in [name for name, _ in conversation_items]:
                    # Find the conversation ID for the selected name
                    selected_id = next(id for name, id in conversation_items if name == selected_conv)
                    
                    # Only switch if different from current
                    if selected_id != st.session_state.conversation_id:
                        # Update conversation ID in session state
                        st.session_state.conversation_id = selected_id
                        
                        # Load messages for the selected conversation
                        db_messages = get_conversation_messages(selected_id)
                        
                        # Update messages in session state
                        st.session_state.messages = [
                            {"role": msg.role, "content": msg.content}
                            for msg in db_messages
                        ]
                        
                        st.success(f"Switched to conversation: {selected_conv}")
                        st.rerun()
            else:
                st.info("No previous conversations found")
                
        except Exception as e:
            st.error(f"Error loading conversations: {str(e)}")
            print(f"Error in conversation selector: {e}")
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This assistant helps answer questions about insurance policies using the
    information from the uploaded policy documents.
    
    Upload your insurance policy PDFs and ask questions to get accurate information
    about coverage, terms, and claims.
    
    Previous conversations are saved automatically and can be accessed from the
    sidebar menu.
    """)

# Main content area
st.title("Insurance Policy Information Chatbot")

# Add a small link to the admin page
st.markdown(
    '<div style="position: absolute; top: 0.5rem; right: 1rem;"><a href="/admin" target="_self">Admin Panel</a></div>', 
    unsafe_allow_html=True
)

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("Ask me about your insurance policy..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Store the message in the database if conversation_id exists
    if st.session_state.conversation_id:
        try:
            add_message(st.session_state.conversation_id, "user", prompt)
            print(f"Stored user message in database")
        except Exception as e:
            print(f"Error storing message in database: {e}")
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Check if documents have been processed
    if not st.session_state.documents_processed:
        with st.chat_message("assistant"):
            st.warning("Please upload and process insurance policy documents first.")
            response_text = "Please upload and process insurance policy documents first."
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_text
            })
            
            # Store assistant response in database
            if st.session_state.conversation_id:
                try:
                    add_message(st.session_state.conversation_id, "assistant", response_text)
                    print(f"Stored assistant message in database")
                except Exception as e:
                    print(f"Error storing message in database: {e}")
    else:
        # Initialize the conversation chain if not already done
        if st.session_state.conversation_chain is None:
            llm = get_llm()
            st.session_state.conversation_chain = get_conversation_chain(
                llm, 
                st.session_state.vector_store
            )
        
        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                # Format chat history for the chain
                formatted_history = format_chat_history(st.session_state.messages[:-1])  # Exclude current message
                
                # Get response from conversation chain
                response = st.session_state.conversation_chain({
                    "question": prompt, 
                    "chat_history": formatted_history
                })
                
                # Extract the answer
                answer = response.get("answer", "I couldn't find an answer to that question based on the provided documents.")
                
                # Check if a source document was referenced
                source_documents = response.get("source_documents", [])
                
                # Format the final response
                if source_documents:
                    source_info = "\n\n**Sources:**\n"
                    for i, doc in enumerate(source_documents[:3], 1):  # Limit to first 3 sources
                        source = doc.metadata.get("source", "Unknown source")
                        page = doc.metadata.get("page", "Unknown page")
                        source_info += f"{i}. {os.path.basename(source)}, Page {page}\n"
                    
                    final_response = f"{answer}\n{source_info}"
                else:
                    # Fallback mechanism for when no sources are found
                    if "I don't know" in answer or "I couldn't find" in answer:
                        final_response = (
                            f"{answer}\n\n"
                            "I couldn't find specific information about this in the policy documents. "
                            "For complex questions like this, you may want to contact your insurance agent or customer service representative."
                        )
                    else:
                        final_response = answer
                
                # Display the answer
                message_placeholder.markdown(final_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": final_response
                })
                
                # Store assistant response in database
                if st.session_state.conversation_id:
                    try:
                        add_message(st.session_state.conversation_id, "assistant", final_response)
                        print(f"Stored assistant response in database")
                    except Exception as e:
                        print(f"Error storing message in database: {e}")
                
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                message_placeholder.error(error_message)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message
                })
                
                # Store error message in database
                if st.session_state.conversation_id:
                    try:
                        add_message(st.session_state.conversation_id, "assistant", error_message)
                        print(f"Stored error message in database")
                    except Exception as e:
                        print(f"Error storing message in database: {e}")

# Conversation management buttons
if st.session_state.messages and len(st.session_state.messages) > 0:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear Conversation", type="primary"):
            # Clear the conversation history, but don't delete from database
            st.session_state.messages = []
            st.rerun()
    
    with col2:
        if st.button("Start New Conversation", type="secondary"):
            # Clear the current conversation
            st.session_state.messages = []
            
            # Create a new conversation in the database
            if st.session_state.user_id:
                try:
                    import datetime
                    # Create a new conversation with timestamp
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    new_title = f"Insurance Chat - {timestamp}"
                    conversation = create_conversation(st.session_state.user_id, new_title)
                    st.session_state.conversation_id = conversation.id
                    print(f"Created new conversation with ID: {conversation.id}")
                except Exception as e:
                    print(f"Error creating new conversation: {e}")
            
            st.rerun()
