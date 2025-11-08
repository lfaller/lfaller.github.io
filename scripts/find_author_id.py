#!/usr/bin/env python3
"""
Find your LinkedIn Author ID by inspecting your LinkedIn profile URL

This script helps you find your LinkedIn person URN without needing
additional API scopes beyond w_member_social.
"""

import sys

def main():
    print("="*60)
    print("LinkedIn Author ID Finder")
    print("="*60)
    print("\nSince the w_member_social scope doesn't provide access to")
    print("profile endpoints, we'll use your LinkedIn profile URL instead.")
    print("\n" + "="*60)
    print("OPTION 1: Extract from Public Profile")
    print("="*60)
    print("\n1. Go to your LinkedIn profile page")
    print("2. Look at the URL in your browser")
    print("3. It should look like: https://www.linkedin.com/in/USERNAME/")
    print("4. Note your USERNAME")
    print("\nFor example, if your URL is:")
    print("  https://www.linkedin.com/in/linafaller/")
    print("Your username is: linafaller")

    print("\n" + "="*60)
    print("OPTION 2: Use LinkedIn Inspector Tool")
    print("="*60)
    print("\n1. Go to: https://www.linkedin.com/help/linkedin/answer/a519819")
    print("2. This shows tools to inspect your LinkedIn profile")
    print("3. Look for your 'Member ID' or 'URN'")

    print("\n" + "="*60)
    print("OPTION 3: Test Post Method (Recommended)")
    print("="*60)
    print("\nThe easiest way is to make a test post and capture the author")
    print("information from the API response.")
    print("\nLet's do that now!")
    print("\n" + "="*60)

    # Get access token
    if len(sys.argv) > 1:
        access_token = sys.argv[1]
    else:
        print("\nPlease paste your LinkedIn access token:")
        access_token = input("> ").strip()

    if not access_token or len(access_token) < 10:
        print("Error: Invalid access token")
        sys.exit(1)

    print("\nI'll now make a test API call to discover your author ID...")
    print("Note: This will create a DRAFT post (not published) to safely get your ID")

    import requests

    # We'll try to make a minimal test call that reveals the author
    # The ugcPosts endpoint returns the author info we need

    url = "https://api.linkedin.com/v2/me"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    # First try: Check what info we can get with current token
    print("\nChecking your token permissions...")

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
            return

    # If that didn't work, provide manual instructions
    print("\n" + "="*60)
    print("Manual Method Required")
    print("="*60)
    print("\nPlease visit your LinkedIn profile and provide your profile URL")
    print("or username so we can construct your author URN.")
    print("\nWhat is your LinkedIn profile URL or username?")
    profile_input = input("> ").strip()

    # Extract username from URL if provided
    if 'linkedin.com' in profile_input:
        parts = profile_input.split('/in/')
        if len(parts) > 1:
            username = parts[1].strip('/').split('/')[0]
        else:
            print("Couldn't parse URL. Please provide just your username.")
            username = input("Username: ").strip()
    else:
        username = profile_input

    print(f"\nYour username: {username}")
    print("\nUnfortunately, we need the numeric person ID, not just the username.")
    print("LinkedIn doesn't provide a public API to convert username to person ID")
    print("without additional API scopes.")
    print("\n" + "="*60)
    print("RECOMMENDED SOLUTION:")
    print("="*60)
    print("\n1. Go back to LinkedIn Developer Portal")
    print("2. Regenerate your OAuth token with BOTH scopes:")
    print("   - w_member_social (for posting)")
    print("   - r_liteprofile OR r_basicprofile (for getting your ID)")
    print("3. Run this script again with the new token")
    print("\nOR")
    print("\n4. Contact me with your username and I'll help find your person ID")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
