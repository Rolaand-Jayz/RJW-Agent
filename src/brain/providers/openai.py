"""
OpenAI LLM Provider.

Implements the LLMProvider interface using OpenAI's GPT models.
Requires OPENAI_API_KEY environment variable.
"""
import json
import os
from typing import Optional

from ..interface import LLMProvider


class OpenAIProvider(LLMProvider):
    """
    OpenAI implementation of LLMProvider.
    
    Uses the OpenAI API to generate text completions and structured JSON output.
    Defaults to gpt-4o model for optimal performance.
    
    Attributes:
        model: The OpenAI model to use (default: gpt-4o)
        api_key: OpenAI API key from environment variable
        client: OpenAI client instance
    """
    
    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None):
        """
        Initialize OpenAI provider.
        
        Args:
            model: OpenAI model name (default: gpt-4o)
            api_key: Optional API key override (defaults to OPENAI_API_KEY env var)
            
        Raises:
            ValueError: If API key is not provided or found in environment
        """
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Please set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Import here to avoid requiring openai if not used
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "openai package not installed. Install with: pip install openai"
            )
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text completion using OpenAI.
        
        Args:
            prompt: User prompt/query
            system_prompt: Optional system instructions
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If API call fails
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def generate_json(self, prompt: str, schema: dict) -> dict:
        """
        Generate structured JSON output using OpenAI.
        
        Uses response_format="json_object" to enforce JSON output.
        
        Args:
            prompt: User prompt requesting structured data
            schema: Expected JSON structure description
            
        Returns:
            Dictionary containing structured response
            
        Raises:
            Exception: If API call fails or response is not valid JSON
        """
        # Add schema description to prompt to guide the model
        enhanced_prompt = f"{prompt}\n\nRespond with valid JSON matching this structure:\n{json.dumps(schema, indent=2)}"
        
        messages = [
            {
                "role": "system", 
                "content": "You are a helpful assistant that responds with valid JSON."
            },
            {
                "role": "user",
                "content": enhanced_prompt
            }
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
        
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response: {str(e)}")
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
