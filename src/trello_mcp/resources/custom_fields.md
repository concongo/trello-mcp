# Trello Custom Fields

## Overview

Custom Fields allow managing custom data on cards. The Custom Fields Power-Up must be enabled on a board. Field definitions exist at the board level; values are set on individual cards.

## Supported Field Types

| Type | Valid Values | Description |
|------|-------------|-------------|
| checkbox | boolean | Toggle checkbox |
| date | ISO datetime string | Date input |
| list | object with options | Dropdown selection |
| number | number | Numeric input |
| text | string | Free-form text |

**Important:** All values are stored as strings, even for numeric and date types.

## Getting Custom Fields

```
GET https://api.trello.com/1/boards/{boardId}/customFields
```

Returns an empty array if the Power-Up is disabled.

## Creating Custom Fields

```
POST https://api.trello.com/1/customFields
Body: { "idModel": "{boardId}", "modelType": "board", "name": "Field Name", "type": "text" }
```

Returns 403 if the Power-Up is disabled. Maximum 50 custom field definitions per board.

## Managing List Options

Add options to list-type fields:

```
POST https://api.trello.com/1/customField/{fieldId}/options
Body: { "pos": "bottom", "value": { "text": "Option Name" } }
```

## Getting Card Values

```
GET https://api.trello.com/1/cards/{cardId}?customFieldItems=true
```

## Setting Card Values

```
PUT https://api.trello.com/1/card/{cardId}/customField/{fieldId}/item
Body: { "value": { "text": "my value" } }
```

For list-type fields, use `idValue`:
```
PUT https://api.trello.com/1/card/{cardId}/customField/{fieldId}/item
Body: { "idValue": "{optionId}" }
```

## Clearing Values

```
PUT https://api.trello.com/1/card/{cardId}/customField/{fieldId}/item
Body: { "idValue": "", "value": "" }
```

## Deleting Custom Fields

```
DELETE https://api.trello.com/1/customFields/{fieldId}
```

**Warning:** Deletion removes all associated card values permanently.

## Webhook Actions

- `addCustomField` — Field created on board
- `deleteCustomField` — Field removed from board
- `updateCustomField` — Field modified
- `updateCustomFieldItem` — Card value changed
