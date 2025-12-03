# Brain Module - LLM Provider Architecture

The Brain module provides a modular, pluggable interface for different LLM providers following the Strategy Pattern and supporting "Bring Your Own Key" (BYOK).

## Overview

This module implements a provider architecture that allows the RJW-IDD Agent to work with multiple LLM providers:

- **OpenAI** (GPT-4, GPT-3.5, etc.)
- **Google Gemini** (Gemini Pro, Gemini Flash, etc.)
- **VS Code Bridge** (for integration with VS Code's Language Model API)

## Architecture

### Strategy Pattern

The module uses the Strategy Pattern to allow runtime selection of LLM providers:

```
LLMProvider (Interface)
    ├── OpenAIProvider
    ├── GeminiProvider
    └── VSCodeBridgeProvider
```

### Factory Pattern

The `get_provider()` factory function instantiates the appropriate provider based on configuration:

```python
from src.brain import get_provider

# Use default provider (or RJW_PROVIDER env var)
provider = get_provider()

# Explicitly choose a provider
provider = get_provider('gemini')

# Pass custom configuration
provider = get_provider('openai', model='gpt-4-turbo')
```

## Usage

### Basic Text Generation

```python
from src.brain import get_provider

provider = get_provider('openai')
response = provider.generate(
    prompt="What are the key principles of secure authentication?",
    system_prompt="You are a helpful technical assistant."
)
print(response)
```

### Structured JSON Output

```python
from src.brain import get_provider

provider = get_provider('gemini')
schema = {
    "practices": [
        {
            "name": "string",
            "description": "string"
        }
    ]
}

response = provider.generate_json(
    prompt="List 3 best practices for API security",
    schema=schema
)
print(response)  # Returns a dictionary
```

### CLI Integration

The Brain module is integrated into the CLI via the `--provider` flag:

```bash
# Use OpenAI (default)
rjw chat

# Use Gemini
rjw --provider gemini chat

# Use VS Code Bridge
rjw --provider vscode run "Add authentication"
```

## Configuration

### Environment Variables

Each provider requires its own API key via environment variables:

- **OpenAI**: `OPENAI_API_KEY`
- **Gemini**: `GEMINI_API_KEY`
- **Tavily** (for research): `TAVILY_API_KEY`

You can also set the default provider:

- **Default Provider**: `RJW_PROVIDER` (choices: `openai`, `gemini`, `vscode`)

### Using .env Files

The factory automatically loads environment variables from `.env` files using `python-dotenv`:

```bash
# .env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
TAVILY_API_KEY=...
RJW_PROVIDER=openai
```

## Provider Details

### OpenAI Provider

- **Default Model**: `gpt-4o`
- **Features**: Text generation, JSON mode
- **Configuration**: Set `OPENAI_API_KEY`

### Gemini Provider

- **Default Model**: `gemini-1.5-pro`
- **Features**: Text generation, JSON extraction
- **Configuration**: Set `GEMINI_API_KEY`

### VS Code Bridge Provider

- **Purpose**: Integration with VS Code Language Model API
- **Protocol**: Bridge communication via stdin/stdout
- **Use Case**: When running as a subprocess within VS Code extension

The VS Code Bridge uses a special protocol:

1. CLI prints: `[REQUEST_LM_GENERATION] <json_payload>`
2. Extension intercepts and calls VS Code LM API
3. Extension responds: `[RESPONSE_LM_GENERATION] <json_payload>`
4. CLI parses response and continues

## Integration Points

### ResearchHarvester

The `ResearchHarvester` uses the LLM provider for:

- Conducting web research with Tavily + LLM summarization
- Extracting insights from search results
- Generating evidence summaries

### PromptOptimizer

The `PromptOptimizer` uses the LLM provider for:

- Extracting research topics from user input
- Analyzing user requirements
- Intelligent workflow orchestration

## Graceful Degradation

The framework maintains backward compatibility when LLM providers are unavailable:

- Falls back to keyword-based topic extraction
- Uses simulated research output
- Continues to generate evidence files with reduced intelligence

This ensures the tool remains functional for testing, development, and users who don't have API keys configured.

## Testing

Test the providers using the included test script:

```bash
# Test OpenAI provider
python examples/test_providers.py --provider openai

# Test Gemini provider
python examples/test_providers.py --provider gemini

# Test specific functionality
python examples/test_providers.py --provider openai --test json
```

## Error Handling

All providers implement consistent error handling:

- Invalid API keys → Clear error message with setup instructions
- API failures → Exception with descriptive error
- JSON parsing failures → Exception with content preview

## Extending

To add a new provider:

1. Create a new file in `src/brain/providers/`
2. Implement the `LLMProvider` interface
3. Add the provider to `factory.py`
4. Update this documentation

Example:

```python
# src/brain/providers/claude.py
from ..interface import LLMProvider

class ClaudeProvider(LLMProvider):
    def __init__(self, model: str = "claude-3-opus", api_key: str = None):
        # Implementation
        pass
    
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        # Implementation
        pass
    
    def generate_json(self, prompt: str, schema: dict) -> dict:
        # Implementation
        pass
```

## Dependencies

- `openai>=1.0.0` - OpenAI API client
- `google-generativeai>=0.3.0` - Google Gemini API client
- `tavily-python>=0.3.0` - Tavily search API client
- `python-dotenv>=1.0.0` - Environment variable management
