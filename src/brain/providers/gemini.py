"""
Google Gemini LLM Provider.

Implements the LLMProvider interface using Google's Gemini models.
Requires GEMINI_API_KEY environment variable.
"""
import json
import os
from typing import Optional

from ..interface import LLMProvider


class GeminiProvider(LLMProvider):
    """
    Google Gemini implementation of LLMProvider.
    
    Uses the Google Generative AI API to generate text completions and structured output.
    Defaults to gemini-1.5-pro model for optimal performance.
    
    Attributes:
        model: The Gemini model to use (default: gemini-1.5-pro)
        api_key: Gemini API key from environment variable
        client: Gemini GenerativeModel instance
    """
    
    def __init__(self, model: str = "gemini-1.5-pro", api_key: Optional[str] = None):
        """
        Initialize Gemini provider.
        
        Args:
            model: Gemini model name (default: gemini-1.5-pro)
            api_key: Optional API key override (defaults to GEMINI_API_KEY env var)
            
        Raises:
            ValueError: If API key is not provided or found in environment
        """
        self.model = model
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Import here to avoid requiring google-generativeai if not used
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
        except ImportError:
            raise ImportError(
                "google-generativeai package not installed. "
                "Install with: pip install google-generativeai"
            )
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text completion using Gemini.
        
        Args:
            prompt: User prompt/query
            system_prompt: Optional system instructions (prepended to prompt)
            
        Returns:
            Generated text response
            
        Raises:
            Exception: If API call fails
        """
        # Gemini handles system instructions differently - prepend to prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        try:
            response = self.client.generate_content(full_prompt)
            return response.text
        
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def generate_json(self, prompt: str, schema: dict) -> dict:
        """
        Generate structured JSON output using Gemini.
        
        Args:
            prompt: User prompt requesting structured data
            schema: Expected JSON structure description
            
        Returns:
            Dictionary containing structured response
            
        Raises:
            Exception: If API call fails or response is not valid JSON
        """
        # Add schema description and JSON request to prompt
        enhanced_prompt = (
            f"{prompt}\n\n"
            f"Respond with ONLY valid JSON matching this structure:\n"
            f"{json.dumps(schema, indent=2)}\n\n"
            f"Do not include any text before or after the JSON."
        )
        
        try:
            response = self.client.generate_content(enhanced_prompt)
            content = response.text.strip()
            
            # Try to extract JSON if wrapped in markdown code blocks
            if content.startswith("```"):
                # Remove markdown code fence (handles language specifier like ```json)
                lines = content.split("\n")
                # Remove first line (opening fence, e.g., "```json")
                lines = lines[1:]
                # Remove last line if it's a closing fence
                if lines and lines[-1].strip().startswith("```"):
                    lines = lines[:-1]
                content = "\n".join(lines).strip()
            
            return json.loads(content)
        
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response: {str(e)}\nContent: {content}")
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
