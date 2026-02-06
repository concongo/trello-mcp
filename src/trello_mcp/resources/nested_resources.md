# Trello Nested Resources

## Overview

The Trello API allows accessing data through nested resources, leveraging the hierarchical structure (cards within lists within boards). Resources can be accessed via URL parameters or query parameters.

```
GET https://api.trello.com/1/boards/{boardId}/cards
GET https://api.trello.com/1/boards/{boardId}/?cards=all
```

## Cards Nested Resource

Format: `/boards/{id}/cards` or `?cards=all`

| Parameter | Options |
|-----------|---------|
| cards | all, closed, complete, incomplete, none, open, visible |
| card_fields | all or comma-separated field list |
| card_members | true, false |
| card_attachments | true, false, cover |
| card_stickers | true, false |
| card_customFieldItems | true, false |

Card fields: badges, checkItemStates, closed, dateLastActivity, desc, descData, due, idAttachmentCover, idBoard, idChecklists, idLabels, idList, idMembers, idMembersVoted, idShort, labels, limits, manualCoverAttachment, name, pos, shortLink, shortUrl, subscribed, url

## Lists Nested Resource

Format: `/boards/{id}/lists` or `?lists=open`

| Parameter | Options |
|-----------|---------|
| lists | all, closed, none, open |
| list_fields | all or comma-separated field list |

## Members Nested Resource

Format: `/boards/{id}/members` or `?members=all`

| Parameter | Options |
|-----------|---------|
| members | none, normal, admins, owners, all |
| member_fields | all or comma-separated field list (default: avatarHash, fullName, initials, username) |

## Labels Nested Resource

| Parameter | Default | Options |
|-----------|---------|---------|
| labels | none | all, none |
| label_fields | all | color, idBoard, name, uses |
| labels_limit | 50 | 0-1000 |

## Checklists Nested Resource

Format: `/cards/{id}/checklists` or `?checklists=all`

| Parameter | Options |
|-----------|---------|
| checklists | none, all |
| checkItems | all, none |
| checkItem_fields | name, nameData, pos, due, dueReminder, idMember, state, type |

## Actions Nested Resource

Format: `/object/{id}/actions`

| Parameter | Default | Options |
|-----------|---------|---------|
| actions | - | all or specific action types |
| actions_limit | 50 | 0-1000 (max 300 returned) |
| actions_since | none | ISO date or Mongo ID |
| actions_before | none | ISO date or Mongo ID |
| action_fields | all | comma-separated field list |
| action_member | true | true, false |

## Custom Fields Nested Resource

| Parameter | Options |
|-----------|---------|
| customFields | true, false (default: false) |

## Key Concepts

- Resources can be accessed through URL paths or query parameters
- Most resources allow specifying which fields to return via comma-separated lists
- Many resources support limiting results (0-1000), filtering by date ranges, and pagination
- When requesting actions, Trello caps returns at 300 items regardless of specified limits
