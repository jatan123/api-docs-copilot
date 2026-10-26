# Suppliers

Requires scope `suppliers:read`.

A supplier is the company that owns or manages properties — usually a hotel chain or a management company. One supplier can have many properties; each property has exactly one supplier.

## Get a supplier
```
GET /suppliers/{supplierId}
```
Returns supplier name, headquarters country, contact email for partnership questions, status, and `propertyCount`.

Example:
```
GET /suppliers/SUP-2041
```
```json
{ "supplierId": "SUP-2041", "name": "Saguaro Hotel Group", "country": "US", "status": "active", "propertyCount": 37 }
```

## List a supplier's properties
```
GET /suppliers/{supplierId}/properties
```
Supports `page` and `pageSize` like property search.

## ID formats
- Supplier IDs start with `SUP-` followed by digits.
- Property IDs start with `PRP-` followed by digits.
IDs are identical in sandbox and production for the same real-world entity, so you can test with production IDs in sandbox.
