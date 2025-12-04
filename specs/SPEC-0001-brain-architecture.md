# SPEC-0001: Brain Module Architecture

**Status:** Approved  
**Version:** 1.0.0  
**Date:** 2025-12-04  
**Related Decision:** DEC-0005-modular-brain.md

## Overview

This specification defines the architecture and interface for the "Brain" module, which provides LLM (Large Language Model) integration for the RJW-Agent framework using a Strategy Pattern.

## Architecture

```
src/brain/
├── __init__.py           # Package init, exposes LLMProvider and get_provider
├── interface.py          # LLMProvider abstract base class
├── factory.py            # get_provider() factory function
└── providers/
    ├── __init__.py       # Providers package init
    ├── openai.py         # OpenAIProvider implementation
    ├── gemini.py         # GeminiProvider implementation
    └── vscode.py         # VSCodeBridgeProvider implementation
```

## Component Specifications

### 1. LLMProvider Interface (`src/brain/interface.py`)

Abstract base class defining the contract for all LLM providers.

#### Class Definition

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> str:
        """
        Generate text completion from prompt.
        
        Args:
            prompt: User prompt/input
            system_prompt: Optional system instructions
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        pass
    
    @abstractmethod
    def generate_json(
        self,
        prompt: str,
        schema: Dict[str, Any],
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate structured JSON response.
        
        Args:
            prompt: User prompt/input
            schema: JSON schema for response format
            system_prompt: Optional system instructions
            
        Returns:
            Structured JSON response
        """
        pass
```

#### Requirements

- Must use `abc.ABC` as base class
- Must mark `generate()` and `generate_json()` with `@abstractmethod`
- Cannot be instantiated directly (raises `TypeError`)
- Subclasses must implement all abstract methods

### 2. Provider Factory (`src/brain/factory.py`)

Factory function for creating provider instances.

#### Function Signature

```python
def get_provider(
    provider_name: str,
    api_key: Optional[str] = None,
    **kwargs
) -> LLMProvider:
    """
    Get LLM provider instance.
    
    Args:
        provider_name: Provider identifier (openai, gemini, vscode)
        api_key: Optional API key (can use environment variable)
        **kwargs: Provider-specific configuration
        
    Returns:
        LLMProvider instance
        
    Raises:
        ValueError: If provider_name is unknown
    """
```

#### Behavior

- Provider names are case-insensitive
- Supported providers: `"openai"`, `"gemini"`, `"vscode"`
- Raises `ValueError` for unknown providers
- Passes `api_key` and `**kwargs` to provider constructor

### 3. OpenAI Provider (`src/brain/providers/openai.py`)

#### Class Definition

```python
class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4",
        **kwargs
    ):
        """
        Initialize OpenAI provider.
        
        Args:
            api_key: OpenAI API key (or use OPENAI_API_KEY env var)
            model: Model identifier (default: gpt-4)
            **kwargs: Additional OpenAI client options
        """
```

#### Requirements

- Uses `openai` Python package
- Default model: `gpt-4`
- Supports environment variable `OPENAI_API_KEY`
- Uses Chat Completions API (`client.chat.completions.create()`)
- For `generate_json()`: Uses JSON mode (`response_format={"type": "json_object"}`)

### 4. Gemini Provider (`src/brain/providers/gemini.py`)

#### Class Definition

```python
class GeminiProvider(LLMProvider):
    """Google Gemini LLM provider."""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-pro",
        **kwargs
    ):
        """
        Initialize Gemini provider.
        
        Args:
            api_key: Google API key (or use GOOGLE_API_KEY env var)
            model: Model identifier (default: gemini-pro)
            **kwargs: Additional Gemini options
        """
```

#### Requirements

- Uses `google-generativeai` package
- Default model: `gemini-pro`
- Supports environment variable `GOOGLE_API_KEY`
- Handles Gemini response object (access `.text` attribute)
- For `generate_json()`: Instructs model to output JSON in prompt

### 5. VS Code Bridge Provider (`src/brain/providers/vscode.py`)

#### Class Definition

```python
class VSCodeBridgeProvider(LLMProvider):
    """VS Code Copilot bridge provider."""
    
    def __init__(self, **kwargs):
        """
        Initialize VS Code bridge provider.
        
        Note: No API key required - uses VS Code Copilot integration
        """
```

#### Requirements

- No API key required
- Uses stdin/stdout for inter-process communication
- Placeholder implementation for future VS Code integration
- Must implement `generate()` and `generate_json()` methods

## Integration Points

### CLI Integration (`src/cli/main.py`)

#### New Arguments

```python
parser.add_argument(
    '--provider',
    choices=['openai', 'gemini', 'vscode'],
    default='openai',
    help='LLM provider to use'
)

parser.add_argument(
    '--api-key',
    help='API key for LLM provider (or use environment variable)'
)

parser.add_argument(
    '--model',
    help='Model identifier for the selected provider'
)
```

#### Helper Functions

```python
def get_api_key(provider: str, cli_key: Optional[str]) -> Optional[str]:
    """Get API key from CLI arg or environment variable."""

def initialize_provider(args) -> LLMProvider:
    """Create provider instance from CLI arguments."""
```

## Testing Requirements

### Test Files

1. `tests/test_brain_interface.py` - Interface enforcement tests
2. `tests/test_brain_factory.py` - Factory function tests
3. `tests/test_brain_providers.py` - Provider implementation tests

### Test Coverage

- Interface cannot be instantiated directly
- Incomplete implementations raise `TypeError`
- Factory returns correct provider types
- Factory handles case-insensitive names
- Factory raises `ValueError` for unknown providers
- Providers format API calls correctly (with mocks)
- Providers parse responses correctly (with mocks)

## Dependencies

Add to `requirements.txt`:

```
openai>=1.0.0
google-generativeai>=0.3.0
tavily-python>=0.3.0
python-dotenv>=1.0.0
```

## Non-Functional Requirements

### Security

- API keys must be stored securely (environment variables preferred)
- No API keys in source code or logs
- Validate/sanitize all user inputs before sending to LLM

### Performance

- Implement timeout handling for API calls
- Consider rate limiting for production use
- Cache responses when appropriate

### Error Handling

- Graceful degradation when provider unavailable
- Clear error messages for missing API keys
- Handle network failures and API errors

## Future Enhancements

- Support for streaming responses
- Token usage tracking and limits
- Response caching layer
- Additional providers (Anthropic Claude, Cohere, etc.)
- Fine-tuned model support
- Batch processing capabilities

## Acceptance Criteria

- ✅ All tests pass (TDD approach)
- ✅ Interface properly enforces abstract methods
- ✅ Factory correctly instantiates all providers
- ✅ OpenAI provider successfully calls API (with mocks)
- ✅ Gemini provider successfully calls API (with mocks)
- ✅ VS Code provider can be instantiated
- ✅ CLI accepts and processes provider arguments
- ✅ Code passes linting (flake8, black, mypy)
- ✅ Documentation is complete and accurate
