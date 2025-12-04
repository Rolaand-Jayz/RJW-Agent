"""
Provider Factory for LLM providers.

Implements the Factory pattern to instantiate the appropriate LLM provider
based on configuration or user choice.
"""
import os
from typing import Optional

from .interface import LLMProvider


def get_provider(provider_name: Optional[str] = None, **kwargs) -> LLMProvider:
    """
    Factory function to get an LLM provider instance.
    
    This function:
    1. Loads environment variables using python-dotenv
    2. Determines which provider to use (from parameter or environment)
    3. Instantiates and returns the appropriate provider
    
    Args:
        provider_name: Name of provider ('openai', 'gemini', 'vscode')
                      If None, uses RJW_PROVIDER env var or defaults to 'openai'
        **kwargs: Additional arguments passed to provider constructor
        
    Returns:
        Initialized LLMProvider instance
        
    Raises:
        ValueError: If provider_name is invalid
        ImportError: If required provider package is not installed
        
    Examples:
        >>> provider = get_provider('openai')
        >>> provider = get_provider('gemini', model='gemini-1.5-flash')
        >>> provider = get_provider()  # Uses default or env var
    """
    # Load environment variables from .env file if present
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # python-dotenv not installed, continue without it
        pass
    
    # Determine provider to use
    if provider_name is None:
        provider_name = os.getenv("RJW_PROVIDER", "openai")
    
    provider_name = provider_name.lower()
    
    # Instantiate the appropriate provider
    if provider_name == "openai":
        from .providers.openai import OpenAIProvider
        return OpenAIProvider(**kwargs)
    
    elif provider_name == "gemini":
        from .providers.gemini import GeminiProvider
        return GeminiProvider(**kwargs)
    
    elif provider_name == "vscode":
        from .providers.vscode_bridge import VSCodeBridgeProvider
        return VSCodeBridgeProvider(**kwargs)
    
    else:
        raise ValueError(
            f"Unknown provider: {provider_name}. "
            f"Valid options are: 'openai', 'gemini', 'vscode'"
        )


def list_providers() -> list:
    """
    List all available provider names.
    
    Returns:
        List of supported provider names
    """
    return ["openai", "gemini", "vscode"]


def get_default_provider() -> str:
    """
    Get the name of the default provider.
    
    Returns:
        Default provider name (from env var or 'openai')
    """
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        # python-dotenv not installed, continue without loading environment variables
        pass
    
    return os.getenv("RJW_PROVIDER", "openai")
