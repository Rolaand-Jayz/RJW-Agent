"""Tests for LLM provider implementations."""

import json
import unittest
from unittest.mock import MagicMock, patch


class TestOpenAIProvider(unittest.TestCase):
    """Test OpenAI provider implementation."""

    @patch("src.brain.providers.openai.OpenAI")
    def test_openai_provider_initialization(self, mock_openai_class):
        """Test OpenAI provider can be initialized."""
        from src.brain.providers.openai import OpenAIProvider

        provider = OpenAIProvider(api_key="test-key", model="gpt-4")

        self.assertEqual(provider.model, "gpt-4")
        self.assertEqual(provider.api_key, "test-key")
        mock_openai_class.assert_called_once()

    @patch("src.brain.providers.openai.OpenAI")
    def test_openai_generate_formats_messages_correctly(self, mock_openai_class):
        """Test that generate() formats messages correctly for OpenAI API."""
        from src.brain.providers.openai import OpenAIProvider

        # Setup mock
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response

        # Create provider and generate
        provider = OpenAIProvider(api_key="test-key")
        result = provider.generate(
            prompt="Test prompt",
            system_prompt="System instructions",
            temperature=0.5,
            max_tokens=512,
        )

        # Verify
        self.assertEqual(result, "Test response")
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args

        messages = call_args.kwargs["messages"]
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], "System instructions")
        self.assertEqual(messages[1]["role"], "user")
        self.assertEqual(messages[1]["content"], "Test prompt")
        self.assertEqual(call_args.kwargs["temperature"], 0.5)
        self.assertEqual(call_args.kwargs["max_tokens"], 512)

    @patch("src.brain.providers.openai.OpenAI")
    def test_openai_generate_without_system_prompt(self, mock_openai_class):
        """Test that generate() works without system prompt."""
        from src.brain.providers.openai import OpenAIProvider

        # Setup mock
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Response"
        mock_client.chat.completions.create.return_value = mock_response

        # Create provider and generate
        provider = OpenAIProvider(api_key="test-key")
        provider.generate(prompt="Test prompt")

        # Verify only user message
        call_args = mock_client.chat.completions.create.call_args
        messages = call_args.kwargs["messages"]
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["role"], "user")

    @patch("src.brain.providers.openai.OpenAI")
    def test_openai_generate_json(self, mock_openai_class):
        """Test that generate_json() uses JSON mode and parses response."""
        from src.brain.providers.openai import OpenAIProvider

        # Setup mock
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client

        json_response = {"key": "value", "number": 42}
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps(json_response)
        mock_client.chat.completions.create.return_value = mock_response

        # Create provider and generate JSON
        provider = OpenAIProvider(api_key="test-key")
        schema = {"type": "object", "properties": {"key": {"type": "string"}}}
        result = provider.generate_json(
            prompt="Generate JSON", schema=schema, system_prompt="System"
        )

        # Verify
        self.assertEqual(result, json_response)
        call_args = mock_client.chat.completions.create.call_args
        self.assertEqual(call_args.kwargs["response_format"], {"type": "json_object"})

        # Verify schema is in messages
        messages = call_args.kwargs["messages"]
        system_content = messages[0]["content"]
        self.assertIn("schema", system_content.lower())


