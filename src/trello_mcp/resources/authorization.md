# Trello API Authorization

## Overview

Trello uses token-based authentication to grant third-party applications access. Users grant permission once, receiving tokens for subsequent requests.

## Getting an API Key

1. Visit https://trello.com/power-ups/admin
2. Access your Power-Up
3. Navigate to the **API Key** tab
4. Select **Generate a new API Key**

## Authorization Flow

Direct users to:

```
https://trello.com/1/authorize?expiration=1day&scope=read&response_type=token&key={YourAPIKey}
```

### Parameters

| Parameter | Values | Purpose |
|-----------|--------|---------|
| callback_method | postMessage, fragment | How the token returns to your application |
| return_url | valid URL | Where the token is delivered |
| scope | read, write, account | Permission level requested |
| expiration | 1hour, 1day, 30days, never | Token lifetime |
| key | API key | Identifies your application |
| response_type | token | Returns token in browser window |

### Scope Definitions

- **read** — Access boards and organizations
- **write** — Modify boards and organizations
- **account** — Access member emails, update member info, mark notifications read

## Passing Credentials

### Query Parameters

```
GET https://api.trello.com/1/members/me?key={apiKey}&token={apiToken}
```

### Authorization Header

```
Authorization: OAuth oauth_consumer_key="{apiKey}", oauth_token="{apiToken}"
```

### Request Body (PUT/POST)

```json
{ "key": "{apiKey}", "token": "{apiToken}", "value": "Updated Name" }
```

## Token Security

- API keys may be public, but tokens must remain confidential
- Revoke compromised tokens immediately
- Users can manage tokens at https://trello.com/u/{username}/account under **Applications**

## Revoking Tokens

Tokens can be revoked via the UI or programmatically:

```
DELETE https://api.trello.com/1/tokens/{token}
```

After revocation, API responses return 401 with `invalid token`.

## OAuth 1.0

For standard OAuth workflows:

```
https://trello.com/1/OAuthGetRequestToken
https://trello.com/1/OAuthAuthorizeToken
https://trello.com/1/OAuthGetAccessToken
```

## Allowed Origins

Configure redirect domains at https://trello.com/power-ups/admin. Supports wildcards (e.g., `https://*.myapp.com`) and localhost for development.
