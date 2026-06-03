# Pigeon-AI

Database schema for a pigeon management application covering user accounts, pigeon profiles, pedigree, breeding, health, racing, AI analysis, file storage, notifications, and weather cache data.

## Schema

The PostgreSQL schema is defined in [`db/schema.sql`](db/schema.sql). It includes:

- UUID primary keys with `gen_random_uuid()` defaults.
- Foreign keys between owners, pigeons, pedigree, breeding, health, racing, AI analysis, files, and notifications.
- Basic data integrity checks for non-negative counts, rankings, speeds, prize money, and humidity.
- Indexes for common relationship lookups and unread notifications.
- An `updated_at` trigger for the `users` table.

## Usage

Apply the schema to a PostgreSQL database:

```bash
psql "$DATABASE_URL" -f db/schema.sql
```
