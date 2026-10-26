# Pagination and versioning

## Pagination
List endpoints (`/properties/search`, `/suppliers/{supplierId}/properties`) are paginated.

- `page` starts at 1.
- `pageSize` defaults to 25; the maximum is 100. Larger values return `400 invalid_parameter`.
- Responses include `page`, `pageSize`, `totalResults` and `totalPages`.

To fetch everything, keep requesting the next page until `page` equals `totalPages`.

## Versioning
The version is part of the URL (`/v2`). Within a major version, Staylane only makes **additive** changes — new endpoints, new optional parameters, new response fields. Your integration must ignore response fields it does not recognise.

Breaking changes ship as a new major version. When a new major version is released, the previous one is supported for **12 months**, and responses from the old version include a `Sunset` header with the retirement date.

## Changelog (recent)
- **v2.4** — Added `program` filter to benefits.
- **v2.3** — Added `late_checkout` and `early_checkin` benefit types.
- **v2.2** — Added `bookingWindow` to offers.
- **v1** — Retired. All v1 calls now return `410 Gone`.
