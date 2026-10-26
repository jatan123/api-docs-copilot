# Environments and certification

Staylane runs two fully separate environments.

| | Sandbox | Production |
|---|---|---|
| Base URL | `https://sandbox.api.staylane.example/v2` | `https://api.staylane.example/v2` |
| Data | Real property and supplier IDs, synthetic benefits and offers | Live data |
| Credentials | Sandbox client ID/secret | Separate production client ID/secret |
| Rate limits | 60/min | 600/min |

Credentials are **not interchangeable**: a sandbox token sent to production returns `401 invalid_token`.

## Certification checklist (required for production access)
1. Handle token expiry by requesting a new token on `401`.
2. Respect `Retry-After` on `429` and `503`.
3. Page through search results correctly.
4. Ignore unknown response fields.
5. Display benefit descriptions exactly as returned (no rewording).
6. Pass a test run of 50 sandbox calls without errors other than intentional ones.

Submit the checklist in the Partner Portal. Review takes **3–5 business days**. Once approved, production credentials appear in the portal.
