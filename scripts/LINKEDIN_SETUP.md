# LinkedIn API Setup Guide

This document covers the setup process for LinkedIn API integration, including common issues encountered.

## Prerequisites

1. LinkedIn Developer account
2. A LinkedIn app with posting permissions

## Creating a LinkedIn App

1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps)
2. Click **"Create app"**
3. Fill in the required information:
   - App name
   - LinkedIn Page (you can use your personal profile page)
   - App logo (optional)
4. Click **"Create app"**

## Required Products & Scopes

### Step 1: Add Required Products

In your app settings, go to the **Products** tab and add:

1. **"Share on LinkedIn"** - For posting content
2. **"Sign In with LinkedIn using OpenID Connect"** - For retrieving your member ID

### Step 2: Configure OAuth Scopes

After adding the products, verify you have these scopes in the **Auth** tab:

- ✅ `openid` - Required for OpenID Connect
- ✅ `profile` - Required to get your numeric member ID
- ✅ `w_member_social` - Required for posting content

## Getting Your Credentials

### 1. Get OAuth Access Token

1. In your app, go to the **Auth** tab
2. Scroll to **OAuth 2.0 tools**
3. Click **"Create token"** or **"Generate token"**
4. **IMPORTANT**: Make sure all three scopes are checked:
   - `openid`
   - `profile`
   - `w_member_social`
5. Copy the access token

**Note**: Access tokens expire after 60 days. You'll need to regenerate periodically.

### 2. Get Your Member ID

Run the helper script with your new access token:

```bash
cd scripts
source venv/bin/activate
python get_author_id.py YOUR_ACCESS_TOKEN
```

Or use curl:

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     https://api.linkedin.com/v2/userinfo
```

The response will include your `sub` field, which is your numeric member ID:

```json
{
  "sub": "123456789",
  "name": "Your Name",
  "email": "your@email.com"
}
```

Your author ID will be: `urn:li:member:123456789`

## Common Issues

### Issue 1: 403 Error on `/v2/userinfo`

**Error**: `"Not enough permissions to access: userinfo.GET.NO_VERSION"`

**Cause**: Your access token doesn't have the `openid` and `profile` scopes.

**Solution**:
1. Add the "Sign In with LinkedIn using OpenID Connect" product to your app
2. Generate a **NEW** access token with `openid`, `profile`, and `w_member_social` scopes
3. The old token won't automatically get new scopes - you must regenerate

### Issue 2: 422 Error on Posting

**Error**: `"urn:li:person:XXX" does not match urn:li:member:\\d+`

**Cause**: Wrong URN format. LinkedIn's posting API requires:
- ✅ `urn:li:member:123456` (numeric ID)
- ❌ `urn:li:person:ACoAAAERPDo...` (alphanumeric profile ID)

**Solution**: Use the `get_author_id.py` script with a token that has `profile` scope to get the correct numeric ID.

### Issue 3: Alphanumeric vs Numeric IDs

LinkedIn has multiple ID formats:
- **Profile URN**: `urn:li:fsd_profile:ACoAAAERPDo...` (from web interface)
- **Person URN**: `urn:li:person:ACoAAAERPDo...` (from Voyager API)
- **Member URN**: `urn:li:member:123456` (from REST API - **this is what you need**)

Only the numeric member URN works with the posting API.

### Issue 4: Scope Authorization Delays

**Symptom**: Just added OpenID Connect product but still getting 403 errors

**Solution**: Wait a few minutes for LinkedIn to process the authorization on their backend. If it persists beyond 10 minutes, try:
1. Regenerating your access token
2. Logging out and back into LinkedIn Developer Portal
3. Checking that the products show as "Active" in your app settings

## Setting Up GitHub Actions

Once you have your credentials:

1. Go to your GitHub repository
2. Navigate to: **Settings → Secrets and variables → Actions**
3. Click **"New repository secret"**
4. Add two secrets:
   - Name: `LINKEDIN_ACCESS_TOKEN`, Value: Your OAuth token
   - Name: `LINKEDIN_AUTHOR_ID`, Value: `urn:li:member:YOUR_NUMERIC_ID`

The GitHub Action will use these secrets to post to LinkedIn automatically when you push to main.

## Testing Your Setup

Test that everything works:

```bash
cd scripts
source venv/bin/activate

# Test getting your author ID
python get_author_id.py YOUR_ACCESS_TOKEN

# Test posting (this will create a real post!)
python linkedin_post.py ../_posts/your-post.md
```

## Access Token Expiration

LinkedIn access tokens expire after **60 days**. When your token expires:

1. Go to LinkedIn Developer Portal
2. Navigate to your app → Auth tab
3. Generate a new token with the same scopes
4. Update your `.env` file (local) and GitHub Secrets (for Actions)

## Security Notes

- Never commit your `.env` file (already in `.gitignore`)
- Never share your access token publicly
- Rotate tokens if accidentally exposed
- Use GitHub Secrets for CI/CD - never hardcode credentials
