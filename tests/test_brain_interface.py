"""Tests for the Brain module interface."""
import unittest
from typing import Dict, Any, Optional


class TestLLMProviderInterface(unittest.TestCase):
    """Test the LLMProvider abstract base class."""
    
    def test_interface_enforcement(self):
        """Test that subclass without implementing abstract methods raises TypeError on instantiation."""
        from src.brain.interface import LLMProvider
        
        # Create incomplete implementation
        class IncompleteProvider(LLMProvider):
            """Provider missing abstract method implementations."""
            pass
        
        # Should raise TypeError when trying to instantiate
        with self.assertRaises(TypeError) as context:
            IncompleteProvider()
        
        # Error message should mention abstract methods
        error_msg = str(context.exception)
        self.assertIn("abstract method", error_msg.lower())
    
    def test_llm_provider_is_abstract(self):
        """Test that LLMProvider itself cannot be instantiated."""
        from src.brain.interface import LLMProvider
        
        # Should raise TypeError when trying to instantiate ABC directly
        with self.assertRaises(TypeError) as context:
            LLMProvider()
        
        error_msg = str(context.exception)
        self.assertIn("abstract", error_msg.lower())
    
    def test_interface_enforcement_complete_implementation(self):
        """Test that complete subclass CAN be instantiated."""
        from src.brain.interface import LLMProvider
        
        # Create complete implementation
        class CompleteProvider(LLMProvider):
            """Provider with all abstract methods implemented."""
            
            def generate(
                self,
                prompt: str,
                system_prompt: Optional[str] = None,
                temperature: float = 0.7,
                max_tokens: int = 1024
            ) -> str:
                return f"Response to: {prompt}"
            
            def generate_json(
                self,
                prompt: str,
                schema: Dict[str, Any],
                system_prompt: Optional[str] = None
            ) -> Dict[str, Any]:
                return {"response": "json response"}
        
        # Should NOT raise any exception
        provider = CompleteProvider()
        self.assertIsNotNone(provider)
        
        # Verify methods work
        text_response = provider.generate("test prompt")
        self.assertIsInstance(text_response, str)
        self.assertIn("test prompt", text_response)
        
        json_response = provider.generate_json("test", {})
        self.assertIsInstance(json_response, dict)
        self.assertIn("response", json_response)
    
    def test_interface_has_required_methods(self):
        """Test that LLMProvider defines the required abstract methods."""
        from src.brain.interface import LLMProvider
        import inspect
        
        # Get abstract methods
        abstract_methods = {
            name for name, method in inspect.getmembers(LLMProvider)
            if getattr(method, '__isabstractmethod__', False)
        }
        
        # Should have generate and generate_json
        self.assertIn('generate', abstract_methods)
        self.assertIn('generate_json', abstract_methods)
        self.assertEqual(len(abstract_methods), 2, 
                        f"Expected 2 abstract methods, found: {abstract_methods}")


if __name__ == '__main__':
    unittest.main()
