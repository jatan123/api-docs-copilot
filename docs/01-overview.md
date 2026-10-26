# Staylane Partner API — Overview

> Staylane is a **fictional** hotel-partnership platform created for this demo. Any resemblance to a real company or API is coincidental.

The Staylane Partner API lets travel partners (booking engines, card issuers, travel agencies) read hotel reference data and the perks Staylane negotiates with hotels: properties, suppliers, contracted benefits, and promotional offers.

## Who uses this API
- **Booking partners** display Staylane properties and benefits inside their own booking flows.
- **Content teams** sync property and offer data into marketing pages.
- **Internal tools** validate that contracted benefits are complete before they go live.

## Core resources
| Resource | What it represents |
|---|---|
| Property | A single hotel (e.g. one building in one city). Identified by `propertyId`. |
| Supplier | The company that owns or manages one or more properties (e.g. a hotel chain). Identified by `supplierId`. |
| Benefit | A perk a guest receives at a property, such as a room upgrade, daily breakfast or a property credit. |
| Offer | A time-limited promotion at a property, such as "third night free". |

## Base URLs
- Sandbox: `https://sandbox.api.staylane.example/v2`
- Production: `https://api.staylane.example/v2`

All responses are JSON and all timestamps are ISO 8601 in UTC.

## Getting access
Partners request credentials through the Staylane Partner Portal. New partners start with **sandbox access only**. Production access is granted after the partner passes the certification checklist (see *Environments*).
