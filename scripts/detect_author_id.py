#!/usr/bin/env python3
"""
Detect your LinkedIn Author ID using the w_member_social scope

This script makes a test API call to discover your author URN.
"""

import sys
import requests
import json

def detect_author_id(access_token):
    """Try to detect the author ID using various LinkedIn API endpoints"""

    print("="*60)
    print("LinkedIn Author ID Detector")
    print("="*60)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    # Method 1: Try to get profile info (may fail with 403)
    print("\nAttempting Method 1: Profile API...")
    try:
        response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
        if response.status_code == 200:
            data = response.json()
            person_id = data.get('id')
            if person_id:
                author_urn = f"urn:li:person:{person_id}"
                print_success(author_urn, data)
                return author_urn
        else:
            print(f"  Status: {response.status_code} - {response.text[:100]}")
    except Exception as e:
        print(f"  Failed: {e}")

    # Method 2: Introspect the token itself
    print("\nAttempting Method 2: Token Introspection...")
    print("  (This will tell us what user the token belongs to)")

    # LinkedIn doesn't have a standard introspection endpoint, but we can try
    # to make a minimal UGC post request that will fail but reveal the author

    print("\nAttempting Method 3: Make a test UGC share request...")
    print("  (We'll use an invalid format that won't actually post)")

    test_payload = {
        "author": "urn:li:person:UNKNOWN",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": "Test"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    try:
        response = requests.post(
            'https://api.linkedin.com/v2/ugcPosts',
            headers=headers,
            json=test_payload
        )

        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.text[:500]}")

        # The error might contain info about the correct author ID
        if 'author' in response.text.lower():
            print("\n  The error message might contain clues about your author ID.")
            print("  Look for any URN format like 'urn:li:person:XXXXX'")

    except Exception as e:
        print(f"  Failed: {e}")

    # Method 4: Check if we can get it from userinfo (OpenID)
    print("\nAttempting Method 4: OpenID UserInfo endpoint...")
    try:
        response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)
        if response.status_code == 200:
            data = response.json()
            person_id = data.get('sub')
            if person_id:
                author_urn = f"urn:li:person:{person_id}"
                print_success(author_urn, data)
                return author_urn
        else:
            print(f"  Status: {response.status_code}")
    except Exception as e:
        print(f"  Failed: {e}")

    print("\n" + "="*60)
    print("UNABLE TO AUTO-DETECT AUTHOR ID")
    print("="*60)
    print("\nUnfortunately, the w_member_social scope alone doesn't provide")
    print("access to your profile information.")
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("\n1. Try reaching out to LinkedIn Developer Support")
    print("2. Look in your LinkedIn profile URL")
    print("   Example: linkedin.com/in/USERNAME")
    print("\n3. OR: Create a test post manually and inspect it:")
    print("   - Make a post on LinkedIn")
    print("   - Use browser dev tools to inspect the API call")
    print("   - Look for 'urn:li:person:XXXXX' in the request")
    print("\n" + "="*60 + "\n")

    return None

def print_success(author_urn, data=None):
    """Print success message with author URN"""
    print("\n" + "="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print(f"\nYour LinkedIn Author ID is:")
    print(f"\n  {author_urn}")
    print(f"\nAdd this to your scripts/.env file:")
    print(f"\n  LINKEDIN_AUTHOR_ID={author_urn}")
    print("\n" + "="*60)

    if data:
        print("\nProfile information:")
        for key, value in data.items():
            if key not in ['id', 'sub']:
                print(f"  {key}: {value}")

    print("="*60 + "\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python detect_author_id.py YOUR_ACCESS_TOKEN")
        print("\nExample:")
        print("  python detect_author_id.py AQVEg9hyftCm...")
        sys.exit(1)

    access_token = sys.argv[1]

    if len(access_token) < 20:
        print("Error: Access token appears invalid (too short)")
        sys.exit(1)

    detect_author_id(access_token)

if __name__ == '__main__':
    main()
