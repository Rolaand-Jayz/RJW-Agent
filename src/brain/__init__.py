"""
Brain Module - LLM Provider Architecture.

Provides a modular, pluggable interface for different LLM providers
following the Strategy Pattern and supporting "Bring Your Own Key" (BYOK).
"""
from .interface import LLMProvider
from .factory import get_provider, list_providers, get_default_provider

__all__ = [
    'LLMProvider',
    'get_provider',
    'list_providers',
    'get_default_provider'
]
