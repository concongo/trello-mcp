# Trello API Introduction

## Overview

The Trello API provides powerful capabilities for building applications. It uses delegated authentication, so applications never handle usernames or passwords directly.

## API Key Management

To begin development, you need an API key:

1. Create a Trello Power-Up first
2. Visit https://trello.com/power-ups/admin
3. Access your Power-Up and navigate to the **API Key** tab
4. Select **Generate a new API Key**

**Important:** API keys are publicly accessible by design. However, API tokens grant user data access and must be kept confidential.

## Making Requests

### Getting User Boards

```
GET https://api.trello.com/1/members/me/boards?key={yourKey}&token={yourToken}
```

Returns a JSON array of boards accessible to the authenticated user. The `me` parameter references the token owner's account.

### Retrieving Specific Board Details

```
GET https://api.trello.com/1/boards/{idBoard}?key={yourKey}&token={yourToken}
```

## Core Resources

- **Boards** – Collections where work occurs; support multiple members, lists, and customization.
- **Lists** – Card containers organized on boards.
- **Cards** – Basic Trello units containing names, descriptions, labels, and members.
- **Actions** – Complete audit logs of all board and card modifications, including comments.
- **Webhooks** – HTTP notifications triggered when monitored resources change.

## Key API Methods

| Resource | Method | Endpoint |
|----------|--------|----------|
| Lists | GET | `/1/lists/{idList}/cards` |
| Cards | POST | `/1/cards` |
| Cards | PUT | `/1/cards/{id}` |
| Comments | POST | `/1/cards/{id}/actions/comments` |
| Members | POST | `/1/cards/{id}/idMembers` |
| Webhooks | POST | `/1/webhooks` |

## Pagination

Results are capped at 1,000 items. For larger datasets, use `before` and `since` parameters with ISO 8601 dates or card/action IDs.
