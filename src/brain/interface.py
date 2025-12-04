"""
LLM Provider Interface.

Defines the abstract base class for all LLM providers using the Strategy Pattern.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.

    All LLM provider implementations must inherit from this class and implement
    the abstract methods: generate() and generate_json().
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """
        Generate text completion from prompt.

        Args:
            prompt: User prompt/input text
            system_prompt: Optional system instructions for the LLM
            temperature: Sampling temperature (0.0-1.0), higher = more random
            max_tokens: Maximum number of tokens to generate

        Returns:
            Generated text response as a string

        Raises:
            Exception: Provider-specific exceptions for API errors
        """
        pass

    @abstractmethod
    def generate_json(
        self, prompt: str, schema: Dict[str, Any], system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate structured JSON response.

        Args:
            prompt: User prompt/input text
            schema: JSON schema defining the expected response structure
            system_prompt: Optional system instructions for the LLM

        Returns:
            Structured response as a Python dictionary

        Raises:
            Exception: Provider-specific exceptions for API errors
        """
        pass
