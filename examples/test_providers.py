#!/usr/bin/env python3
"""
Test script for LLM providers.

This script tests the different LLM providers to ensure they work correctly.
Run with different providers using the --provider flag.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.brain import get_provider, list_providers


def test_text_generation(provider_name: str):
    """Test basic text generation."""
    print(f"\n{'='*60}")
    print(f"Testing {provider_name.upper()} Provider - Text Generation")
    print(f"{'='*60}\n")
    
    try:
        provider = get_provider(provider_name)
        print(f"✓ Provider initialized successfully")
        
        # Test simple generation
        prompt = "What are the key principles of secure authentication?"
        print(f"\nPrompt: {prompt}")
        print("\nGenerating response...")
        
        response = provider.generate(prompt, system_prompt="You are a helpful technical assistant.")
        if len(response) > 500:
            print(f"\nResponse:\n{response[:500]}...")
        else:
            print(f"\nResponse:\n{response}")
        
        print(f"\n✓ Text generation successful")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def test_json_generation(provider_name: str):
    """Test JSON generation."""
    print(f"\n{'='*60}")
    print(f"Testing {provider_name.upper()} Provider - JSON Generation")
    print(f"{'='*60}\n")
    
    try:
        provider = get_provider(provider_name)
        
        # Test JSON generation
        prompt = "List 3 best practices for API security"
        schema = {
            "practices": [
                {
                    "name": "string",
                    "description": "string"
                }
            ]
        }
        
        print(f"Prompt: {prompt}")
        print(f"Schema: {schema}")
        print("\nGenerating JSON response...")
        
        response = provider.generate_json(prompt, schema)
        print(f"\nResponse:")
        import json
        print(json.dumps(response, indent=2))
        
        print(f"\n✓ JSON generation successful")
        return True
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False


def main():
    """Main test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test LLM providers')
    parser.add_argument(
        '--provider',
        choices=list_providers(),
        default='openai',
        help='Provider to test'
    )
    parser.add_argument(
        '--test',
        choices=['text', 'json', 'all'],
        default='all',
        help='Which test to run'
    )
    
    args = parser.parse_args()
    
    print(f"\nAvailable providers: {', '.join(list_providers())}")
    print(f"Testing provider: {args.provider}")
    
    results = []
    
    if args.test in ['text', 'all']:
        results.append(('text_generation', test_text_generation(args.provider)))
    
    if args.test in ['json', 'all']:
        results.append(('json_generation', test_json_generation(args.provider)))
    
    # Print summary
    print(f"\n{'='*60}")
    print("Test Summary")
    print(f"{'='*60}")
    
    for test_name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    # Exit with appropriate code
    all_passed = all(success for _, success in results)
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()
