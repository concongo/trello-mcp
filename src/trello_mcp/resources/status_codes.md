# Trello API Status Codes

| Code | Name | Description |
|------|------|-------------|
| 200 | Success | Request completed successfully |
| 400 | Bad Request | Missing required fields or invalid field values |
| 401 | Unauthorized | Invalid credentials, missing credentials, or insufficient permissions |
| 403 | Forbidden | Operation not allowed (e.g., too many checklists on a card) |
| 404 | Not Found | No matching route or the requested resource doesn't exist |
| 409 | Conflict | Request doesn't match current server state |
| 429 | Too Many Requests | Rate limit exceeded — reduce request frequency |
| 449 | Sub-Request Failed | API was unable to process every part of the request |
| 500 | Internal Server Error | Unexpected server-side error |
| 503 | Service Unavailable | A dependent service is down |
| 504 | Gateway Timeout | GET request exceeded the 30-second time limit |
