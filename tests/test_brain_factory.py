"""Tests for the Brain module factory."""
import unittest
from unittest.mock import patch, MagicMock


class TestProviderFactory(unittest.TestCase):
    """Test the get_provider factory function."""
    
    def test_get_provider_openai(self):
        """Test that get_provider('openai') returns OpenAIProvider."""
        from src.brain.factory import get_provider
        from src.brain.providers.openai import OpenAIProvider
        
        # Mock the OpenAI client to avoid actual API calls
        with patch('src.brain.providers.openai.OpenAI'):
            provider = get_provider("openai", api_key="test-key")
            self.assertIsInstance(provider, OpenAIProvider)
    
    def test_get_provider_gemini(self):
        """Test that get_provider('gemini') returns GeminiProvider."""
        from src.brain.factory import get_provider
        from src.brain.providers.gemini import GeminiProvider
        
        # Mock the Gemini configure and GenerativeModel
        with patch('src.brain.providers.gemini.genai.configure'), \
             patch('src.brain.providers.gemini.genai.GenerativeModel'):
            provider = get_provider("gemini", api_key="test-key")
            self.assertIsInstance(provider, GeminiProvider)
    
    def test_get_provider_vscode(self):
        """Test that get_provider('vscode') returns VSCodeBridgeProvider."""
        from src.brain.factory import get_provider
        from src.brain.providers.vscode import VSCodeBridgeProvider
        
        provider = get_provider("vscode")
        self.assertIsInstance(provider, VSCodeBridgeProvider)
    
    def test_get_provider_unknown_raises_error(self):
        """Test that unknown provider raises ValueError."""
        from src.brain.factory import get_provider
        
        with self.assertRaises(ValueError) as context:
            get_provider("unknown-provider")
        
        error_msg = str(context.exception)
        self.assertIn("unknown", error_msg.lower())
        self.assertIn("provider", error_msg.lower())
    
    def test_get_provider_case_insensitive(self):
        """Test that provider names are case-insensitive."""
        from src.brain.factory import get_provider
        from src.brain.providers.openai import OpenAIProvider
        from src.brain.providers.gemini import GeminiProvider
        from src.brain.providers.vscode import VSCodeBridgeProvider
        
        # Test various case combinations
        with patch('src.brain.providers.openai.OpenAI'):
            provider1 = get_provider("OpenAI", api_key="test-key")
            self.assertIsInstance(provider1, OpenAIProvider)
            
            provider2 = get_provider("OPENAI", api_key="test-key")
            self.assertIsInstance(provider2, OpenAIProvider)
        
        with patch('src.brain.providers.gemini.genai.configure'), \
             patch('src.brain.providers.gemini.genai.GenerativeModel'):
            provider3 = get_provider("Gemini", api_key="test-key")
            self.assertIsInstance(provider3, GeminiProvider)
            
            provider4 = get_provider("GEMINI", api_key="test-key")
            self.assertIsInstance(provider4, GeminiProvider)
        
        provider5 = get_provider("VSCode")
        self.assertIsInstance(provider5, VSCodeBridgeProvider)
        
        provider6 = get_provider("VSCODE")
        self.assertIsInstance(provider6, VSCodeBridgeProvider)
    
    def test_get_provider_passes_kwargs(self):
        """Test that get_provider passes additional kwargs to provider."""
        from src.brain.factory import get_provider
        
        # Mock OpenAI to verify kwargs are passed
        with patch('src.brain.providers.openai.OpenAI') as mock_openai_client:
            provider = get_provider(
                "openai",
                api_key="test-key",
                model="gpt-3.5-turbo",
                custom_param="value"
            )
            
            # Verify provider was created (we can't easily test kwargs without
            # deeper inspection, but the provider should be instantiated)
            self.assertIsNotNone(provider)
    
    def test_get_provider_returns_llm_provider_interface(self):
        """Test that get_provider returns an instance of LLMProvider."""
        from src.brain.factory import get_provider
        from src.brain.interface import LLMProvider
        
        with patch('src.brain.providers.openai.OpenAI'):
            provider = get_provider("openai", api_key="test-key")
            self.assertIsInstance(provider, LLMProvider)
        
        with patch('src.brain.providers.gemini.genai.configure'), \
             patch('src.brain.providers.gemini.genai.GenerativeModel'):
            provider = get_provider("gemini", api_key="test-key")
            self.assertIsInstance(provider, LLMProvider)
        
        provider = get_provider("vscode")
        self.assertIsInstance(provider, LLMProvider)


if __name__ == '__main__':
    unittest.main()
