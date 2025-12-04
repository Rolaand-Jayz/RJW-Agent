"""
Brain Module - LLM Integration.

This module provides LLM integration using a Strategy Pattern to support
multiple providers (BYOK - Bring Your Own Key).
"""

from .interface import LLMProvider
from .factory import get_provider

__all__ = ["LLMProvider", "get_provider"]
