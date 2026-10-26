# Properties

Requires scope `properties:read`.

## Search properties
```
GET /properties/search
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| `city` | string | no | City name, e.g. `Phoenix` |
| `country` | string | no | ISO 3166-1 alpha-2 code, e.g. `US` |
| `supplierId` | string | no | Only properties belonging to this supplier |
| `name` | string | no | Partial, case-insensitive name match |
| `status` | string | no | `active` (default), `paused`, or `retired` |
| `page` | integer | no | Page number, starting at 1 |
| `pageSize` | integer | no | Results per page, default 25, maximum 100 |

At least one of `city`, `country`, `supplierId` or `name` is required; otherwise the API returns `400 missing_search_criteria`.

Example:
```
GET /properties/search?city=Phoenix&supplierId=SUP-2041
```

## Get a property
```
GET /properties/{propertyId}
```
Returns name, address, coordinates, star rating, supplierId, status, and the list of programs the property belongs to.

Example response:
```json
{
  "propertyId": "PRP-88213",
  "name": "Desert Bloom Resort",
  "supplierId": "SUP-2041",
  "city": "Phoenix",
  "country": "US",
  "starRating": 5,
  "status": "active",
  "programs": ["luxury-collection"]
}
```

## Property status
- `active` — bookable and shown to guests.
- `paused` — temporarily hidden (e.g. renovation). Benefits are kept but not displayed.
- `retired` — permanently removed. Retired properties are returned by `GET /properties/{propertyId}` for 12 months, then return `404`.

## Programs
A property can belong to the `luxury-collection` program, the `boutique-collection` program, or both. Program membership affects which benefits apply (see *Benefits*).
