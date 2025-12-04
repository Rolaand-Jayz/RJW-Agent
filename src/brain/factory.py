"""
Provider Factory.

Factory function for creating LLM provider instances.
"""

from typing import Optional

from .interface import LLMProvider
from .providers.openai import OpenAIProvider
from .providers.gemini import GeminiProvider
from .providers.vscode import VSCodeBridgeProvider


def get_provider(provider_name: str, api_key: Optional[str] = None, **kwargs) -> LLMProvider:
    """
    Get LLM provider instance.

    Factory function that creates and returns an instance of the specified
    LLM provider. Provider names are case-insensitive.

    Args:
        provider_name: Provider identifier (openai, gemini, vscode)
        api_key: Optional API key (can use environment variable)
        **kwargs: Provider-specific configuration options

    Returns:
        LLMProvider instance

    Raises:
        ValueError: If provider_name is unknown

    Examples:
        >>> provider = get_provider("openai", api_key="sk-...")
        >>> provider = get_provider("gemini", model="gemini-pro")
        >>> provider = get_provider("vscode")
    """
    # Normalize provider name to lowercase
    provider_name_lower = provider_name.lower()

    # Create and return appropriate provider
    if provider_name_lower == "openai":
        return OpenAIProvider(api_key=api_key, **kwargs)

    elif provider_name_lower == "gemini":
        return GeminiProvider(api_key=api_key, **kwargs)

    elif provider_name_lower == "vscode":
        return VSCodeBridgeProvider(**kwargs)

    else:
        raise ValueError(
            f"Unknown provider: '{provider_name}'. " f"Supported providers: openai, gemini, vscode"
        )
