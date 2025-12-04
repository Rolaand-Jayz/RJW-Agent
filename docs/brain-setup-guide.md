# Brain Setup Guide

This guide will help you set up and use the Brain provider architecture in the RJW-IDD Agent.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs the necessary LLM provider libraries:
- `openai` - For OpenAI/GPT models
- `google-generativeai` - For Google Gemini models
- `tavily-python` - For web research
- `python-dotenv` - For environment variable management

### 2. Get API Keys

You'll need API keys for the providers you want to use:

#### OpenAI (Default Provider)
1. Sign up at [platform.openai.com](https://platform.openai.com)
2. Create an API key in your account settings
3. Copy the key (starts with `sk-...`)

#### Google Gemini
1. Sign up at [ai.google.dev](https://ai.google.dev)
2. Get an API key from Google AI Studio
3. Copy the key

#### Tavily (For Research)
1. Sign up at [tavily.com](https://tavily.com)
2. Get an API key from your dashboard
3. Copy the key

### 3. Configure Environment Variables

Create a `.env` file in your project root:

```bash
# .env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...
TAVILY_API_KEY=...

# Optional: Set default provider
RJW_PROVIDER=openai
```

**Important:** Add `.env` to your `.gitignore` to avoid committing secrets!

### 4. Test Your Setup

Test that everything works:

```bash
# Test OpenAI
python examples/test_providers.py --provider openai

# Test Gemini
python examples/test_providers.py --provider gemini
```

## Using the Brain in CLI

### Basic Usage

```bash
# Use default provider (OpenAI)
rjw chat

# Explicitly choose a provider
rjw --provider gemini chat

# One-shot commands with specific provider
rjw --provider openai run "Add authentication to user API"
```

### Provider Selection Priority

The provider is selected in this order:
1. CLI flag: `--provider openai`
2. Environment variable: `RJW_PROVIDER=gemini`
3. Default: `openai`

## Provider Comparison

### OpenAI (Recommended)
- **Model**: gpt-4o (default)
- **Strengths**: Best overall quality, JSON mode support
- **Cost**: Moderate
- **Speed**: Fast
- **Best For**: Production use, complex reasoning

### Gemini
- **Model**: gemini-1.5-pro (default)
- **Strengths**: Fast, cost-effective, large context
- **Cost**: Lower than OpenAI
- **Speed**: Very fast
- **Best For**: Development, large documents

### VS Code Bridge
- **Purpose**: Integration with VS Code
- **Strengths**: Uses VS Code's built-in LM API
- **Cost**: Free (depends on VS Code configuration)
- **Speed**: Depends on VS Code backend
- **Best For**: VS Code extension development

## Advanced Configuration

### Custom Models

You can customize the model used by each provider:

```python
from src.brain import get_provider

# Use a specific OpenAI model
provider = get_provider('openai', model='gpt-4-turbo')

# Use a specific Gemini model
provider = get_provider('gemini', model='gemini-1.5-flash')
```

### Programmatic Usage

Use the Brain in your own Python code:

```python
from src.brain import get_provider

# Initialize provider
provider = get_provider('openai')

# Generate text
response = provider.generate(
    prompt="What are secure authentication patterns?",
    system_prompt="You are a security expert."
)

# Generate structured data
result = provider.generate_json(
    prompt="List 3 API security best practices",
    schema={
        "type": "object",
        "properties": {
            "practices": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
)
```

## Troubleshooting

### "OpenAI API key not found"

**Solution:** Set the `OPENAI_API_KEY` environment variable or create a `.env` file.

### "Failed to initialize LLM provider"

**Symptoms:** Warnings in output, fallback to keyword-based extraction

**Solution:** 
1. Check that your API key is valid
2. Verify the API key environment variable name
3. Ensure the provider package is installed (`pip install openai`)

### "Tavily API key not found"

**Impact:** Research will use simulated output instead of real web search

**Solution:** Set `TAVILY_API_KEY` if you want real research capabilities

### Rate Limiting

If you hit rate limits:
1. Reduce request frequency
2. Upgrade your API plan
3. Switch to a different provider temporarily

## Working Without API Keys

The RJW-IDD Agent gracefully degrades when API keys are not configured:

- **Topic Extraction**: Falls back to keyword matching
- **Research**: Uses simulated output
- **Evidence Generation**: Creates valid EVD files with less intelligence

This allows you to:
- Test the tool without API keys
- Develop features without costs
- Onboard users gradually

## Security Best Practices

1. **Never commit API keys** - Use `.env` files and `.gitignore`
2. **Rotate keys regularly** - Change keys periodically
3. **Use separate keys for dev/prod** - Don't share keys across environments
4. **Monitor usage** - Check API dashboards for unexpected usage
5. **Set spending limits** - Configure billing alerts

## Cost Management

### OpenAI
- GPT-4o: See [OpenAI pricing](https://openai.com/pricing) for current rates
- Set monthly spending limits in OpenAI dashboard
- Monitor usage at [platform.openai.com/usage](https://platform.openai.com/usage)

### Gemini
- See [Google AI pricing](https://ai.google.dev/pricing) for current rates and free tier details
- Rate limits are generous in free tier

### Tavily
- Free tier: 1000 searches/month
- Paid: $0.003 per search
- Check usage at [tavily.com/dashboard](https://tavily.com/dashboard)

## Getting Help

- **Documentation**: See `src/brain/README.md`
- **Examples**: Check `examples/test_providers.py`
- **Issues**: Report at [GitHub Issues](https://github.com/Rolaand-Jayz/RJW-Agent/issues)

## Next Steps

1. Set up your preferred provider
2. Test with `examples/test_providers.py`
3. Try the interactive CLI: `rjw --provider openai chat`
4. Experiment with different providers to find what works best for you
