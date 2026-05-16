import os
import datetime
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Get database URL from environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create declarative base for models
Base = declarative_base()

# Define User model
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user")
    
    def __repr__(self):
        return f"<User id={self.id}, name={self.name}>"

# Define Conversation model
class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(200))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
    
    def __repr__(self):
        return f"<Conversation id={self.id}, title={self.title}>"

# Define Message model
class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    role = Column(String(50))  # 'user' or 'assistant'
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message id={self.id}, role={self.role}>"

# Define Document model
class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255))
    file_path = Column(String(255))
    content_type = Column(String(100))
    processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f"<Document id={self.id}, filename={self.filename}>"

# Create all tables in the database
def initialize_database():
    """
    Initialize the database by creating all tables.
    """
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

# Helper functions for common database operations
def get_db_session():
    """
    Get a new database session.
    
    Returns:
        SQLAlchemy session
    """
    session = SessionLocal()
    try:
        return session
    except Exception as e:
        session.close()
        raise e

def create_user(name, email):
    """
    Create a new user in the database.
    
    Args:
        name: User's name
        email: User's email
        
    Returns:
        Created User object
    """
    session = get_db_session()
    try:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    finally:
        session.close()

def create_conversation(user_id, title="New Conversation"):
    """
    Create a new conversation for a user.
    
    Args:
        user_id: ID of the user
        title: Title of the conversation
        
    Returns:
        Created Conversation object
    """
    session = get_db_session()
    try:
        conversation = Conversation(user_id=user_id, title=title)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation
    finally:
        session.close()

def add_message(conversation_id, role, content):
    """
    Add a new message to a conversation.
    
    Args:
        conversation_id: ID of the conversation
        role: Role of the message sender ('user' or 'assistant')
        content: Content of the message
        
    Returns:
        Created Message object
    """
    session = get_db_session()
    try:
        message = Message(conversation_id=conversation_id, role=role, content=content)
        session.add(message)
        session.commit()
        session.refresh(message)
        return message
    finally:
        session.close()

def get_conversation_messages(conversation_id):
    """
    Get all messages for a conversation.
    
    Args:
        conversation_id: ID of the conversation
        
    Returns:
        List of Message objects
    """
    session = get_db_session()
    try:
        messages = session.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at).all()
        return messages
    finally:
        session.close()

def add_document(filename, file_path, content_type="application/pdf", processed=False):
    """
    Add a document to the database.
    
    Args:
        filename: Name of the file
        file_path: Path to the file
        content_type: MIME type of the file
        processed: Whether the document has been processed
        
    Returns:
        Created Document object
    """
    session = get_db_session()
    try:
        document = Document(
            filename=filename,
            file_path=file_path,
            content_type=content_type,
            processed=processed
        )
        session.add(document)
        session.commit()
        session.refresh(document)
        return document
    finally:
        session.close()

def mark_document_as_processed(document_id):
    """
    Mark a document as processed.
    
    Args:
        document_id: ID of the document
        
    Returns:
        Updated Document object
    """
    session = get_db_session()
    try:
        document = session.query(Document).filter(Document.id == document_id).first()
        if document:
            document.processed = True
            session.commit()
            session.refresh(document)
        return document
    finally:
        session.close()

def get_all_documents():
    """
    Get all documents.
    
    Returns:
        List of Document objects
    """
    session = get_db_session()
    try:
        documents = session.query(Document).all()
        return documents
    finally:
        session.close()

def get_unprocessed_documents():
    """
    Get all unprocessed documents.
    
    Returns:
        List of Document objects that haven't been processed
    """
    session = get_db_session()
    try:
        documents = session.query(Document).filter(Document.processed == False).all()
        return documents
    finally:
        session.close()
        
def get_user_conversations(user_id):
    """
    Get all conversations for a user, ordered by most recent first.
    
    Args:
        user_id: ID of the user
        
    Returns:
        List of Conversation objects
    """
    session = get_db_session()
    try:
        conversations = session.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.created_at.desc()).all()
        return conversations
    finally:
        session.close()