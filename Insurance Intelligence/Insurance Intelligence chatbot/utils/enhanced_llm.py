"""
Enhanced LLM implementation that integrates with LangChain
and provides detailed, conversational insurance chatbot functionality.
"""

from typing import Any, Dict, List, Optional
from langchain.llms.base import LLM
from utils.adaptive_llm import AdaptiveLLM

class EnhancedLLM(LLM):
    """
    An enhanced LLM implementation that provides detailed, conversational responses
    using pre-defined templates and pattern matching to simulate more sophisticated
    LLM behavior.
    """
    
    def __init__(self):
        """Initialize the enhanced LLM with adaptive components."""
        super().__init__()
        self.adaptive_llm = AdaptiveLLM()
        
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any) -> str:
        """
        Process the prompt and generate a detailed, conversational response.
        
        Args:
            prompt: The prompt to respond to
            stop: Optional list of stop sequences
            
        Returns:
            A detailed, conversational string response
        """
        # Extract chat history from kwargs if available
        chat_history = kwargs.get("chat_history", "")
        
        # Format history for the adaptive LLM if provided
        history = []
        if chat_history:
            # Try to parse the chat history from different formats
            if isinstance(chat_history, str):
                # Attempt to split string-based history into turns
                turns = chat_history.split("\n\n")
                for turn in turns:
                    if "Human:" in turn or "User:" in turn:
                        user_msg = turn.split(":", 1)[1].strip()
                        history.append({"role": "user", "content": user_msg})
                    elif "AI:" in turn or "Assistant:" in turn:
                        ai_msg = turn.split(":", 1)[1].strip()
                        history.append({"role": "assistant", "content": ai_msg})
            elif isinstance(chat_history, list):
                # Direct list format
                history = chat_history
        
        # Generate response using the adaptive LLM
        response = self.adaptive_llm(prompt, history=history)
        
        return response
    
    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "enhanced-conversational-llm"


def get_llm():
    """
    Initialize and return an enhanced LLM model that provides detailed, conversational responses.
    
    Returns:
        An initialized enhanced LLM
    """
    return EnhancedLLM()