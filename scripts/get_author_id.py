#!/usr/bin/env python3
"""
Helper script to get your LinkedIn Author ID

Usage:
    python get_author_id.py YOUR_ACCESS_TOKEN

This will fetch your LinkedIn profile information and display your author ID
in the format needed for the .env file.
"""

import sys
import requests

def get_author_id(access_token):
    """Fetch LinkedIn author ID using the access token"""

    # Method 1: Try userinfo endpoint (requires r_liteprofile or r_basicprofile)
    print("Attempting to fetch your LinkedIn author ID...")
    print("\nMethod 1: Trying v2/userinfo endpoint...")

    url = "https://api.linkedin.com/v2/userinfo"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            person_id = data.get('sub')

            if person_id:
                author_urn = f"urn:li:person:{person_id}"
                print("\n" + "="*60)
                print("SUCCESS!")
                print("="*60)
                print(f"\nYour LinkedIn Author ID is:")
                print(f"\n  {author_urn}")
                print(f"\nAdd this to your scripts/.env file:")
                print(f"\n  LINKEDIN_AUTHOR_ID={author_urn}")
                print("\n" + "="*60)

                name = data.get('name', 'N/A')
                email = data.get('email', 'N/A')
                print(f"\nProfile verification:")
                print(f"  Name: {name}")
                print(f"  Email: {email}")
                print("="*60 + "\n")
                return author_urn
    except:
        pass

    # Method 2: Try v2/me endpoint
    print("Method 1 failed. Trying v2/me endpoint...")
    url = "https://api.linkedin.com/v2/me"

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            person_id = data.get('id')

            if person_id:
                author_urn = f"urn:li:person:{person_id}"
                print("\n" + "="*60)
                print("SUCCESS!")
                print("="*60)
                print(f"\nYour LinkedIn Author ID is:")
                print(f"\n  {author_urn}")
                print(f"\nAdd this to your scripts/.env file:")
                print(f"\n  LINKEDIN_AUTHOR_ID={author_urn}")
                print("\n" + "="*60 + "\n")
                return author_urn
    except:
        pass

    # If both methods failed
    print("\n" + "="*60)
    print("UNABLE TO FETCH AUTHOR ID AUTOMATICALLY")
    print("="*60)
    print("\nThe w_member_social scope alone is not sufficient to fetch")
    print("your profile information via the API.")
    print("\n" + "="*60)
    print("MANUAL SOLUTION:")
    print("="*60)
    print("\n1. Make a test post using the API to find your author ID")
    print("2. We'll extract it from the response")
    print("\nWould you like to run the test post? (This will post publicly)")
    print("We can make a simple test post and then delete it.")
    print("\nAlternatively, you can:")
    print("  - Add 'r_liteprofile' scope to your OAuth token")
    print("  - Or manually find your person ID from LinkedIn's API")
    print("="*60 + "\n")

    return None


def main():
    if len(sys.argv) != 2:
        print("Usage: python get_author_id.py YOUR_ACCESS_TOKEN")
        print("\nExample:")
        print("  python get_author_id.py AQVBl9p...")
        print("\nTo get an access token:")
        print("  1. Go to LinkedIn Developer Portal")
        print("  2. Select your app")
        print("  3. Use the OAuth 2.0 tools to generate a token with 'w_member_social' scope")
        sys.exit(1)

    access_token = sys.argv[1]

    if not access_token or len(access_token) < 10:
        print("Error: Access token appears to be invalid (too short)")
        sys.exit(1)

    get_author_id(access_token)


if __name__ == '__main__':
    main()
