# Benefits

Requires scope `benefits:read`.

Benefits are the perks a guest receives when they book a property through a Staylane partner — for example a room upgrade on arrival, daily breakfast for two, or a property credit.

## Get benefits for a property
```
GET /properties/{propertyId}/benefits
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `checkIn` | date | no | Return benefits valid for a stay starting on this date (YYYY-MM-DD) |
| `checkOut` | date | no | Required if `checkIn` is sent |
| `program` | string | no | `luxury-collection` or `boutique-collection` |

A `propertyId` is always required. If you only know the hotel's name or city, call `GET /properties/search` first to find its `propertyId`.

Example response:
```json
{
  "propertyId": "PRP-88213",
  "benefits": [
    { "type": "room_upgrade", "description": "Room upgrade on arrival, when available" },
    { "type": "breakfast", "description": "Daily breakfast for two" },
    { "type": "property_credit", "amount": 100, "currency": "USD", "description": "USD 100 credit for dining or spa" },
    { "type": "late_checkout", "description": "4pm late checkout, when available" }
  ],
  "validatedAt": "2026-03-02T17:10:00Z"
}
```

## Benefit types
`room_upgrade`, `breakfast`, `property_credit`, `early_checkin`, `late_checkout`, `wifi`.

## Validation
Every benefit set is **validated** before it is published: amounts must be positive, the currency must match the property's country currency, and descriptions must be under 200 characters. Only validated benefits are returned. The `validatedAt` field shows when the current set passed validation.

## Program rules
- `luxury-collection` properties must offer at least `breakfast`, `property_credit` and `room_upgrade`.
- `boutique-collection` properties must offer at least `property_credit` and `late_checkout`.

## Submitting updates (internal partners only)
```
POST /properties/{propertyId}/benefits
```
Requires scope `benefits:write`. Submitted updates are validated asynchronously and appear in `GET` responses within **15 minutes** if they pass. Failed submissions trigger a `benefits.validation_failed` webhook.
