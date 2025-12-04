"""Tests for the Brain/LLM provider module."""
import json
import os
import sys
import unittest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Mock the external dependencies before importing our modules
sys.modules['openai'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['tavily'] = MagicMock()

from src.brain.factory import get_provider, list_providers, get_default_provider
from src.brain.interface import LLMProvider
from src.brain.providers.openai import OpenAIProvider
from src.brain.providers.gemini import GeminiProvider
from src.brain.providers.vscode_bridge import VSCodeBridgeProvider


class TestFactory(unittest.TestCase):
    """Test the provider factory functions."""
    
    def test_list_providers(self):
        """Test listing available providers."""
        providers = list_providers()
        self.assertIn('openai', providers)
        self.assertIn('gemini', providers)
        self.assertIn('vscode', providers)
        self.assertEqual(len(providers), 3)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_get_default_provider_without_env(self):
        """Test default provider when no env var is set."""
        default = get_default_provider()
        self.assertEqual(default, 'openai')
    
    @patch.dict(os.environ, {'RJW_PROVIDER': 'gemini'})
    def test_get_default_provider_with_env(self):
        """Test default provider respects env var."""
        default = get_default_provider()
        self.assertEqual(default, 'gemini')
    
    def test_get_provider_invalid_name(self):
        """Test error handling for invalid provider name."""
        with self.assertRaises(ValueError) as context:
            get_provider('invalid_provider')
        self.assertIn('Unknown provider', str(context.exception))
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key-123'})
    def test_get_provider_openai(self):
        """Test getting OpenAI provider."""
        with patch('openai.OpenAI'):
            provider = get_provider('openai')
            self.assertIsInstance(provider, OpenAIProvider)
            self.assertEqual(provider.model, 'gpt-4o')
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key-456'})
    def test_get_provider_gemini(self):
        """Test getting Gemini provider."""
        with patch('google.generativeai.configure'), \
             patch('google.generativeai.GenerativeModel'):
            provider = get_provider('gemini')
            self.assertIsInstance(provider, GeminiProvider)
            self.assertEqual(provider.model, 'gemini-1.5-pro')
    
    def test_get_provider_vscode(self):
        """Test getting VS Code Bridge provider."""
        provider = get_provider('vscode')
        self.assertIsInstance(provider, VSCodeBridgeProvider)
    
    @patch.dict(os.environ, {'RJW_PROVIDER': 'gemini', 'GEMINI_API_KEY': 'test-key'})
    def test_get_provider_uses_env_var(self):
        """Test provider selection from environment variable."""
        with patch('google.generativeai.configure'), \
             patch('google.generativeai.GenerativeModel'):
            provider = get_provider()  # No provider name specified
            self.assertIsInstance(provider, GeminiProvider)


class TestOpenAIProvider(unittest.TestCase):
    """Test OpenAI provider implementation."""
    
    def test_init_without_api_key(self):
        """Test initialization fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                OpenAIProvider()
            self.assertIn('API key not found', str(context.exception))
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_init_with_env_api_key(self):
        """Test initialization with API key from environment."""
        with patch('openai.OpenAI') as mock_openai_class:
            provider = OpenAIProvider()
            self.assertEqual(provider.api_key, 'test-key')
            mock_openai_class.assert_called_once_with(api_key='test-key')
    
    def test_init_with_explicit_api_key(self):
        """Test initialization with explicitly provided API key."""
        with patch('openai.OpenAI') as mock_openai_class:
            provider = OpenAIProvider(api_key='explicit-key')
            self.assertEqual(provider.api_key, 'explicit-key')
            mock_openai_class.assert_called_once_with(api_key='explicit-key')
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_generate_text(self):
        """Test text generation."""
        with patch('openai.OpenAI') as mock_openai_class:
            # Setup mock response
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Generated response"
            mock_client.chat.completions.create.return_value = mock_response
            
            # Test generation
            provider = OpenAIProvider()
            result = provider.generate("Test prompt")
            
            self.assertEqual(result, "Generated response")
            mock_client.chat.completions.create.assert_called_once()
            call_args = mock_client.chat.completions.create.call_args
            self.assertIn('messages', call_args.kwargs)
            self.assertEqual(call_args.kwargs['model'], 'gpt-4o')
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_generate_with_system_prompt(self):
        """Test text generation with system prompt."""
        with patch('openai.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Response"
            mock_client.chat.completions.create.return_value = mock_response
            
            provider = OpenAIProvider()
            provider.generate("Test prompt", system_prompt="Be helpful")
            
            call_args = mock_client.chat.completions.create.call_args
            messages = call_args.kwargs['messages']
            self.assertEqual(len(messages), 2)
            self.assertEqual(messages[0]['role'], 'system')
            self.assertEqual(messages[0]['content'], 'Be helpful')
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_generate_json(self):
        """Test JSON generation."""
        with patch('openai.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = '{"result": "data"}'
            mock_client.chat.completions.create.return_value = mock_response
            
            provider = OpenAIProvider()
            schema = {"type": "object", "properties": {"result": {"type": "string"}}}
            result = provider.generate_json("Test prompt", schema)
            
            self.assertEqual(result, {"result": "data"})
            call_args = mock_client.chat.completions.create.call_args
            self.assertEqual(call_args.kwargs['response_format'], {"type": "json_object"})
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_generate_json_invalid_response(self):
        """Test JSON generation with invalid JSON response."""
        with patch('openai.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = 'not valid json'
            mock_client.chat.completions.create.return_value = mock_response
            
            provider = OpenAIProvider()
            schema = {"type": "object"}
            with self.assertRaises(Exception) as context:
                provider.generate_json("Test prompt", schema)
            self.assertIn('Failed to parse JSON', str(context.exception))


class TestGeminiProvider(unittest.TestCase):
    """Test Gemini provider implementation."""
    
    def test_init_without_api_key(self):
        """Test initialization fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as context:
                GeminiProvider()
            self.assertIn('API key not found', str(context.exception))
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    def test_init_with_api_key(self):
        """Test initialization with API key."""
        import google.generativeai as genai
        with patch.object(genai, 'configure') as mock_configure, \
             patch.object(genai, 'GenerativeModel'):
            provider = GeminiProvider()
            self.assertEqual(provider.api_key, 'test-key')
            mock_configure.assert_called_once_with(api_key='test-key')
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    def test_generate_text(self):
        """Test text generation."""
        import google.generativeai as genai
        with patch.object(genai, 'configure'), \
             patch.object(genai, 'GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model
            mock_response = MagicMock()
            mock_response.text = "Generated response"
            mock_model.generate_content.return_value = mock_response
            
            provider = GeminiProvider()
            result = provider.generate("Test prompt")
            
            self.assertEqual(result, "Generated response")
            mock_model.generate_content.assert_called_once_with("Test prompt")
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    def test_generate_with_system_prompt(self):
        """Test text generation with system prompt."""
        import google.generativeai as genai
        with patch.object(genai, 'configure'), \
             patch.object(genai, 'GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model
            mock_response = MagicMock()
            mock_response.text = "Response"
            mock_model.generate_content.return_value = mock_response
            
            provider = GeminiProvider()
            provider.generate("User prompt", system_prompt="System instructions")
            
            # Gemini prepends system prompt to user prompt
            mock_model.generate_content.assert_called_once()
            call_args = mock_model.generate_content.call_args[0][0]
            self.assertIn("System instructions", call_args)
            self.assertIn("User prompt", call_args)
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    def test_generate_json(self):
        """Test JSON generation."""
        import google.generativeai as genai
        with patch.object(genai, 'configure'), \
             patch.object(genai, 'GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model
            mock_response = MagicMock()
            mock_response.text = '{"result": "data"}'
            mock_model.generate_content.return_value = mock_response
            
            provider = GeminiProvider()
            schema = {"type": "object"}
            result = provider.generate_json("Test prompt", schema)
            
            self.assertEqual(result, {"result": "data"})
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    def test_generate_json_with_markdown_fence(self):
        """Test JSON extraction from markdown code fence."""
        import google.generativeai as genai
        with patch.object(genai, 'configure'), \
             patch.object(genai, 'GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model
            mock_response = MagicMock()
            mock_response.text = '```json\n{"result": "data"}\n```'
            mock_model.generate_content.return_value = mock_response
            
            provider = GeminiProvider()
            schema = {"type": "object"}
            result = provider.generate_json("Test prompt", schema)
            
            self.assertEqual(result, {"result": "data"})
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    def test_generate_json_with_language_specifier(self):
        """Test JSON extraction with language specifier in fence."""
        import google.generativeai as genai
        with patch.object(genai, 'configure'), \
             patch.object(genai, 'GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model
            mock_response = MagicMock()
            mock_response.text = '```javascript\n{"result": "data"}\n```'
            mock_model.generate_content.return_value = mock_response
            
            provider = GeminiProvider()
            result = provider.generate_json("Test prompt", {})
            
            self.assertEqual(result, {"result": "data"})


class TestVSCodeBridgeProvider(unittest.TestCase):
    """Test VS Code Bridge provider implementation."""
    
    def test_init(self):
        """Test initialization."""
        provider = VSCodeBridgeProvider()
        self.assertEqual(provider.timeout, 30)
        
        provider_custom = VSCodeBridgeProvider(timeout=60)
        self.assertEqual(provider_custom.timeout, 60)
    
    @patch('sys.stdin', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('select.select')
    def test_generate_text(self, mock_select, mock_stdout, mock_stdin):
        """Test text generation via bridge protocol."""
        # Setup mock stdin to return response
        response = '[RESPONSE_LM_GENERATION] {"content": "Generated response"}\n'
        mock_stdin.return_value = response
        mock_stdin.readline = Mock(return_value=response)
        
        # Mock select to indicate stdin is ready
        mock_select.return_value = ([True], [], [])
        
        provider = VSCodeBridgeProvider()
        
        with patch('sys.stdin.readline', return_value=response):
            result = provider.generate("Test prompt")
        
        self.assertEqual(result, "Generated response")
    
    @patch('sys.stdin', new_callable=StringIO)
    @patch('sys.stdout', new_callable=StringIO)
    @patch('select.select')
    def test_generate_json(self, mock_select, mock_stdout, mock_stdin):
        """Test JSON generation via bridge protocol."""
        response = '[RESPONSE_LM_GENERATION] {"content": "{\\"result\\": \\"data\\"}"}\n'
        mock_stdin.readline = Mock(return_value=response)
        mock_select.return_value = ([True], [], [])
        
        provider = VSCodeBridgeProvider()
        
        with patch('sys.stdin.readline', return_value=response):
            result = provider.generate_json("Test prompt", {})
        
        self.assertEqual(result, {"result": "data"})
    
    @patch('select.select')
    def test_timeout(self, mock_select):
        """Test timeout handling."""
        # Mock select to indicate timeout (empty ready list)
        mock_select.return_value = ([], [], [])
        
        provider = VSCodeBridgeProvider(timeout=1)
        
        with self.assertRaises(Exception) as context:
            provider.generate("Test prompt")
        
        # The exception gets wrapped
        self.assertIn('VS Code Bridge communication error', str(context.exception))
        self.assertIn('No response received', str(context.exception))
    
    @patch('sys.stdin', new_callable=StringIO)
    @patch('select.select')
    def test_invalid_response_format(self, mock_select, mock_stdin):
        """Test handling of invalid response format."""
        response = 'Invalid response without token\n'
        mock_stdin.readline = Mock(return_value=response)
        mock_select.return_value = ([True], [], [])
        
        provider = VSCodeBridgeProvider()
        
        with patch('sys.stdin.readline', return_value=response):
            with self.assertRaises(Exception) as context:
                provider.generate("Test prompt")
            self.assertIn('Invalid response format', str(context.exception))
    
    @patch('sys.stdin', new_callable=StringIO)
    @patch('select.select')
    def test_error_response(self, mock_select, mock_stdin):
        """Test handling of error in response."""
        response = '[RESPONSE_LM_GENERATION] {"error": "API error occurred"}\n'
        mock_stdin.readline = Mock(return_value=response)
        mock_select.return_value = ([True], [], [])
        
        provider = VSCodeBridgeProvider()
        
        with patch('sys.stdin.readline', return_value=response):
            with self.assertRaises(Exception) as context:
                provider.generate("Test prompt")
            self.assertIn('VS Code LM API error', str(context.exception))
    
    @patch('sys.stdin', new_callable=StringIO)
    @patch('select.select')
    def test_empty_response(self, mock_select, mock_stdin):
        """Test handling of empty response."""
        mock_stdin.readline = Mock(return_value='')
        mock_select.return_value = ([True], [], [])
        
        provider = VSCodeBridgeProvider()
        
        with patch('sys.stdin.readline', return_value=''):
            with self.assertRaises(Exception) as context:
                provider.generate("Test prompt")
            self.assertIn('No response received', str(context.exception))


if __name__ == '__main__':
    unittest.main()
