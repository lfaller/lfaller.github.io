#!/usr/bin/env python3
"""
Test LinkedIn posting and extract member ID from error response

This script attempts to post with different URN formats to discover
the correct member ID format that LinkedIn expects.
"""

import sys
import requests
import json
import os
from dotenv import load_dotenv

def test_post_with_urn(access_token, author_urn):
    """Attempt to post with a given URN and analyze the response"""

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": "Test post - please ignore (will delete shortly)"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    print(f"\nTesting with URN: {author_urn}")
    print("-" * 60)

    response = requests.post(url, headers=headers, json=payload)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    return response

def main():
    # Load environment variables
    load_dotenv('/Users/linafaller/repos/lfaller.github.io/scripts/.env')

    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    author_id = os.getenv('LINKEDIN_AUTHOR_ID')

    if not access_token:
        print("Error: LINKEDIN_ACCESS_TOKEN not found in .env file")
        sys.exit(1)

    print("=" * 60)
    print("LinkedIn Member ID Finder")
    print("=" * 60)
    print("\nThis script will attempt different URN formats to find")
    print("the correct member ID.\n")

    # Try the current author ID from .env
    if author_id:
        print(f"Found LINKEDIN_AUTHOR_ID in .env: {author_id}")
        test_post_with_urn(access_token, author_id)

    # Try converting to member URN
    if author_id and 'ACoAAAERPDoBimyT2I0gXmYOPhXW7D7jDTpnNCY' in author_id:
        print("\n" + "=" * 60)
        print("Trying with urn:li:member format...")
        print("=" * 60)
        member_urn = "urn:li:member:ACoAAAERPDoBimyT2I0gXmYOPhXW7D7jDTpnNCY"
        test_post_with_urn(access_token, member_urn)

    # Check token scopes
    print("\n" + "=" * 60)
    print("Checking Token Scopes")
    print("=" * 60)

    # Try to introspect token (if LinkedIn supports it)
    introspect_url = "https://api.linkedin.com/oauth/v2/introspectToken"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(introspect_url, headers=headers)
    print(f"\nToken introspection status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Response: {response.text}")

    print("\n" + "=" * 60)
    print("RECOMMENDATION")
    print("=" * 60)
    print("\nIf all attempts failed with 403 or 422 errors:")
    print("\n1. Verify your OAuth token was generated with these scopes:")
    print("   - openid")
    print("   - profile")
    print("   - w_member_social")
    print("\n2. The token might need to be regenerated after adding")
    print("   the OpenID Connect product to your app")
    print("\n3. After regenerating, try this endpoint directly:")
    print("   curl -H 'Authorization: Bearer YOUR_TOKEN' \\")
    print("        https://api.linkedin.com/v2/userinfo")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    main()
