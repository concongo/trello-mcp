# Trello API Limits

## Overview

Trello enforces object limits on boards and cards to maintain system stability. These include cards, checklists, stickers, labels, lists, and attachments.

## Retrieving Board Limits

```
GET https://api.trello.com/1/boards/{boardId}/?fields=limits
```

### Response Structure

```json
{
  "id": "552595baa7b650edb7a0f8ff",
  "limits": {
    "cards": {
      "openPerBoard": {
        "status": "ok",
        "disableAt": 5000,
        "warnAt": 4500
      },
      "totalPerBoard": {
        "status": "ok",
        "disableAt": 2000000,
        "warnAt": 1800000
      }
    }
  }
}
```

## Limit Parameters

| Parameter | Description |
|-----------|-------------|
| disableAt | Threshold where object creation becomes disabled |
| warnAt | Threshold triggering user warnings in clients |
| status | "ok" (compliant), "warn" (approaching limit), or "disabled" (exceeded) |
| count | Current count (appears when status changes from "ok") |

## Retrieving Card Limits

```
GET https://api.trello.com/1/boards/{boardId}/cards/?fields=limits&limit=1
```

Card limits apply to attachments, checklists, and stickers per individual card.

## Important Notes

- Limits vary by board and account
- Integrations should actively enforce the `disableAt` threshold
- Creating webhooks on objects exceeding limits returns an error
- Existing webhooks on items with `maxExceeded` status get automatically deleted
