"""
Provider Interface for Brain/LLM providers.

Defines the abstract base class that all LLM providers must implement,
enabling a pluggable "Bring Your Own Key" (BYOK) architecture.
"""
from abc import ABC, abstractmethod
from typing import Optional


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    
    All LLM providers must implement this interface to ensure consistent
    behavior across different models (OpenAI, Gemini, VS Code, etc.).
    
    This enables the Strategy Pattern for LLM provider selection.
    """
    
    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text completion from the LLM.
        
        Args:
            prompt: The user prompt/query
            system_prompt: Optional system instructions to guide the model's behavior
            
        Returns:
            Generated text response from the model
            
        Raises:
            Exception: If generation fails (API errors, authentication, etc.)
        """
        pass
    
    @abstractmethod
    def generate_json(self, prompt: str, schema: dict) -> dict:
        """
        Generate structured JSON output from the LLM.
        
        This method enforces JSON output format. The schema parameter describes
        the expected structure but implementations are not required to validate
        against it - it serves primarily as a hint to the LLM.
        
        Args:
            prompt: The user prompt/query requesting structured data
            schema: Dictionary describing the expected JSON structure.
                   Can be a JSON Schema or simplified format (implementation-specific).
                   Used to guide the LLM but not necessarily for validation.
            
        Returns:
            Dictionary containing the structured response
            
        Raises:
            Exception: If generation fails or response is not valid JSON
        """
        pass
