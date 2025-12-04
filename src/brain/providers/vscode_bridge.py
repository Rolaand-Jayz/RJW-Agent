"""
VS Code Bridge LLM Provider.

Implements a bridge mechanism for VS Code integration.
Since this is a Python CLI that cannot directly call VS Code APIs,
it uses a special protocol to communicate with a wrapper extension.
"""
import json
import select
import sys
from typing import Optional

from ..interface import LLMProvider


class VSCodeBridgeProvider(LLMProvider):
    """
    VS Code Bridge implementation of LLMProvider.
    
    This provider implements a bridge protocol for VS Code integration:
    1. Prints a special token to stdout: [REQUEST_LM_GENERATION] <json_payload>
    2. Pauses execution and waits for response on stdin
    3. Parses the response and returns it
    
    This allows a VS Code extension wrapper to:
    - Monitor stdout for the special token
    - Intercept the request payload
    - Call VS Code's LM API
    - Pipe the response back via stdin
    
    **Security Warning**: Prompt data is printed to stdout without sanitization.
    Do not include sensitive information (API keys, credentials, PII) in prompts
    when using the VS Code Bridge provider, as they will be exposed in logs and
    console output.
    
    Attributes:
        timeout: Optional timeout in seconds for waiting for response
    """
    
    def __init__(self, timeout: Optional[int] = 30):
        """
        Initialize VS Code Bridge provider.
        
        Args:
            timeout: Timeout in seconds for waiting for response (default: 30)
        """
        self.timeout = timeout
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Generate text completion via VS Code Bridge.
        
        Sends a request to the VS Code extension and waits for response.
        
        Args:
            prompt: User prompt/query
            system_prompt: Optional system instructions
            
        Returns:
            Generated text response from VS Code LM API
            
        Raises:
            Exception: If communication fails or response is invalid
        """
        request = {
            "type": "text_generation",
            "prompt": prompt,
            "system_prompt": system_prompt
        }
        
        return self._send_request(request)
    
    def generate_json(self, prompt: str, schema: dict) -> dict:
        """
        Generate structured JSON output via VS Code Bridge.
        
        Args:
            prompt: User prompt requesting structured data
            schema: Expected JSON structure description
            
        Returns:
            Dictionary containing structured response
            
        Raises:
            Exception: If communication fails or response is not valid JSON
        """
        request = {
            "type": "json_generation",
            "prompt": prompt,
            "schema": schema
        }
        
        response_text = self._send_request(request)
        
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response from VS Code: {str(e)}")
    
    def _send_request(self, request: dict) -> str:
        """
        Send request to VS Code extension via bridge protocol.
        
        Protocol:
        1. Print special token + JSON payload to stdout
        2. Flush stdout to ensure immediate delivery
        3. Wait for response on stdin
        4. Parse and return response
        
        Args:
            request: Request payload dictionary
            
        Returns:
            Response text from VS Code
            
        Raises:
            Exception: If communication fails
        """
        try:
            # Encode request as JSON
            payload = json.dumps(request)
            
            # Print special token + payload to stdout
            # VS Code extension should monitor for this pattern
            print(f"[REQUEST_LM_GENERATION] {payload}", flush=True)
            
            # Wait for response on stdin with timeout
            # Use select for Unix-like systems (works on Linux, macOS)
            if hasattr(select, 'select'):
                # Unix/Linux/macOS implementation
                ready, _, _ = select.select([sys.stdin], [], [], self.timeout)
                if not ready:
                    raise TimeoutError(
                        f"No response received from VS Code extension within {self.timeout} seconds. "
                        "Ensure the VS Code extension is running and monitoring stdout."
                    )
                response_line = sys.stdin.readline()
            else:
                # Windows implementation using threading for timeout
                import threading
                response_container = []
                
                def read_line():
                    response_container.append(sys.stdin.readline())
                
                thread = threading.Thread(target=read_line, daemon=True)
                thread.start()
                thread.join(timeout=self.timeout)
                
                if not response_container:
                    raise TimeoutError(
                        f"No response received from VS Code extension within {self.timeout} seconds. "
                        "Ensure the VS Code extension is running and monitoring stdout."
                    )
                response_line = response_container[0]
            
            if not response_line:
                raise Exception("No response received from VS Code extension")
            
            # Parse response
            # Expected format: [RESPONSE_LM_GENERATION] <json_payload>
            if not response_line.startswith("[RESPONSE_LM_GENERATION]"):
                raise Exception(
                    f"Invalid response format from VS Code extension: {response_line[:100]}"
                )
            
            # Extract payload
            response_json = response_line[len("[RESPONSE_LM_GENERATION]"):].strip()
            response_data = json.loads(response_json)
            
            # Check for errors
            if response_data.get("error"):
                raise Exception(f"VS Code LM API error: {response_data['error']}")
            
            # Return the generated content
            return response_data.get("content", "")
        
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse VS Code response: {str(e)}")
        except Exception as e:
            raise Exception(f"VS Code Bridge communication error: {str(e)}")
