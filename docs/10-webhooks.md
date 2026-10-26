# Webhooks

Webhooks notify you when data changes, so you don't have to poll.

## Events
| Event | Sent when |
|---|---|
| `property.updated` | A property's details change |
| `property.status_changed` | A property moves between `active`, `paused` and `retired` |
| `benefits.published` | A new validated benefit set goes live |
| `benefits.validation_failed` | A submitted benefit update failed validation (internal partners only) |
| `offer.created` | A new offer is added |
| `offer.expired` | An offer passes its end date |

## Registering an endpoint
Register an HTTPS URL in the Partner Portal and choose which events to receive. HTTP URLs are rejected.

## Verifying signatures
Each webhook includes a `Staylane-Signature` header: an HMAC-SHA256 of the raw request body using your webhook signing secret. Compute the same HMAC and compare before trusting the payload. Reject requests older than 5 minutes using the `Staylane-Timestamp` header to prevent replay attacks.

## Delivery and retries
Respond with any `2xx` status within **10 seconds**. Otherwise Staylane retries up to **8 times over 24 hours** with exponential backoff. After that the event is dropped and appears as failed in the portal, where it can be resent manually.

Events can arrive out of order or more than once. Use the `eventId` field to deduplicate.
