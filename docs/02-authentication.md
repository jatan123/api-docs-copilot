# Authentication

The Staylane Partner API uses the **OAuth 2.0 client credentials** flow. Every request must carry a valid bearer access token.

## Getting a token
Send your client ID and client secret to the token endpoint:

```
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&scope=properties:read benefits:read
```

Response:
```json
{ "access_token": "eyJ...", "token_type": "Bearer", "expires_in": 3600, "scope": "properties:read benefits:read" }
```

## Using the token
Add it to every request:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Token lifetime
Access tokens expire after **3600 seconds (1 hour)**. There are no refresh tokens in the client credentials flow — request a new token when the old one expires. Cache tokens and reuse them; do not request a new token per API call. Requesting more than **20 tokens per minute** from one client ID returns `429`.

## Scopes
| Scope | Grants |
|---|---|
| `properties:read` | Property search and property details |
| `suppliers:read` | Supplier endpoints |
| `benefits:read` | Benefit endpoints |
| `offers:read` | Offer endpoints |
| `benefits:write` | Submitting benefit updates (internal partners only) |

Calling an endpoint without the required scope returns `403 insufficient_scope`.

## Rotating credentials
Client secrets can be rotated in the Partner Portal. The old secret stays valid for **24 hours** after rotation so you can deploy the new one without downtime.
