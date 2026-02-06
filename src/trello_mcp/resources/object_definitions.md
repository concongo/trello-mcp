# Trello Object Definitions

## Board Object

| Field | Type | Description |
|-------|------|-------------|
| id | string | Board identifier |
| name | string | Board title |
| desc | string | Description |
| closed | boolean | Archive status |
| idMemberCreator | string | Creator's member ID |
| idOrganization | string | Associated workspace |
| url | string | Board link |
| shortUrl | string | Short permalink |
| prefs | object | Board settings and preferences |
| labelNames | object | Custom label names by color |
| starred | boolean | User's star status |
| limits | object | Resource usage information |
| memberships | array | User relationships and roles |

```
GET https://api.trello.com/1/boards/{boardId}?fields=all
```

## Card Object

| Field | Type | Description |
|-------|------|-------------|
| id | string | Card identifier |
| name | string | Card title |
| desc | string | Description (up to 16,384 characters) |
| closed | boolean | Archive status |
| idBoard | string | Parent board ID |
| idList | string | Parent list ID |
| idMembers | array | Assigned member IDs |
| idLabels | array | Label IDs applied |
| idChecklists | array | Checklist IDs on card |
| due | date | Due date if set |
| dueComplete | boolean | Completion status |
| pos | float | Position in list |
| labels | array | Label objects |
| badges | object | Display indicators (votes, comments, attachments, etc.) |
| dateLastActivity | date | Last modification timestamp |
| shortLink | string | 8-character shortened ID |
| url | string | Full card link |
| idAttachmentCover | string | Cover image attachment ID |
| address | string | Location address |
| locationName | string | Location name |
| coordinates | object | Latitude/longitude values |

```
GET https://api.trello.com/1/cards/{cardId}?fields=all
```

## List Object

Lists are containers for cards within a board.

| Field | Type | Description |
|-------|------|-------------|
| id | string | List identifier |
| name | string | List title |
| closed | boolean | Archive status |
| idBoard | string | Parent board ID |
| pos | float | Position on board |

## Member Object

| Field | Type | Description |
|-------|------|-------------|
| id | string | Member identifier |
| avatarUrl | string | Profile image URL |
| initials | string | User initials |
| fullName | string | Display name |
| username | string | Unique username |
| confirmed | boolean | Email verification status |
| idOrganizations | array | Associated workspaces |
| idBoards | array | Member's boards |

## Action Object

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique action identifier |
| data | object | Contextual information about the action |
| date | date | When the action occurred |
| idMemberCreator | string | ID of the member who triggered the action |
| type | string | Action category |

## Attachment Object

| Field | Type | Description |
|-------|------|-------------|
| id | string | Attachment identifier |
| bytes | integer | File size in bytes |
| date | string | When added |
| idMember | string | Member who added it |
| isUpload | boolean | Whether uploaded vs. linked |
| mimeType | string | File type |
| name | string | Filename |
| pos | float | Position in attachment list |
| previews | array | Generated image thumbnails |
| url | string | Attachment link |
