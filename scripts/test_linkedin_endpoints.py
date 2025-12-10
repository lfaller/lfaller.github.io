#!/usr/bin/env python3
"""
Test various LinkedIn API endpoints to determine which ones are accessible.
"""

import os
import sys
import requests
from dotenv import load_dotenv

def test_endpoint(name, method, url, headers, payload=None):
    """Test a single endpoint and report results"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    print(f"URL: {url}")
    print(f"Method: {method}")

    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=payload, timeout=10)
        else:
            print(f"Unknown method: {method}")
            return

        print(f"Status: {response.status_code}")

        if response.status_code == 200 or response.status_code == 201:
            print(f"✓ ACCESSIBLE")
            try:
                data = response.json()
                print(f"Response (first 300 chars): {str(data)[:300]}")
            except:
                print(f"Response: {response.text[:300]}")
        elif response.status_code == 403:
            print(f"✗ FORBIDDEN (insufficient permissions)")
            try:
                data = response.json()
                print(f"  Error: {data.get('message')}")
            except:
                print(f"  Response: {response.text[:200]}")
        elif response.status_code == 404:
            print(f"✗ NOT FOUND (endpoint or resource doesn't exist)")
            try:
                data = response.json()
                print(f"  Error: {data.get('message')}")
            except:
                print(f"  Response: {response.text[:200]}")
        else:
            print(f"? UNEXPECTED STATUS")
            print(f"  Response: {response.text[:300]}")

    except Exception as e:
        print(f"✗ ERROR: {str(e)}")

def main():
    load_dotenv()
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    author_id = os.getenv('LINKEDIN_AUTHOR_ID')

    if not access_token:
        print("Error: LINKEDIN_ACCESS_TOKEN not set")
        sys.exit(1)

    if not author_id:
        print("Error: LINKEDIN_AUTHOR_ID not set")
        sys.exit(1)

    print(f"Testing LinkedIn API endpoints")
    print(f"Author ID: {author_id}")
    print(f"Token: {access_token[:30]}...")

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    # Test endpoints
    endpoints = [
        # Basic endpoints
        ("GET /me", "GET", "https://api.linkedin.com/v2/me", {}),

        # Posts endpoint (what we use for posting)
        ("GET /ugcPosts", "GET", "https://api.linkedin.com/v2/ugcPosts", {}),

        # Comments endpoint (what's failing)
        ("POST /comments (dummy)", "POST", "https://api.linkedin.com/v2/comments?action=create", {
            "object": "urn:li:share:0000000000000000000",
            "message": {"text": "Test"},
            "actor": author_id
        }),

        # Alternative comments endpoint format
        ("POST /comments (alt format)", "POST", "https://api.linkedin.com/v2/comments", {
            "object": "urn:li:share:0000000000000000000",
            "message": {"text": "Test"},
            "actor": author_id
        }),

        # Reactions endpoint (for comparison)
        ("POST /reactions", "POST", "https://api.linkedin.com/v2/reactions?action=create", {
            "object": "urn:li:share:0000000000000000000",
            "reactionType": "LIKE",
            "actor": author_id
        }),
    ]

    for name, method, url, payload in endpoints:
        test_endpoint(name, method, url, headers, payload if payload else None)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print("\nIf /comments endpoint returns 403, you need:")
    print("  → Add 'Community Management API' OR")
    print("  → Request access to a Social API product that includes comments")
    print("\nIf /comments endpoint returns 404 with correct URN:")
    print("  → The endpoint URL might be wrong, or")
    print("  → Your app tier doesn't support comments")
    print("\nTry adding one of these products:")
    print("  - Community Management API (Development Tier)")
    print("  - Request access to 'Share on LinkedIn' for comments feature")

if __name__ == '__main__':
    main()
