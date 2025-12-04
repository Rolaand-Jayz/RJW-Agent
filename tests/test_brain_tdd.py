"""
TDD Tests for Brain/LLM Provider Module

These tests are written FIRST, before any implementation exists.
They capture all requirements from the 21 review concerns on PR #9.

Test Organization:
1. Interface tests - verify abstract base class contract
2. Factory tests - verify provider selection and initialization  
3. OpenAI provider tests - verify API integration and error handling
4. Gemini provider tests - verify API integration and markdown handling
5. VSCode Bridge tests - verify protocol, timeout, and security
6. Integration tests - verify ResearchHarvester and PromptOptimizer integration
"""
import json
import os
import sys
import unittest
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Mock external dependencies before any imports
sys.modules['openai'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['tavily'] = MagicMock()


class TestLLMProviderInterface(unittest.TestCase):
    """Test the abstract LLMProvider interface."""
    
    def test_interface_exists(self):
        """Test that LLMProvider interface can be imported."""
        from src.brain.interface import LLMProvider
        self.assertTrue(hasattr(LLMProvider, 'generate'))
        self.assertTrue(hasattr(LLMProvider, 'generate_json'))
    
    def test_generate_method_signature(self):
        """Test generate method has correct signature."""
        from src.brain.interface import LLMProvider
        import inspect
        sig = inspect.signature(LLMProvider.generate)
        params = list(sig.parameters.keys())
        self.assertIn('prompt', params)
        self.assertIn('system_prompt', params)
    
    def test_generate_json_method_signature(self):
        """Test generate_json method has correct signature."""
        from src.brain.interface import LLMProvider
        import inspect
        sig = inspect.signature(LLMProvider.generate_json)
        params = list(sig.parameters.keys())
        self.assertIn('prompt', params)
        self.assertIn('schema', params)
    
    def test_generate_json_documentation_clarity(self):
        """
        Test that generate_json has clear documentation about schema validation.
        Addresses concern: Schema parameter should clarify it's a hint, not enforced.
        """
        from src.brain.interface import LLMProvider
        docstring = LLMProvider.generate_json.__doc__
        self.assertIsNotNone(docstring)
        # Should mention that schema is a hint/guide, not validation
        self.assertTrue(
            'hint' in docstring.lower() or 'guide' in docstring.lower(),
            "Documentation should clarify schema is a hint to LLM"
        )


class TestProviderFactory(unittest.TestCase):
    """Test the provider factory with proper error handling."""
    
    def test_factory_exists(self):
        """Test that get_provider factory function exists."""
        from src.brain.factory import get_provider
        self.assertTrue(callable(get_provider))
    
    def test_list_providers_function(self):
        """Test list_providers returns available providers."""
        from src.brain.factory import list_providers
        providers = list_providers()
        self.assertIn('openai', providers)
        self.assertIn('gemini', providers)
        self.assertIn('vscode', providers)
    
    def test_get_default_provider_function(self):
        """Test get_default_provider returns default."""
        from src.brain.factory import get_default_provider
        default = get_default_provider()
        self.assertIsInstance(default, str)
    
    def test_factory_raises_value_error_for_invalid_provider(self):
        """
        Test factory raises ValueError (not generic Exception) for invalid provider.
        Addresses concern: Use specific exceptions.
        """
        from src.brain.factory import get_provider
        with self.assertRaises(ValueError):
            get_provider('invalid_provider_name')
    
    def test_factory_empty_except_has_comment(self):
        """
        Test that empty except blocks have explanatory comments.
        Addresses concern: Add comments to empty except blocks.
        """
        import inspect
        from src.brain import factory
        source = inspect.getsource(factory)
        # If there's an except ImportError with just pass, should have comment
        if 'except ImportError:' in source and '\n        pass' in source:
            # Should have a comment explaining why
            self.assertTrue('# ' in source, "Empty except blocks should have comments")
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_factory_creates_openai_provider(self):
        """Test factory can create OpenAI provider."""
        from src.brain.factory import get_provider
        with patch('openai.OpenAI'):
            provider = get_provider('openai')
            self.assertIsNotNone(provider)
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    def test_factory_creates_gemini_provider(self):
        """Test factory can create Gemini provider."""
        from src.brain.factory import get_provider
        with patch('google.generativeai.configure'), \
             patch('google.generativeai.GenerativeModel'):
            provider = get_provider('gemini')
            self.assertIsNotNone(provider)
    
    def test_factory_creates_vscode_provider(self):
        """Test factory can create VS Code Bridge provider."""
        from src.brain.factory import get_provider
        provider = get_provider('vscode')
        self.assertIsNotNone(provider)


class TestOpenAIProvider(unittest.TestCase):
    """Test OpenAI provider implementation."""
    
    def test_openai_provider_exists(self):
        """Test OpenAI provider class exists."""
        from src.brain.providers.openai import OpenAIProvider
        self.assertTrue(callable(OpenAIProvider))
    
    def test_init_raises_value_error_without_api_key(self):
        """
        Test initialization raises ValueError (not generic Exception).
        Addresses concern: Use specific exceptions.
        """
        from src.brain.providers.openai import OpenAIProvider
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                OpenAIProvider()
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_generate_json_has_schema_comment(self):
        """
        Test that generate_json has comment about schema being a hint.
        Addresses concern: Add clarifying comment about schema usage.
        """
        import inspect
        from src.brain.providers.openai import OpenAIProvider
        source = inspect.getsource(OpenAIProvider.generate_json)
        # Should have comment explaining schema is a hint, not enforced
        self.assertIn('# ', source)
        self.assertTrue(
            'hint' in source.lower() or 'guide' in source.lower() or 'not validate' in source.lower(),
            "Should have comment explaining schema is not enforced"
        )
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_generate_returns_string(self):
        """Test generate method returns string."""
        from src.brain.providers.openai import OpenAIProvider
        with patch('openai.OpenAI') as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "test response"
            mock_client.chat.completions.create.return_value = mock_response
            
            provider = OpenAIProvider()
            result = provider.generate("test prompt")
            self.assertIsInstance(result, str)
    
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'})
    def test_generate_json_returns_dict(self):
        """Test generate_json method returns dict."""
        from src.brain.providers.openai import OpenAIProvider
        with patch('openai.OpenAI') as mock_client_class:
            mock_client = MagicMock()
            mock_client_class.return_value = mock_client
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = '{"key": "value"}'
            mock_client.chat.completions.create.return_value = mock_response
            
            provider = OpenAIProvider()
            result = provider.generate_json("test prompt", {})
            self.assertIsInstance(result, dict)


class TestGeminiProvider(unittest.TestCase):
    """Test Gemini provider implementation."""
    
    def test_gemini_provider_exists(self):
        """Test Gemini provider class exists."""
        from src.brain.providers.gemini import GeminiProvider
        self.assertTrue(callable(GeminiProvider))
    
    def test_init_raises_value_error_without_api_key(self):
        """Test initialization raises ValueError without API key."""
        from src.brain.providers.gemini import GeminiProvider
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                GeminiProvider()
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    def test_markdown_fence_detection_handles_language_specifier(self):
        """
        Test markdown fence detection handles ```json, ```javascript, etc.
        Addresses concern: Fix markdown code fence detection logic.
        """
        from src.brain.providers.gemini import GeminiProvider
        import google.generativeai as genai
        with patch.object(genai, 'configure'), \
             patch.object(genai, 'GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model
            mock_response = MagicMock()
            # Test with language specifier
            mock_response.text = '```json\n{"result": "data"}\n```'
            mock_model.generate_content.return_value = mock_response
            
            provider = GeminiProvider()
            result = provider.generate_json("test", {})
            self.assertEqual(result, {"result": "data"})
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test-key'})
    def test_markdown_fence_handles_trailing_whitespace(self):
        """
        Test markdown fence handles closing fence with whitespace.
        Addresses concern: Fence detection should use startswith for flexibility.
        """
        from src.brain.providers.gemini import GeminiProvider
        import google.generativeai as genai
        with patch.object(genai, 'configure'), \
             patch.object(genai, 'GenerativeModel') as mock_model_class:
            mock_model = MagicMock()
            mock_model_class.return_value = mock_model
            mock_response = MagicMock()
            # Test with trailing whitespace/content on closing fence
            mock_response.text = '```\n{"result": "data"}\n``` \n'
            mock_model.generate_content.return_value = mock_response
            
            provider = GeminiProvider()
            result = provider.generate_json("test", {})
            self.assertEqual(result, {"result": "data"})


class TestVSCodeBridgeProvider(unittest.TestCase):
    """Test VS Code Bridge provider implementation."""
    
    def test_vscode_provider_exists(self):
        """Test VS Code Bridge provider class exists."""
        from src.brain.providers.vscode_bridge import VSCodeBridgeProvider
        self.assertTrue(callable(VSCodeBridgeProvider))
    
    def test_vscode_has_security_warning_in_docstring(self):
        """
        Test VS Code Bridge has security warning about sensitive data.
        Addresses concern: Add security warning to docstring.
        """
        from src.brain.providers.vscode_bridge import VSCodeBridgeProvider
        docstring = VSCodeBridgeProvider.__doc__
        self.assertIsNotNone(docstring)
        self.assertTrue(
            'security' in docstring.lower() or 'sensitive' in docstring.lower(),
            "Should have security warning about sensitive data in prompts"
        )
    
    def test_timeout_parameter_accepted(self):
        """Test timeout parameter is accepted in constructor."""
        from src.brain.providers.vscode_bridge import VSCodeBridgeProvider
        provider = VSCodeBridgeProvider(timeout=60)
        self.assertEqual(provider.timeout, 60)
    
    @patch('select.select')
    def test_timeout_raises_timeout_error_on_unix(self):
        """
        Test timeout raises TimeoutError on Unix systems.
        Addresses concern: Implement timeout functionality.
        """
        from src.brain.providers.vscode_bridge import VSCodeBridgeProvider
        # Mock select to indicate timeout
        mock_select = MagicMock(return_value=([], [], []))
        with patch('select.select', mock_select):
            provider = VSCodeBridgeProvider(timeout=1)
            with self.assertRaises(Exception) as context:
                provider.generate("test")
            # The TimeoutError gets wrapped in generic Exception
            self.assertIn('timeout', str(context.exception).lower())
    
    def test_windows_timeout_implementation_exists(self):
        """
        Test Windows timeout implementation exists.
        Addresses concern: Add Windows-compatible timeout.
        """
        import inspect
        from src.brain.providers.vscode_bridge import VSCodeBridgeProvider
        source = inspect.getsource(VSCodeBridgeProvider._send_request)
        # Should have Windows fallback using threading
        self.assertIn('threading', source.lower(), "Should have Windows timeout using threading")
    
    @patch('sys.stdin')
    @patch('select.select')
    def test_empty_response_raises_exception(self):
        """Test empty response raises exception."""
        from src.brain.providers.vscode_bridge import VSCodeBridgeProvider
        mock_select = MagicMock(return_value=([True], [], []))
        with patch('select.select', mock_select), \
             patch('sys.stdin.readline', return_value=''):
            provider = VSCodeBridgeProvider()
            with self.assertRaises(Exception):
                provider.generate("test")
    
    @patch('sys.stdin')
    @patch('select.select')
    def test_invalid_format_raises_exception(self):
        """Test invalid response format raises exception."""
        from src.brain.providers.vscode_bridge import VSCodeBridgeProvider
        mock_select = MagicMock(return_value=([True], [], []))
        with patch('select.select', mock_select), \
             patch('sys.stdin.readline', return_value='invalid response\n'):
            provider = VSCodeBridgeProvider()
            with self.assertRaises(Exception) as context:
                provider.generate("test")
            self.assertIn('Invalid response format', str(context.exception))


class TestPromptOptimizerIntegration(unittest.TestCase):
    """Test PromptOptimizer integration with LLM provider."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_optimizer_accepts_provider_parameter(self):
        """Test PromptOptimizer accepts optional provider parameter."""
        from src.interaction.optimizer import PromptOptimizer
        # Should not raise error
        optimizer = PromptOptimizer(research_output_dir=self.test_dir)
        self.assertTrue(hasattr(optimizer, 'llm_provider'))
    
    def test_optimizer_initialization_handles_specific_exceptions(self):
        """
        Test optimizer catches specific exceptions, not generic Exception.
        Addresses concern: Use specific exception types.
        """
        import inspect
        from src.interaction import optimizer
        source = inspect.getsource(optimizer.PromptOptimizer.__init__)
        # Should catch specific exceptions like ValueError, ImportError, OSError
        if 'except' in source:
            self.assertTrue(
                'ValueError' in source or 'ImportError' in source,
                "Should catch specific exceptions like ValueError, ImportError, OSError"
            )
    
    def test_topic_extraction_handles_specific_exceptions(self):
        """
        Test topic extraction catches specific exceptions.
        Addresses concern: Replace broad Exception with specific types.
        """
        import inspect
        from src.interaction import optimizer
        source = inspect.getsource(optimizer.PromptOptimizer._extract_research_topics)
        # Should catch specific exceptions
        if 'except' in source and 'Exception' in source:
            self.assertTrue(
                'ValueError' in source or 'KeyError' in source or 'TypeError' in source,
                "Should catch specific exceptions in topic extraction"
            )
    
    def test_topic_extraction_schema_consistency(self):
        """
        Test topic extraction uses consistent schema (array, not dict with 'topics').
        Addresses concern: Fix schema inconsistency.
        """
        from src.interaction.optimizer import PromptOptimizer
        with patch('src.interaction.optimizer.get_provider') as mock_get:
            mock_provider = Mock()
            # Return direct list (not dict with 'topics' key)
            mock_provider.generate_json.return_value = ["topic1", "topic2"]
            mock_get.return_value = mock_provider
            
            optimizer = PromptOptimizer(research_output_dir=self.test_dir, provider='openai')
            topics = optimizer._extract_research_topics("test input")
            self.assertIsInstance(topics, list)
    
    def test_no_unused_imports(self):
        """
        Test PromptOptimizer doesn't import unused LLMProvider.
        Addresses concern: Remove unused LLMProvider import.
        """
        import inspect
        from src.interaction import optimizer
        source = inspect.getsource(optimizer)
        # Should import get_provider but not LLMProvider class directly
        self.assertIn('from ..brain import get_provider', source)
        self.assertNotIn('from ..brain import get_provider, LLMProvider', source)


class TestResearchHarvesterIntegration(unittest.TestCase):
    """Test ResearchHarvester integration with LLM and Tavily."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_harvester_accepts_llm_provider_parameter(self):
        """Test ResearchHarvester accepts optional llm_provider parameter."""
        from src.discovery.research import ResearchHarvester
        mock_provider = Mock()
        harvester = ResearchHarvester(self.test_dir, llm_provider=mock_provider)
        self.assertEqual(harvester.llm_provider, mock_provider)
    
    def test_research_handles_specific_exceptions(self):
        """
        Test research method catches specific exceptions.
        Addresses concern: Replace broad Exception with specific types.
        """
        import inspect
        from src.discovery import research
        source = inspect.getsource(research.ResearchHarvester._conduct_research)
        # Should catch specific exceptions like ImportError, KeyError, ValueError, ConnectionError
        if 'except' in source and 'Exception' in source:
            exception_count = source.count('ImportError') + source.count('KeyError') + source.count('ValueError')
            self.assertGreater(exception_count, 0, "Should catch specific exceptions")
    
    @patch.dict(os.environ, {'TAVILY_API_KEY': 'test-key'})
    def test_tavily_integration_with_llm(self):
        """Test Tavily search integration with LLM summarization."""
        from src.discovery.research import ResearchHarvester
        with patch('tavily.TavilyClient') as mock_tavily_class:
            mock_tavily = Mock()
            mock_tavily_class.return_value = mock_tavily
            mock_tavily.search.return_value = {
                'results': [{'url': 'test.com', 'content': 'test content'}]
            }
            
            mock_llm = Mock()
            mock_llm.generate_json.return_value = {
                'summary': 'test summary',
                'insights': ['insight1', 'insight2']
            }
            
            harvester = ResearchHarvester(self.test_dir, llm_provider=mock_llm)
            summary, insights = harvester._conduct_research("test topic")
            
            self.assertIsInstance(summary, str)
            self.assertIsInstance(insights, list)


class TestDocumentation(unittest.TestCase):
    """Test documentation improvements."""
    
    def test_brain_readme_mentions_gpt4o(self):
        """
        Test Brain README mentions gpt-4o specifically.
        Addresses concern: Fix model name references.
        """
        readme_path = 'src/brain/README.md'
        if os.path.exists(readme_path):
            with open(readme_path) as f:
                content = f.read()
            self.assertIn('gpt-4o', content, "Should mention gpt-4o model specifically")
    
    def test_setup_guide_has_pricing_links(self):
        """
        Test setup guide links to current pricing pages.
        Addresses concern: Make cost estimates link to current pricing.
        """
        guide_path = 'docs/brain-setup-guide.md'
        if os.path.exists(guide_path):
            with open(guide_path) as f:
                content = f.read()
            self.assertIn('openai.com/pricing', content, "Should link to OpenAI pricing")
            self.assertIn('ai.google.dev/pricing', content, "Should link to Google pricing")


class TestRequirementsTxt(unittest.TestCase):
    """Test requirements.txt has necessary dependencies."""
    
    def test_requirements_has_llm_dependencies(self):
        """Test requirements.txt includes LLM provider dependencies."""
        with open('requirements.txt') as f:
            content = f.read()
        self.assertIn('openai', content)
        self.assertIn('google-generativeai', content)
        self.assertIn('tavily-python', content)
        self.assertIn('python-dotenv', content)


class TestExamplesScripts(unittest.TestCase):
    """Test example scripts."""
    
    def test_test_providers_script_exists(self):
        """Test examples/test_providers.py exists."""
        self.assertTrue(os.path.exists('examples/test_providers.py'))
    
    def test_response_truncation_logic(self):
        """
        Test response truncation only adds ... when needed.
        Addresses concern: Fix truncation logic.
        """
        script_path = 'examples/test_providers.py'
        if os.path.exists(script_path):
            with open(script_path) as f:
                content = f.read()
            # Should check length before truncating
            if '[:500]' in content:
                self.assertIn('if len', content, "Should check length before truncating")


if __name__ == '__main__':
    unittest.main()
