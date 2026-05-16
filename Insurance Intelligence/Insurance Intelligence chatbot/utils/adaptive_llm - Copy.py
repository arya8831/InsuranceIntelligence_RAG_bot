"""
Adaptive LLM implementation with natural language processing capabilities.

This module provides an enhanced LLM that can:
1. Learn from conversations to improve responses
2. Detect patterns in questions and provide appropriate responses
3. Maintain context across conversation turns
4. Generate more human-like, conversational responses
"""

import re
import random
import json
from typing import Any, List, Dict, Optional, Tuple
from utils.insurance_responses import get_insurance_response

class AdaptiveLLM:
    """
    An adaptive LLM that learns from conversations and provides more natural responses.
    """
    
    def __init__(self):
        """Initialize the adaptive LLM with conversation memory and response patterns."""
        # Conversation memory to track topics and learn from interactions
        self.conversation_memory = {
            "recent_topics": [],
            "question_patterns": {},
            "response_patterns": {},
            "conversation_turns": 0
        }
        
        # Natural language patterns for more human-like responses
        self.human_patterns = {
            "greetings": [
                "Hello! I'm happy to help with your insurance questions today.",
                "Hi there! I'd be glad to assist you with that.",
                "Good day! I'm here to help with your insurance needs."
            ],
            "transitions": [
                "Now, regarding your question about {}...",
                "Let me address your question about {}...",
                "About your question on {}..."
            ],
            "thinking": [
                "That's an interesting question about {}. Let me think...",
                "Regarding {}, let me provide you with a detailed answer...",
                "When it comes to {}, there are several important aspects to consider..."
            ],
            "acknowledgments": [
                "I understand you're asking about {}.",
                "You're interested in learning about {}, correct?",
                "I see you want to know more about {}."
            ],
            "continuations": [
                "Would you like to know more about this topic?",
                "Is there anything specific about this you'd like me to elaborate on?",
                "Do you have any follow-up questions about this?"
            ],
            "personal_touches": [
                "Many customers find this aspect of insurance particularly important.",
                "I've helped many people with similar questions about their insurance needs.",
                "This is actually a common concern among insurance customers."
            ],
            "reflections": [
                "Looking back at our conversation, I think I understand your insurance needs better now.",
                "Based on what we've discussed so far, it seems your main concern is about {}.",
                "From our conversation, I gather that you're primarily interested in {}."
            ]
        }
        
        # Learning parameters
        self.learning_rate = 0.1
        self.context_window = 5  # Number of turns to maintain in active context
        self.question_types = [
            "what", "how", "why", "when", "where", "who", "can", "should", "is", "are", "do", "does"
        ]
        
        # Initialize response templates memory
        self.load_response_templates()
    
    def load_response_templates(self):
        """Load pre-defined response templates and patterns."""
        # These would typically be loaded from a file, but for simplicity
        # we'll define them here for the insurance domain
        self.response_templates = {
            "greeting": [
                "Hello! I'm your insurance assistant. How can I help you today?",
                "Hi there! I'm here to answer your insurance questions. What would you like to know?",
                "Welcome! I'm ready to help with any insurance information you need."
            ],
            "farewell": [
                "Thank you for chatting with me today. If you have more insurance questions in the future, don't hesitate to ask!",
                "I'm glad I could help with your insurance needs. Have a great day!",
                "It was a pleasure assisting you with your insurance questions. Feel free to reach out anytime!"
            ],
            "clarification": [
                "I'd like to make sure I understand your question correctly. Are you asking about {} insurance?",
                "To better assist you, could you clarify if you're interested in {} specifically?",
                "Let me make sure I understand - you're asking about {}, correct?"
            ],
            "transition": [
                "Now, let's talk about {}.",
                "Moving on to your question about {}.",
                "Regarding {},"
            ],
            "detailed_answer": [
                "Here's what you need to know about {}: {}",
                "Regarding {}, the important details are: {}",
                "When it comes to {}, here's a comprehensive explanation: {}"
            ],
            "not_understood": [
                "I'm not quite sure I understood your question. Could you rephrase it?",
                "I'd like to help, but I'm having trouble understanding your question. Could you try asking in a different way?",
                "I apologize, but I'm not sure what you're asking. Could you provide more details?"
            ]
        }
    
    def identify_question_type(self, query: str) -> Tuple[str, List[str]]:
        """
        Identify the type of question and extract key topics.
        
        Args:
            query: The user's question
            
        Returns:
            A tuple with question type and list of key topics
        """
        query = query.lower().strip()
        
        # Check for question words
        question_type = "general"
        for q_type in self.question_types:
            if query.startswith(q_type) or f" {q_type} " in query:
                question_type = q_type
                break
                
        # Extract key topics using basic keyword extraction
        insurance_types = ["auto", "car", "motor", "life", "health", "home", "property", "travel"]
        insurance_aspects = ["coverage", "premium", "deductible", "claim", "policy", "apply", "cost", "quote"]
        
        topics = []
        for word in insurance_types + insurance_aspects:
            if word in query:
                topics.append(word)
                
        return question_type, topics
    
    def generate_human_like_response(self, base_response: str, question_type: str, topics: List[str]) -> str:
        """
        Enhance a base response with human-like elements.
        
        Args:
            base_response: The core information to include
            question_type: The type of question asked
            topics: List of topics identified in the question
            
        Returns:
            Enhanced human-like response
        """
        # Don't modify if base response is very short
        if len(base_response) < 50:
            return base_response
            
        # Extract a short topic description for templates
        topic_str = " and ".join(topics) if topics else "this insurance topic"
        
        # Add a greeting or thinking phrase at the beginning (occasionally)
        response_parts = []
        if random.random() < 0.3:  # 30% chance
            if question_type in ["what", "how"]:
                response_parts.append(random.choice(self.human_patterns["thinking"]).format(topic_str))
            else:
                response_parts.append(random.choice(self.human_patterns["acknowledgments"]).format(topic_str))
                
        # Add the main response content
        response_parts.append(base_response)
        
        # Add a personal touch or continuation prompt (occasionally)
        if random.random() < 0.4:  # 40% chance
            if self.conversation_memory["conversation_turns"] > 2:
                response_parts.append(random.choice(self.human_patterns["personal_touches"]))
            else:
                response_parts.append(random.choice(self.human_patterns["continuations"]))
            
        # Join all parts with appropriate spacing
        return " ".join(response_parts)
    
    def update_conversation_memory(self, query: str, response: str):
        """
        Update the conversation memory with the latest interaction.
        
        Args:
            query: The user's question
            response: The system's response
        """
        # Extract question type and topics
        question_type, topics = self.identify_question_type(query)
        
        # Update recent topics
        for topic in topics:
            if topic not in self.conversation_memory["recent_topics"]:
                self.conversation_memory["recent_topics"] = [topic] + self.conversation_memory["recent_topics"]
                if len(self.conversation_memory["recent_topics"]) > self.context_window:
                    self.conversation_memory["recent_topics"].pop()
        
        # Update conversation turns counter
        self.conversation_memory["conversation_turns"] += 1
        
        # Update question patterns (simple learning mechanism)
        query_pattern = self.extract_pattern(query)
        if query_pattern:
            if query_pattern not in self.conversation_memory["question_patterns"]:
                self.conversation_memory["question_patterns"][query_pattern] = {
                    "count": 1,
                    "topics": topics,
                    "question_type": question_type
                }
            else:
                self.conversation_memory["question_patterns"][query_pattern]["count"] += 1
                
        # Update response patterns (for future learning)
        response_pattern = self.extract_pattern(response, is_response=True)
        if response_pattern:
            if response_pattern not in self.conversation_memory["response_patterns"]:
                self.conversation_memory["response_patterns"][response_pattern] = {
                    "count": 1,
                    "for_question_type": question_type,
                    "for_topics": topics
                }
            else:
                self.conversation_memory["response_patterns"][response_pattern]["count"] += 1
    
    def extract_pattern(self, text: str, is_response: bool = False) -> Optional[str]:
        """
        Extract a simplified pattern from text for learning.
        
        Args:
            text: The text to extract pattern from
            is_response: Whether this is a response (different pattern rules)
            
        Returns:
            A pattern string or None
        """
        # This is a simplified implementation
        # In a real system, this would use NLP techniques like POS tagging
        
        if not text or len(text) < 10:
            return None
            
        # For questions, focus on question structure
        if not is_response:
            # Simplify to question word + key nouns pattern
            words = text.lower().split()
            if len(words) > 3:
                question_words = [w for w in words if w in self.question_types]
                if question_words:
                    return f"{question_words[0]}_QUERY"
                else:
                    return "STATEMENT_QUERY"
            return None
            
        # For responses, focus on structure and length
        else:
            # Very simple pattern based on length and paragraph structure
            if len(text) < 100:
                return "SHORT_RESPONSE"
            elif len(text) < 500:
                return "MEDIUM_RESPONSE"
            else:
                return "DETAILED_RESPONSE"
    
    def extract_context_from_history(self, history):
        """
        Extract contextual information from conversation history.
        
        Args:
            history: List of previous conversation messages
            
        Returns:
            Dictionary of context information
        """
        context = {
            "mentioned_topics": set(),
            "question_count": 0,
            "topic_focus": None,
            "sentiment": "neutral"
        }
        
        # Process the history to extract context
        for i, message in enumerate(history):
            if i % 2 == 0:  # User messages
                text = message.get("content", "").lower()
                
                # Extract topics
                _, topics = self.identify_question_type(text)
                for topic in topics:
                    context["mentioned_topics"].add(topic)
                
                # Count questions
                if any(text.startswith(q) for q in self.question_types) or "?" in text:
                    context["question_count"] += 1
        
        # Determine primary topic focus if any topic appears multiple times
        topic_counts = {}
        for topic in context["mentioned_topics"]:
            topic_counts[topic] = sum(1 for msg in history if msg.get("role") == "user" and topic in msg.get("content", "").lower())
        
        if topic_counts:
            max_topic = max(topic_counts.items(), key=lambda x: x[1])
            if max_topic[1] >= 2:  # Topic mentioned at least twice
                context["topic_focus"] = max_topic[0]
        
        return context
    
    def __call__(self, prompt: str, history=None, **kwargs):
        """
        Generate a response to the user's prompt.
        
        Args:
            prompt: The user's question
            history: Optional conversation history
            
        Returns:
            A conversational response
        """
        prompt = prompt.lower().strip()
        
        # Extract context from history if provided
        context = {}
        if history:
            context = self.extract_context_from_history(history)
        
        # Identify question type and topics
        question_type, topics = self.identify_question_type(prompt)
        
        # Get the specialized response based on insurance domain
        base_response = get_insurance_response(prompt)
        
        # Enhance the response with human-like patterns
        enhanced_response = self.generate_human_like_response(
            base_response, 
            question_type, 
            topics
        )
        
        # Update the conversation memory
        self.update_conversation_memory(prompt, enhanced_response)
        
        return enhanced_response