#!/usr/bin/env python3
"""
Bearer Token Generator for MCP Inspector Testing

This script generates a valid bearer token for testing the MCP server with
MCP Inspector. The token includes a server secret and optional user identity.

Usage:
    python examples/create_bearer_token.py
    python examples/create_bearer_token.py --email trader@company.com
    python examples/create_bearer_token.py --with-connectors
"""

import argparse
import base64
import json
import sys
from typing import Dict, Optional

try:
    import jwt
except ImportError:
    print("Error: PyJWT not installed. Install with: pip install pyjwt")
    sys.exit(1)


def create_user_id_token(email: str, secret: str = "test-secret") -> str:
    """
    Create a JWT token for user identity.
    
    Args:
        email: User email address
        secret: Secret key for signing JWT (for demo/testing only)
    
    Returns:
        Encoded JWT token
    """
    payload = {
        "email": email,
        # Add other claims as needed for testing
        "sub": email,
        "iat": 1234567890,  # Issued at (timestamp) - fixed for demo
    }
    
    # Sign the JWT (using HS256 for simplicity in demo)
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token


def create_bearer_token(
    server_secret: str,
    user_email: Optional[str] = None,
    connector_tokens: Optional[Dict[str, str]] = None
) -> str:
    """
    Create a bearer token for MCP authentication.
    
    The bearer token is a Base64-encoded JSON object containing:
    - server_secret: Required for server authentication
    - user_id_token: Optional JWT for user identity
    - connector_access_tokens: Optional OAuth tokens for third-party services
    
    Args:
        server_secret: Server secret key
        user_email: Optional user email for identity
        connector_tokens: Optional dict of connector names to OAuth tokens
    
    Returns:
        Base64-encoded bearer token
    """
    # Build the auth payload
    auth_payload = {
        "server_secret": server_secret
    }
    
    # Add user identity if provided
    if user_email:
        user_id_token = create_user_id_token(user_email)
        auth_payload["user_id_token"] = user_id_token
    
    # Add connector tokens if provided
    if connector_tokens:
        auth_payload["connector_access_tokens"] = connector_tokens
    
    # Encode as JSON
    json_str = json.dumps(auth_payload)
    
    # Encode as Base64
    token_bytes = json_str.encode('utf-8')
    base64_token = base64.b64encode(token_bytes).decode('utf-8')
    
    return base64_token


def main():
    """Main entry point for bearer token generator."""
    parser = argparse.ArgumentParser(
        description="Generate bearer token for MCP Inspector testing"
    )
    parser.add_argument(
        "--server-secret",
        type=str,
        default="demo-secret-key",
        help="Server secret (default: demo-secret-key)"
    )
    parser.add_argument(
        "--email",
        type=str,
        default=None,
        help="User email for identity (optional)"
    )
    parser.add_argument(
        "--with-connectors",
        action="store_true",
        help="Include sample connector tokens (google, slack)"
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default=None,
        help="Save token to file instead of printing"
    )
    
    args = parser.parse_args()
    
    # Build connector tokens if requested
    connector_tokens = None
    if args.with_connectors:
        connector_tokens = {
            "google": "sample-google-oauth-token",
            "slack": "sample-slack-oauth-token"
        }
    
    # Generate token
    bearer_token = create_bearer_token(
        server_secret=args.server_secret,
        user_email=args.email,
        connector_tokens=connector_tokens
    )
    
    # Output results
    print("=" * 70)
    print("Bearer Token Generated Successfully")
    print("=" * 70)
    print(f"\nServer Secret: {args.server_secret}")
    if args.email:
        print(f"User Email: {args.email}")
    if connector_tokens:
        print(f"Connectors: {', '.join(connector_tokens.keys())}")
    print("\n" + "=" * 70)
    print("Bearer Token (use in MCP Inspector):")
    print("=" * 70)
    print(bearer_token)
    print("=" * 70)
    
    # Save to file if requested
    if args.output_file:
        try:
            with open(args.output_file, 'w') as f:
                f.write(bearer_token)
            print(f"\n✓ Token saved to: {args.output_file}")
        except Exception as e:
            print(f"\n✗ Failed to save token: {e}", file=sys.stderr)
            sys.exit(1)
    
    # Usage instructions
    print("\nUsage in MCP Inspector:")
    print("1. Transport Type: Streamable HTTP")
    print("2. URL: http://localhost:5222/mcp")
    print("3. Authentication → Bearer token: [paste token above]")
    print("4. Click 'Connect'")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()

