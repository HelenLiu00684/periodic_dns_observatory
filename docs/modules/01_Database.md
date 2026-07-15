# Database Component

**Project:** DNS Measurement Platform

**Component:** Database Layer

**Version:** 1.0

---

# 1. Purpose

The Database Component provides the persistent archive layer for the DNS Measurement Platform.

Its primary responsibility is to store, retrieve, and manage normalized network observations.

Unlike telemetry databases that optimize time-series metrics, the Database Component preserves complete canonical observations for long-term archival, historical analysis, and downstream processing.

The Database Component serves as the authoritative source of truth for the platform.

---

# 2. Responsibilities

The Database Component is responsible for:

- Managing SQLite connections
- Initializing the database schema
- Persisting normalized observations
- Retrieving archived observations
- Supporting batch processing
- Providing data for telemetry generation
- Supporting operational tools

The Database Component is **not responsible** for:

- DNS parsing
- Observation normalization
- Telemetry generation
- Time-series storage
- Visualization
- REST APIs
- Business analytics

---

# 3. Architecture

The Database Component consists of four independent modules.

```text
                sqlite_connection
                        │
                        ▼
                 sqlite_schema
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
 sqlite_writer                   sqlite_reader
```

Each module owns one clearly defined responsibility.

---

# 4. Module Overview

## sqlite_connection

Responsible for:

- Creating SQLite connections
- Configuring connection behavior
- Managing database lifecycle
- Closing database connections

This module never performs database operations.

---

## sqlite_schema

Responsible for:

- Creating database tables
- Initializing database schema
- Schema maintenance
- Schema evolution

This module contains no business logic.

---

## sqlite_writer

Responsible for persisting platform data.

Supported operations include:

- Insert Measurement
- Insert Probe
- Insert Observation

The Writer never performs analytics or telemetry generation.

---

## sqlite_reader

Responsible for retrieving archived data.

Supported operations include:

- Read Measurement
- Read Probe
- Read Observation
- Batch retrieval
- Historical queries

Reader APIs return archived observations without modification.

---

# 5. Data Flow

The Database Component receives normalized observations from the Observation Layer.

```text
Observation

        │

        ▼

sqlite_writer

        │

        ▼

SQLite Archive

        │

        ▼

sqlite_reader

        │

        ▼

Telemetry
API
CLI Tools
Analytics
```

Database modules do not interpret or modify observation contents.

They preserve canonical platform data.

---

# 6. Public Interfaces

The Database Component exposes a small number of public APIs.

Examples include:

```python
get_connection()

close_connection()

create_tables()

insert_measurement()

insert_probe()

insert_observation()

save_all()

get_measurement()

get_probe()

get_observation()

fetch_raw_observations_after()
```

Public APIs are intentionally limited to maintain a stable interface for higher platform layers.

---

# 7. Archive Philosophy

SQLite is treated as the platform archive rather than a telemetry database.

The archive stores complete canonical observations.

Telemetry metrics are generated later by the Telemetry Component.

This separation preserves historical accuracy while allowing telemetry implementations to evolve independently.

---

# 8. Testing Strategy

Every Database module is independently testable.

Testing includes:

- Unit Testing
- Integration Testing
- Archive Pipeline Testing

All tests execute against an isolated temporary database.

Production archives are never used during automated testing.

---

# 9. Operational Tools

The Database Component provides operational utilities for common administrative tasks.

Examples include:

- Database Status
- Health Check
- Backup
- Reset
- Vacuum
- Statistics
- Archive Viewer

Operational tools are considered part of the Database Component rather than auxiliary scripts.

---

# 10. Future Evolution

The Database Component is designed to evolve without affecting higher platform layers.

Future improvements may include:

- Connection pooling
- Database migration framework
- Multiple archive backends
- Read-only archive mode
- Incremental synchronization
- Archive partitioning

These improvements should preserve existing public interfaces whenever possible.

---

# 11. Design Principles

The Database Component follows several engineering principles.

## Single Responsibility

Each module owns one clearly defined responsibility.

---

## Archive First

SQLite serves as the authoritative archive.

Telemetry databases are derived from archived observations.

---

## Canonical Storage

The archive stores canonical Observation objects without introducing telemetry-specific structures.

---

## Platform Independence

The Database Component has no knowledge of telemetry, visualization, APIs, or frontend technologies.

---

## Long-Term Maintainability

Database APIs are intentionally stable.

Internal implementations may evolve while preserving public interfaces.

---

# 12. Summary

The Database Component forms the persistent foundation of the DNS Measurement Platform.

By separating connection management, schema management, persistence, and retrieval into independent modules, the platform achieves a database architecture that is maintainable, testable, extensible, and suitable for long-term engineering evolution.