# DEC-0005: Modular Brain Architecture with Strategy Pattern

**Status:** Accepted  
**Date:** 2025-12-04  
**Deciders:** Development Team  
**Related:** SPEC-0001-brain-architecture.md

## Context

The RJW-Agent framework requires integration with Large Language Models (LLMs) to provide intelligent assistance for code generation, analysis, and decision-making. Users need flexibility to:

1. **Bring Your Own Key (BYOK):** Use their own API keys with different LLM providers
2. **Provider Choice:** Select from multiple LLM providers (OpenAI, Google Gemini, VS Code Copilot, etc.)
3. **Consistent Interface:** Have a uniform way to interact with different providers
4. **Extensibility:** Easily add new providers without modifying existing code

The challenge is designing an architecture that supports multiple providers while maintaining clean, testable code that adheres to SOLID principles.

## Decision

We will implement the "Brain" module using the **Strategy Pattern** with the following design:

### 1. Abstract Base Class (Interface)
- Create `LLMProvider` abstract base class using Python's `ABC` module
- Define standard methods: `generate()` and `generate_json()`
- All provider implementations must inherit from this interface

### 2. Provider Factory
- Implement `get_provider()` factory function to instantiate providers
- Support provider selection via string identifier (e.g., "openai", "gemini")
- Handle provider-specific initialization (API keys, configuration)

### 3. Concrete Implementations
- `OpenAIProvider`: Integration with OpenAI GPT models
- `GeminiProvider`: Integration with Google Gemini models
- `VSCodeBridgeProvider`: Bridge for VS Code Copilot integration

### 4. CLI Integration
- Add command-line arguments: `--provider`, `--api-key`, `--model`
- Environment variable support for API keys
- Provider initialization in CLI main

## Consequences

### Positive
- ✅ **Extensibility:** New providers can be added without modifying existing code
- ✅ **Testability:** Each provider can be tested independently with mocks
- ✅ **BYOK Support:** Users can use their own API keys
- ✅ **Flexibility:** Easy to switch between providers at runtime
- ✅ **SOLID Principles:** Adheres to Open/Closed and Dependency Inversion principles
- ✅ **Type Safety:** Abstract base class ensures consistent interface

### Negative
- ⚠️ **Initial Complexity:** More files and structure than a monolithic approach
- ⚠️ **Learning Curve:** Developers need to understand the Strategy Pattern
- ⚠️ **Dependency Management:** Multiple provider SDKs need to be maintained

### Risks & Mitigation
- **Risk:** Provider API changes break integration
  - *Mitigation:* Pin dependency versions, comprehensive tests
- **Risk:** Inconsistent behavior across providers
  - *Mitigation:* Standardized interface contract, integration tests
- **Risk:** API key security concerns
  - *Mitigation:* Environment variables, secure storage, documentation

## Alternatives Considered

### Alternative 1: Monolithic LLM Client
- Single class with if/else statements for different providers
- **Rejected:** Violates Open/Closed principle, difficult to test and extend

### Alternative 2: Adapter Pattern
- Individual adapter classes wrapping each provider SDK
- **Rejected:** More overhead than Strategy Pattern for this use case

### Alternative 3: Plugin System
- Dynamic loading of provider plugins at runtime
- **Rejected:** Unnecessary complexity for initial implementation

## Implementation Notes

- Follow Test-Driven Development (TDD) methodology
- Tests must be written BEFORE implementation (RED → GREEN → REFACTOR)
- Use mocking for external API calls in tests
- Document provider-specific behavior and limitations
- Include examples in documentation

## References

- [Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Strategy_pattern)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Google Gemini API Documentation](https://ai.google.dev/api/rest)
- [Python ABC Module](https://docs.python.org/3/library/abc.html)