class TestGeminiProvider(unittest.TestCase):
    """Test Google Gemini provider implementation."""

    @patch("src.brain.providers.gemini.genai.GenerativeModel")
    @patch("src.brain.providers.gemini.genai.configure")
    def test_gemini_provider_initialization(self, mock_configure, mock_model_class):
        """Test Gemini provider can be initialized."""
        from src.brain.providers.gemini import GeminiProvider

        provider = GeminiProvider(api_key="test-key", model="gemini-pro")

        self.assertEqual(provider.model_name, "gemini-pro")
        self.assertEqual(provider.api_key, "test-key")
        mock_configure.assert_called_once_with(api_key="test-key")
        mock_model_class.assert_called_once_with("gemini-pro")

    @patch("src.brain.providers.gemini.genai.GenerativeModel")
    @patch("src.brain.providers.gemini.genai.configure")
    def test_gemini_generate_handles_response_object(self, mock_configure, mock_model_class):
        """Test that generate() handles Gemini response object correctly."""
        from src.brain.providers.gemini import GeminiProvider

        # Setup mock
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model

        mock_response = MagicMock()
        mock_response.text = "Test response from Gemini"
        mock_model.generate_content.return_value = mock_response

        # Create provider and generate
        provider = GeminiProvider(api_key="test-key")
        result = provider.generate(
            prompt="Test prompt",
            system_prompt="System instructions",
            temperature=0.8,
            max_tokens=256,
        )

        # Verify
        self.assertEqual(result, "Test response from Gemini")
        mock_model.generate_content.assert_called_once()

        # Check that system prompt was combined with user prompt
        call_args = mock_model.generate_content.call_args
        prompt_text = call_args[0][0]
        self.assertIn("System instructions", prompt_text)
        self.assertIn("Test prompt", prompt_text)

        # Check generation config
        generation_config = call_args.kwargs["generation_config"]
        self.assertEqual(generation_config["temperature"], 0.8)
        self.assertEqual(generation_config["max_output_tokens"], 256)

    @patch("src.brain.providers.gemini.genai.GenerativeModel")
    @patch("src.brain.providers.gemini.genai.configure")
    def test_gemini_generate_json(self, mock_configure, mock_model_class):
        """Test that generate_json() parses JSON from Gemini response."""
        from src.brain.providers.gemini import GeminiProvider

        # Setup mock
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model

        json_response = {"status": "success", "data": [1, 2, 3]}
        mock_response = MagicMock()
        mock_response.text = json.dumps(json_response)
        mock_model.generate_content.return_value = mock_response

        # Create provider and generate JSON
        provider = GeminiProvider(api_key="test-key")
        schema = {"type": "object"}
        result = provider.generate_json(prompt="Generate JSON", schema=schema)

        # Verify
        self.assertEqual(result, json_response)

        # Verify schema was included in prompt
        call_args = mock_model.generate_content.call_args
        prompt_text = call_args[0][0]
        self.assertIn("schema", prompt_text.lower())
        self.assertIn("json", prompt_text.lower())


class TestVSCodeBridgeProvider(unittest.TestCase):
    """Test VS Code Bridge provider implementation."""

    def test_vscode_provider_initialization(self):
        """Test VS Code provider can be instantiated without API key."""
        from src.brain.providers.vscode import VSCodeBridgeProvider

        # Should not raise any exception
        provider = VSCodeBridgeProvider()
        self.assertIsNotNone(provider)

    def test_vscode_provider_has_generate_method(self):
        """Test VS Code provider has generate method."""
        from src.brain.providers.vscode import VSCodeBridgeProvider

        provider = VSCodeBridgeProvider()
        self.assertTrue(hasattr(provider, "generate"))
        self.assertTrue(callable(provider.generate))

        # Call the method (placeholder implementation)
        result = provider.generate("test prompt")
        self.assertIsInstance(result, str)

    def test_vscode_provider_has_generate_json_method(self):
        """Test VS Code provider has generate_json method."""
        from src.brain.providers.vscode import VSCodeBridgeProvider

        provider = VSCodeBridgeProvider()
        self.assertTrue(hasattr(provider, "generate_json"))
        self.assertTrue(callable(provider.generate_json))

        # Call the method (placeholder implementation)
        result = provider.generate_json("test prompt", {})
        self.assertIsInstance(result, dict)

    def test_vscode_provider_implements_llm_provider(self):
        """Test VS Code provider implements LLMProvider interface."""
        from src.brain.providers.vscode import VSCodeBridgeProvider
        from src.brain.interface import LLMProvider

        provider = VSCodeBridgeProvider()
        self.assertIsInstance(provider, LLMProvider)


class TestProviderEnvironmentVariables(unittest.TestCase):
    """Test providers use environment variables for API keys."""

    @patch.dict("os.environ", {"OPENAI_API_KEY": "env-key"})
    @patch("src.brain.providers.openai.OpenAI")
    def test_openai_uses_env_var(self, mock_openai_class):
        """Test OpenAI provider uses OPENAI_API_KEY from environment."""
        from src.brain.providers.openai import OpenAIProvider

        provider = OpenAIProvider()  # No api_key argument
        self.assertEqual(provider.api_key, "env-key")

    @patch.dict("os.environ", {"GOOGLE_API_KEY": "env-key"})
    @patch("src.brain.providers.gemini.genai.GenerativeModel")
    @patch("src.brain.providers.gemini.genai.configure")
    def test_gemini_uses_env_var(self, mock_configure, mock_model_class):
        """Test Gemini provider uses GOOGLE_API_KEY from environment."""
        from src.brain.providers.gemini import GeminiProvider

        provider = GeminiProvider()  # No api_key argument
        self.assertEqual(provider.api_key, "env-key")
        mock_configure.assert_called_once_with(api_key="env-key")


if __name__ == "__main__":
    unittest.main()
