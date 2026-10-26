# Errors and rate limits

## Error format
All errors return JSON:
```json
{ "error": { "code": "not_found", "message": "Property PRP-00000 was not found", "requestId": "req_7f2c..." } }
```
Include the `requestId` when contacting partner support.

## Error codes
| HTTP | code | Meaning | What to do |
|---|---|---|---|
| 400 | `invalid_parameter` / `missing_search_criteria` | A parameter is missing or malformed | Fix the request; do not retry |
| 401 | `invalid_token` | Token missing, expired or malformed | Get a new token and retry once |
| 403 | `insufficient_scope` | Token lacks the scope for this endpoint | Request the scope in the Partner Portal |
| 404 | `not_found` | The ID does not exist (or the property was retired over 12 months ago) | Check the ID |
| 409 | `conflict` | A benefit update is already being validated for this property | Wait and retry after 15 minutes |
| 429 | `rate_limited` | Too many requests | Wait for the number of seconds in the `Retry-After` header |
| 500 | `internal_error` | Staylane-side failure | Retry with exponential backoff |
| 503 | `maintenance` | Planned maintenance | Retry after the `Retry-After` time |

## Rate limits
| Environment | Per minute | Per day |
|---|---|---|
| Sandbox | 60 requests | 5,000 requests |
| Production | 600 requests | 500,000 requests |

Limits apply per client ID. Every response includes `X-RateLimit-Limit`, `X-RateLimit-Remaining` and `X-RateLimit-Reset` headers.

## Retry guidance
Retry only `429`, `500` and `503`. Use exponential backoff starting at 1 second, doubling up to 32 seconds, with a maximum of 5 retries.
