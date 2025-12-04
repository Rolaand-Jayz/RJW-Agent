"""Tests for Brain/LLM provider integration with existing modules."""
import os
import sys
import unittest
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Mock the external dependencies before importing our modules
sys.modules['openai'] = MagicMock()
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['tavily'] = MagicMock()

from src.interaction.optimizer import PromptOptimizer
from src.discovery.research import ResearchHarvester


class TestPromptOptimizerWithLLM(unittest.TestCase):
    """Test PromptOptimizer with LLM provider integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.research_dir = os.path.join(self.test_dir, 'research')
        self.specs_dir = os.path.join(self.test_dir, 'specs')
        self.decisions_dir = os.path.join(self.test_dir, 'decisions')
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_init_without_provider(self):
        """Test initialization without LLM provider."""
        optimizer = PromptOptimizer(
            research_output_dir=self.research_dir,
            specs_output_dir=self.specs_dir,
            decisions_output_dir=self.decisions_dir
        )
        self.assertIsNone(optimizer.llm_provider)
    
    @patch('src.interaction.optimizer.get_provider')
    def test_init_with_provider(self, mock_get_provider):
        """Test initialization with LLM provider."""
        mock_provider = Mock()
        mock_get_provider.return_value = mock_provider
        
        optimizer = PromptOptimizer(
            research_output_dir=self.research_dir,
            specs_output_dir=self.specs_dir,
            decisions_output_dir=self.decisions_dir,
            provider='openai'
        )
        
        self.assertEqual(optimizer.llm_provider, mock_provider)
        mock_get_provider.assert_called_once_with('openai')
    
    @patch('src.interaction.optimizer.get_provider')
    def test_init_provider_failure(self, mock_get_provider):
        """Test graceful handling of provider initialization failure."""
        mock_get_provider.side_effect = ValueError("API key not found")
        
        with patch('warnings.warn') as mock_warn:
            optimizer = PromptOptimizer(
                research_output_dir=self.research_dir,
                provider='openai'
            )
            
            self.assertIsNone(optimizer.llm_provider)
            mock_warn.assert_called_once()
            self.assertIn('Failed to initialize LLM provider', str(mock_warn.call_args[0][0]))
    
    @patch('src.interaction.optimizer.get_provider')
    def test_extract_topics_with_llm(self, mock_get_provider):
        """Test topic extraction using LLM."""
        mock_provider = Mock()
        mock_provider.generate_json.return_value = [
            "authentication patterns",
            "API security",
            "JWT tokens"
        ]
        mock_get_provider.return_value = mock_provider
        
        optimizer = PromptOptimizer(
            research_output_dir=self.research_dir,
            provider='openai'
        )
        
        topics = optimizer._extract_research_topics("Add secure authentication to the API")
        
        self.assertEqual(len(topics), 3)
        self.assertIn("authentication patterns", topics)
        self.assertIn("API security", topics)
        mock_provider.generate_json.assert_called_once()
    
    @patch('src.interaction.optimizer.get_provider')
    def test_extract_topics_llm_wrapped_response(self, mock_get_provider):
        """Test topic extraction with LLM returning wrapped dict."""
        mock_provider = Mock()
        # Some LLMs might wrap the array in an object
        mock_provider.generate_json.return_value = {
            "topics": ["database design", "NoSQL patterns"]
        }
        mock_get_provider.return_value = mock_provider
        
        optimizer = PromptOptimizer(
            research_output_dir=self.research_dir,
            provider='openai'
        )
        
        topics = optimizer._extract_research_topics("Design a scalable database")
        
        self.assertEqual(len(topics), 2)
        self.assertIn("database design", topics)
    
    @patch('src.interaction.optimizer.get_provider')
    def test_extract_topics_llm_fallback_on_error(self, mock_get_provider):
        """Test fallback to keyword extraction when LLM fails."""
        mock_provider = Mock()
        mock_provider.generate_json.side_effect = ConnectionError("Network error")
        mock_get_provider.return_value = mock_provider
        
        with patch('warnings.warn') as mock_warn:
            optimizer = PromptOptimizer(
                research_output_dir=self.research_dir,
                provider='openai'
            )
            
            topics = optimizer._extract_research_topics("Add authentication to the API")
            
            # Should fall back to keyword-based extraction
            self.assertIsInstance(topics, list)
            self.assertGreater(len(topics), 0)
            mock_warn.assert_called()
            self.assertIn('LLM topic extraction failed', str(mock_warn.call_args[0][0]))
    
    def test_extract_topics_without_llm(self):
        """Test topic extraction without LLM (keyword-based)."""
        optimizer = PromptOptimizer(
            research_output_dir=self.research_dir
        )
        
        topics = optimizer._extract_research_topics("Add authentication to the API")
        
        self.assertIsInstance(topics, list)
        self.assertGreater(len(topics), 0)


class TestResearchHarvesterWithLLM(unittest.TestCase):
    """Test ResearchHarvester with LLM provider integration."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, 'evidence')
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_init_without_llm(self):
        """Test initialization without LLM provider."""
        harvester = ResearchHarvester(self.output_dir)
        self.assertIsNone(harvester.llm_provider)
    
    def test_init_with_llm(self):
        """Test initialization with LLM provider."""
        mock_provider = Mock()
        harvester = ResearchHarvester(self.output_dir, llm_provider=mock_provider)
        self.assertEqual(harvester.llm_provider, mock_provider)
    
    @patch.dict(os.environ, {'TAVILY_API_KEY': 'test-key'})
    def test_research_with_tavily_and_llm(self):
        """Test real research using Tavily and LLM."""
        with patch('tavily.TavilyClient') as mock_tavily_class:
            # Setup mocks
            mock_tavily = Mock()
            mock_tavily_class.return_value = mock_tavily
            mock_tavily.search.return_value = {
                'results': [
                    {
                        'url': 'https://example.com/auth',
                        'content': 'Authentication best practices include using JWT...'
                    },
                    {
                        'url': 'https://example.com/security',
                        'content': 'API security requires proper authentication...'
                    }
                ]
            }
            
            mock_llm = Mock()
            mock_llm.generate_json.return_value = {
                'summary': 'JWT is recommended for API authentication.',
                'insights': [
                    'Use JWT tokens for stateless authentication',
                    'Implement refresh token rotation',
                    'Store tokens securely in httpOnly cookies'
                ]
            }
            
            harvester = ResearchHarvester(self.output_dir, llm_provider=mock_llm)
            summary, insights = harvester._conduct_research("API authentication")
            
            self.assertIn('JWT', summary)
            self.assertEqual(len(insights), 3)
            self.assertIn('JWT tokens', insights[0])
            
            mock_tavily.search.assert_called_once()
            mock_llm.generate_json.assert_called_once()
    
    def test_research_without_llm(self):
        """Test research falls back to simulated output without LLM."""
        harvester = ResearchHarvester(self.output_dir)
        summary, insights = harvester._conduct_research("API authentication")
        
        # Should use simulated output
        self.assertIsInstance(summary, str)
        self.assertIsInstance(insights, list)
        self.assertGreater(len(insights), 0)
    
    @patch.dict(os.environ, {}, clear=True)
    def test_research_without_tavily_key(self):
        """Test research falls back when Tavily key is missing."""
        mock_llm = Mock()
        harvester = ResearchHarvester(self.output_dir, llm_provider=mock_llm)
        
        summary, insights = harvester._conduct_research("API authentication")
        
        # Should fall back to simulated output
        self.assertIsInstance(summary, str)
        self.assertIsInstance(insights, list)
        mock_llm.generate_json.assert_not_called()
    
    @patch.dict(os.environ, {'TAVILY_API_KEY': 'test-key'})
    def test_research_tavily_failure(self):
        """Test fallback when Tavily search fails."""
        with patch('tavily.TavilyClient') as mock_tavily_class:
            mock_tavily = Mock()
            mock_tavily_class.return_value = mock_tavily
            mock_tavily.search.side_effect = ConnectionError("Network error")
            
            mock_llm = Mock()
            harvester = ResearchHarvester(self.output_dir, llm_provider=mock_llm)
            
            with patch('warnings.warn') as mock_warn:
                summary, insights = harvester._conduct_research("API authentication")
                
                # Should fall back to simulated output
                self.assertIsInstance(summary, str)
                self.assertIsInstance(insights, list)
                mock_warn.assert_called()
                self.assertIn('Real research failed', str(mock_warn.call_args[0][0]))
    
    @patch.dict(os.environ, {'TAVILY_API_KEY': 'test-key'})
    def test_research_llm_failure(self):
        """Test fallback when LLM fails to process results."""
        with patch('tavily.TavilyClient') as mock_tavily_class:
            mock_tavily = Mock()
            mock_tavily_class.return_value = mock_tavily
            mock_tavily.search.return_value = {'results': []}
            
            mock_llm = Mock()
            mock_llm.generate_json.side_effect = ValueError("Invalid response")
            
            harvester = ResearchHarvester(self.output_dir, llm_provider=mock_llm)
            
            with patch('warnings.warn') as mock_warn:
                summary, insights = harvester._conduct_research("API authentication")
                
                # Should fall back to simulated output
                self.assertIsInstance(summary, str)
                self.assertIsInstance(insights, list)
                mock_warn.assert_called()
    
    def test_research_with_raw_content(self):
        """Test research with provided raw content skips Tavily."""
        mock_llm = Mock()
        harvester = ResearchHarvester(self.output_dir, llm_provider=mock_llm)
        
        raw_content = "Some research content about authentication"
        summary, insights = harvester._conduct_research(
            "API authentication",
            raw_content=raw_content
        )
        
        # Should use simulated processing, not call LLM
        self.assertIsInstance(summary, str)
        self.assertIsInstance(insights, list)
        mock_llm.generate_json.assert_not_called()


if __name__ == '__main__':
    unittest.main()
