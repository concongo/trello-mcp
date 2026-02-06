# Trello API Rate Limits

## Request Limits

| Scope | Limit |
|-------|-------|
| Per API Key | 300 requests per 10 seconds |
| Per Token | 100 requests per 10 seconds |
| /1/members/ endpoint | 100 requests per 900 seconds |

Exceeding these thresholds returns a **429** HTTP status code.

## Error Responses

**Token limit exceeded:**
```json
{
  "error": "API_TOKEN_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded"
}
```

**Key limit exceeded:**
```json
{
  "error": "API_KEY_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded"
}
```

**Database query limit:**
`API_TOKEN_DB_LIMIT_EXCEEDED` — token is executing too many resource-intensive operations.

**Response size limit:**
`API_TOO_MANY_CARDS_REQUESTED` — retrieve cards first, then request actions separately.

## Rate Limit Headers

Responses include these headers for monitoring:

- `x-rate-limit-api-token-interval-ms`
- `x-rate-limit-api-token-max`
- `x-rate-limit-api-token-remaining`
- `x-rate-limit-api-key-interval-ms`
- `x-rate-limit-api-key-max`
- `x-rate-limit-api-key-remaining`

## Best Practices

- **Use Webhooks** instead of polling for real-time updates
- **Leverage Nested Resources** to reduce the number of API calls
- **Avoid /1/members and /1/search** endpoints when possible; use nested alternatives like `/1/boards/{id}/members`
- **Monitor rate limit headers** to avoid hitting limits
