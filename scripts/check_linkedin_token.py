#!/usr/bin/env python3
"""
Check LinkedIn API token scopes and verify comment endpoint access.
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

def check_token_info(access_token):
    """Check token validity and scopes using the introspect endpoint"""
    print("=" * 60)
    print("CHECKING LINKEDIN TOKEN INFORMATION")
    print("=" * 60)

    # Check token status via introspection endpoint
    url = "https://api.linkedin.com/oauth/v2/introspectToken"

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    params = {
        'token': access_token
    }

    print("\n1. Checking token validity and scopes...")
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"✓ Token is valid")
        print(f"  Status: {data.get('status')}")
        print(f"  Expires in: {data.get('expires_in')} seconds")
        if 'scope' in data:
            scopes = data.get('scope', '').split(' ')
            print(f"\n  Authorized Scopes:")
            for scope in scopes:
                if scope:
                    print(f"    - {scope}")
    else:
        print(f"✗ Token check failed: {response.status_code}")
        print(f"  Response: {response.text[:500]}")
        return False

    return data

def test_comment_endpoint(author_id, access_token):
    """Try to test the comment endpoint with a dummy post"""
    print("\n" + "=" * 60)
    print("TESTING COMMENT ENDPOINT ACCESS")
    print("=" * 60)

    # Use a test post URN format
    test_post_urn = "urn:li:share:0000000000000000000"

    url = "https://api.linkedin.com/v2/comments?action=create"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    payload = {
        "object": test_post_urn,
        "message": {
            "text": "Test comment"
        },
        "actor": author_id
    }

    print(f"\nAttempting to reach comment endpoint...")
    print(f"  URL: {url}")
    print(f"  Method: POST")
    print(f"  Test Post URN: {test_post_urn}")

    response = requests.post(url, headers=headers, json=payload)

    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Headers:")
    for key, value in response.headers.items():
        if key.lower() not in ['authorization', 'cookie', 'set-cookie']:
            print(f"  {key}: {value}")

    print(f"\nResponse Body (first 500 chars):")
    print(f"  {response.text[:500]}")

    # Analyze the response
    print(f"\nAnalysis:")
    if response.status_code == 404:
        print(f"  ✗ 404 Not Found - The endpoint or post doesn't exist")
        print(f"    This could indicate:")
        print(f"      1. Wrong URN format")
        print(f"      2. Token lacks comment permissions")
        print(f"      3. Endpoint URL is incorrect")
    elif response.status_code == 403:
        print(f"  ✗ 403 Forbidden - Token lacks required permissions")
        print(f"    Check if your app has 'w_member_social' scope")
    elif response.status_code == 401:
        print(f"  ✗ 401 Unauthorized - Token is invalid or expired")
    elif response.status_code == 201:
        print(f"  ✓ 201 Created - Comment endpoint is accessible!")
    else:
        print(f"  ? {response.status_code} - Unexpected response code")

    return response

def check_me_endpoint(access_token):
    """Check what the token has access to via /me endpoint"""
    print("\n" + "=" * 60)
    print("CHECKING TOKEN ACCESS VIA /ME ENDPOINT")
    print("=" * 60)

    url = "https://api.linkedin.com/v2/me"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    print(f"\nFetching /me endpoint...")
    response = requests.get(url, headers=headers)

    print(f"Response Status: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print(f"✓ Successfully retrieved profile information")
        print(f"  ID: {data.get('id')}")
        print(f"  Full data: {json.dumps(data, indent=2)[:500]}")
    else:
        print(f"✗ Failed to access /me endpoint")
        print(f"  Response: {response.text[:500]}")

def main():
    load_dotenv()
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    author_id = os.getenv('LINKEDIN_AUTHOR_ID')

    if not access_token:
        print("Error: LINKEDIN_ACCESS_TOKEN not set in environment")
        sys.exit(1)

    if not author_id:
        print("Error: LINKEDIN_AUTHOR_ID not set in environment")
        sys.exit(1)

    print(f"Author ID: {author_id}")
    print(f"Token (first 20 chars): {access_token[:20]}...")

    # Run all checks
    token_info = check_token_info(access_token)
    check_me_endpoint(access_token)
    response = test_comment_endpoint(author_id, access_token)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("\nIf you're seeing 404 errors on the comment endpoint, it likely means:")
    print("1. Your token doesn't have 'w_member_social' scope")
    print("2. The comment API endpoint URL or format is incorrect")
    print("3. There's an API version mismatch")
    print("\nTry regenerating your token with these scopes:")
    print("  - openid")
    print("  - profile")
    print("  - w_member_social")

if __name__ == '__main__':
    main()
