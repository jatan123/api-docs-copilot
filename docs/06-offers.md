# Offers

Requires scope `offers:read`.

Offers are time-limited promotions at a property, such as "third night free" or "15% off stays of 4+ nights". Unlike benefits, offers have start and end dates.

## Get offers for a property
```
GET /properties/{propertyId}/offers
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `status` | string | no | `active` (default), `upcoming`, or `expired` |

Example:
```
GET /properties/PRP-88213/offers?status=upcoming
```

Each offer contains `offerId`, `title`, `terms`, `startDate`, `endDate`, and `bookingWindow` (the dates during which the offer can be booked, which can differ from the stay dates).

## Stacking rules
Offers **can be combined with benefits**, but only **one offer** can be applied per booking. If several offers are active, partners should show the one with the highest guest value; the API returns offers sorted by `priority`, highest first.

## Expired offers
Expired offers are returned for **90 days** after their `endDate` when you pass `status=expired`, then removed.
