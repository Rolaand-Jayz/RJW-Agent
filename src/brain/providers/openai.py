"""
OpenAI Provider Implementation.

Integrates with OpenAI's GPT models using the official Python SDK.
"""

import os
import json
from typing import Dict, Any, Optional

from openai import OpenAI

from ..interface import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4", **kwargs):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key (or use OPENAI_API_KEY env var)
            model: Model identifier (default: gpt-4)
                  Note: gpt-4 is powerful but more expensive. Consider using
                  'gpt-3.5-turbo' for cost-sensitive applications.
            **kwargs: Additional OpenAI client options
        """
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key, **kwargs)

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """
        Generate text completion using OpenAI Chat Completions API.

        Args:
            prompt: User prompt/input text
            system_prompt: Optional system instructions
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=temperature, max_tokens=max_tokens
        )

        return response.choices[0].message.content

    def generate_json(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Generate structured JSON response using OpenAI's JSON mode.

        Args:
            prompt: User prompt/input text
            schema: JSON schema for response format
            system_prompt: Optional system instructions
            temperature: Sampling temperature (0.0-1.0)

        Returns:
            Structured JSON response as dictionary

        Raises:
            ValueError: If response is invalid or cannot be parsed
        """
        messages = []

        # Enhance system prompt with JSON instructions
        json_instruction = (
            f"You must respond with valid JSON that matches this schema: {json.dumps(schema)}"
        )

        if system_prompt:
            enhanced_system = f"{system_prompt}\n\n{json_instruction}"
        else:
            enhanced_system = json_instruction

        messages.append({"role": "system", "content": enhanced_system})

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=temperature,
        )

        # Validate response
        if not response.choices or not response.choices[0].message.content:
            raise ValueError("OpenAI returned empty or invalid response")

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response from OpenAI: {e}") from e
