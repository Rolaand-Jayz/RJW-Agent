"""
Google Gemini Provider Implementation.

Integrates with Google's Gemini models using the official Python SDK.
"""

import os
import json
from typing import Dict, Any, Optional

import google.generativeai as genai

from ..interface import LLMProvider


class GeminiProvider(LLMProvider):
    """Google Gemini LLM provider implementation."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-pro", **kwargs):
        """
        Initialize Gemini provider.

        Args:
            api_key: Google API key (or use GOOGLE_API_KEY env var)
            model: Model identifier (default: gemini-pro)
            **kwargs: Additional Gemini options
        """
        self.model_name = model
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")

        # Configure the API
        genai.configure(api_key=self.api_key)

        # Create the model instance
        self.model = genai.GenerativeModel(self.model_name)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """
        Generate text completion using Gemini.

        Args:
            prompt: User prompt/input text
            system_prompt: Optional system instructions
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response
        """
        # Combine system prompt with user prompt if provided
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        # Generate content with configuration
        generation_config = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        response = self.model.generate_content(full_prompt, generation_config=generation_config)

        # Gemini returns response object with .text attribute
        return response.text

    def generate_json(
        self, prompt: str, schema: Dict[str, Any], system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate structured JSON response using Gemini.

        Args:
            prompt: User prompt/input text
            schema: JSON schema for response format
            system_prompt: Optional system instructions

        Returns:
            Structured JSON response as dictionary

        Raises:
            ValueError: If response is invalid or cannot be parsed
        """
        # Enhance prompt with JSON instructions
        json_instruction = (
            f"Respond with valid JSON that matches this schema: {json.dumps(schema)}\n\n"
        )
        enhanced_prompt = f"{json_instruction}{prompt}"

        # Combine with system prompt if provided
        if system_prompt:
            enhanced_prompt = f"{system_prompt}\n\n{enhanced_prompt}"

        response = self.model.generate_content(enhanced_prompt)

        # Validate response
        if not hasattr(response, "text") or not response.text:
            raise ValueError("Gemini returned empty or invalid response")

        # Parse the JSON from response text
        try:
            return json.loads(response.text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response from Gemini: {e}") from e
