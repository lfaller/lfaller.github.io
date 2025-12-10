# LinkedIn API Investigation - Comment Automation

**Date:** December 10, 2025

## Summary

The automated LinkedIn comment feature is currently **not working** due to LinkedIn API permission limitations. The "Share on LinkedIn" product does not include access to the comments API endpoint, and requesting the "Community Management API" product is blocked.

## Current Status

### ✅ What Works
- **Automatic post publishing** to LinkedIn with images and summary text
- Blog posts are published immediately when pushed to main
- Images upload successfully
- Post content formatting (hashtags, summary) works correctly

### ❌ What Doesn't Work
- **Automated comments** on LinkedIn posts with blog links
- All comment API endpoints return `404 RESOURCE_NOT_FOUND`
- Even with retry logic (12 attempts, 5-second delays), comments fail

## Root Cause Analysis

### Token Permission Issue
The current `LINKEDIN_ACCESS_TOKEN` has severely limited permissions:

**Test Results:**
```
GET /me                     → 403 FORBIDDEN (insufficient permissions)
GET /ugcPosts              → 404 NOT FOUND
POST /comments?action=create → 404 NOT FOUND
POST /reactions?action=create → 404 NOT FOUND
```

### Verified Scopes
The token has these scopes configured (but not actually granted to the current token):
- ✓ `openid`
- ✓ `profile`
- ✓ `w_member_social`
- ✓ `email`

However, the **actual token was generated before these scopes were added**, so it doesn't have them.

### LinkedIn API Product Limitations

**Current Products:**
- ✓ Share on LinkedIn (Default Tier) - allows posting

**What We Need:**
- Community Management API (Development Tier) - allows comments

**The Problem:**
```
"This product cannot be requested because there are currently other
provisioned products or other pending product requests. A new developer
application can be created to request this product."
```

LinkedIn only allows one product per app at a time, and prevents adding Community Management API while "Share on LinkedIn" is active.

## Solutions Attempted

1. **Increase retry delays** - Extended from 2s to 5s delays, up to 12 attempts (55 seconds total)
   - Result: Still returns 404

2. **Fix URN format** - Tried both `urn:li:ugcPost:{id}` and `urn:li:share:{id}` formats
   - Result: Still returns 404

3. **Regenerate token with correct scopes** - Not yet done
   - Reason: Original token doesn't have scopes despite them being configured

4. **Create new app for comments** - Would require separate developer application
   - Trade-off: Adds complexity, requires managing two apps/tokens

## Current Workaround

**Manual Comment Posting:**
- Posts publish automatically to LinkedIn
- Blog link is printed in workflow output: `Post URL for manual comment: {blog_url}`
- Comments are added manually after posts go live
- This takes ~2 minutes per post

**Example Output:**
```
✓ Post published successfully!
✓ Posted with 1 image(s)

Adding comment with blog link...
  Post URL for manual comment: https://linafaller.com/category/year/month/day/slug/
⚠ Comment automation failed. Post is live, but you may need to add the comment manually.
  ✗ Error 404: No virtual resource found
```

## Future Options

### Option 1: Create New Developer App (Recommended)
**Steps:**
1. Create a new LinkedIn Developer app
2. Request "Community Management API" access
3. Generate new access token with full scopes
4. Update `LINKEDIN_ACCESS_TOKEN` in GitHub secrets
5. Remove old app when confirmed working

**Pros:**
- Cleaner separation of concerns
- Full access to all social features
- No need to remove existing product

**Cons:**
- Requires managing two applications
- Takes time for LinkedIn approval (usually 24-48 hours)

### Option 2: Regenerate Current Token
**Steps:**
1. Go to LinkedIn Developer app
2. Regenerate access token (with current scopes)
3. Update `LINKEDIN_ACCESS_TOKEN` in GitHub secrets

**Pros:**
- Quick, minimal changes

**Cons:**
- Still limited by "Share on LinkedIn" product
- May not actually grant w_member_social scope

### Option 3: Accept Manual Comments (Current)
**What we're doing now:**
- Posts publish automatically
- Comments added manually
- Workflow prints blog URL for easy reference

**Pros:**
- Works immediately, no waiting for approvals
- No additional app management
- You have full control over comment timing

**Cons:**
- Requires manual step after post publish
- Takes 1-2 minutes per post

## Technical Details

### Files Involved
- `scripts/linkedin_post.py` - Main posting script with comment attempt
- `scripts/check_linkedin_token.py` - Diagnostic script to test token permissions
- `scripts/test_linkedin_endpoints.py` - Diagnostic script to test API endpoints
- `.github/workflows/linkedin-crosspost.yml` - GitHub Actions workflow

### Comment Function Signature
```python
def create_comment_on_post(post_urn, author_id, access_token, comment_text,
                          retries=12, delay=5):
    """
    LinkedIn posts may need 30-40 seconds to be indexed before accepting comments.
    Retries up to 12 times with 5 second delays between attempts (55 seconds total).
    """
```

**Current behavior:**
- Attempts 12 times over ~55 seconds
- Waits 5 seconds between attempts
- Logs each attempt and response
- Prints blog URL for manual fallback
- Does NOT fail the entire workflow on comment failure

### API Endpoints
- **Post creation:** `POST /ugcPosts` ✅ Working
- **Image registration:** `POST /assets?action=registerUpload` ✅ Working
- **Image upload:** Binary POST to provided URL ✅ Working
- **Comments:** `POST /comments?action=create` ❌ Returns 404
- **Reactions:** `POST /reactions?action=create` ❌ Returns 404
- **Profile info:** `GET /me` ❌ Returns 403

## Recommended Next Steps

1. **Short term (now):** Keep manual comment posting workflow
   - Posts go out automatically
   - Comments added manually
   - Track which posts have comments manually added

2. **Medium term (this week):** Regenerate token and verify it has w_member_social scope
   - Check if it fixes comment endpoint access
   - If not, proceed to Option 1

3. **Long term (if needed):** Create new developer app for full API access
   - Provides more flexibility for future features
   - Better separation of posting vs. community management

## References

- LinkedIn API Documentation: https://docs.microsoft.com/en-us/linkedin/
- Developer Console: https://www.linkedin.com/developers/apps
- API Explorer: https://www.linkedin.com/developers/tools/api-explorer

## Questions for Future Review

- [ ] Have you regenerated the access token after adding scopes?
- [ ] Would you like to pursue the new developer app approach?
- [ ] Should we add a status flag to the GitHub workflow to indicate comment status?
- [ ] Should comments be completely removed from automation (separate manual process)?
