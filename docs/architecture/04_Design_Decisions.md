# Design Decisions

**Project:** DNS Measurement Platform

**Version:** 1.0

---

# Purpose

This document records the major architectural decisions made during the development of the DNS Measurement Platform.

Unlike implementation documentation, this document focuses on **why** specific engineering decisions were made rather than **how** they were implemented.

As the platform evolves, new architectural decisions should be appended to this document to preserve engineering knowledge and maintain long-term consistency.

Each decision follows the same structure:

- Context
- Decision
- Rationale
- Consequences

---

# Decision 001

## Observation is the Canonical Data Model

### Context

The platform collects data from heterogeneous network measurement systems.

Each data source exposes different data structures, naming conventions, and protocol-specific fields.

### Decision

The platform defines **Observation** as the canonical data model.

All external data sources must be normalized into the Observation model before entering the archive.

### Rationale

A canonical model decouples external measurement formats from internal platform architecture.

New protocols can be integrated without redesigning downstream components.

### Consequences

All downstream components operate exclusively on Observation objects.

The Collector, SQLite Archive, Telemetry Pipeline, APIs, and Analytics Engine remain independent of protocol-specific implementations.

---

# Decision 002

## SQLite is the Archive Database

### Context

The platform requires reliable long-term storage for normalized observations.

Telemetry databases are optimized for time-series metrics rather than structured observation records.

### Decision

SQLite serves as the authoritative archive database.

### Rationale

SQLite is lightweight, portable, reliable, and well suited for normalized structured observations.

### Consequences

SQLite stores complete Observation records.

Telemetry metrics are generated from archived observations instead of directly from measurement data.

---

# Decision 003

## Observation Archive and Telemetry Storage are Independent

### Context

Operational archives and telemetry databases have different engineering goals.

### Decision

The platform separates archive storage from telemetry storage.

SQLite stores observations.

InfluxDB stores telemetry metrics.

### Rationale

Separating these responsibilities prevents storage technologies from influencing one another.

Each storage backend can evolve independently.

### Consequences

Changing or replacing the telemetry backend does not affect the archive.

---

# Decision 004

## Canonical Telemetry Metrics

### Context

The platform may support multiple telemetry backends in the future.

### Decision

Telemetry Builder produces Canonical Telemetry Metrics.

Backend writers convert canonical metrics into storage-specific formats.

### Rationale

Metric generation should remain independent of storage technology.

### Consequences

Future integrations with Prometheus, OpenTelemetry, or TimescaleDB require only new writers.

---

# Decision 005

## Database Reader Returns Raw Observations

### Context

Telemetry generation begins with archived observations.

### Decision

Database Reader returns raw Observation records.

Telemetry generation is performed by higher layers.

### Rationale

Database responsibilities remain limited to persistence and retrieval.

### Consequences

The Database Layer remains independent of telemetry logic.

---

# Decision 006

## Layer Responsibilities Never Overlap

### Context

As platforms evolve, modules tend to accumulate unrelated responsibilities.

### Decision

Every component owns one primary responsibility.

### Rationale

Single Responsibility improves readability, maintainability, testing, and long-term evolution.

### Consequences

Responsibilities remain clearly separated across the platform.

---

# Decision 007

## Platform Runtime Owns Service Lifecycle

### Context

The platform consists of multiple services including databases, collectors, telemetry pipelines, APIs, and dashboards.

### Decision

Service initialization and shutdown belong to the Platform Runtime.

Individual components should never start or stop other services.

### Rationale

Centralized runtime management simplifies deployment and operational maintenance.

### Consequences

Runtime becomes the orchestration layer for the entire platform.

---

# Decision 008

## Operational Tools are Platform Components

### Context

Administrative operations such as backup, reset, health checks, and telemetry import are essential platform capabilities.

### Decision

Operational tools are treated as first-class platform components.

### Rationale

Operational workflows should be repeatable, automated, and independently maintainable.

### Consequences

Command-line tools become part of the engineering architecture rather than miscellaneous helper scripts.

---

# Decision 009

## Testing Never Uses Production Data

### Context

Automated tests must execute safely and consistently.

### Decision

Every automated test uses an isolated test database.

### Rationale

Testing must be deterministic and must never modify production archives.

### Consequences

Each test starts with a clean environment and can be executed repeatedly without side effects.

---

# Decision 010

## Documentation Evolves with the Platform

### Context

Engineering knowledge is often lost when projects grow.

### Decision

Architecture, engineering standards, testing strategy, and design decisions are documented as first-class project artifacts.

### Rationale

Documentation preserves architectural intent and reduces future maintenance costs.

### Consequences

Future contributors can understand not only how the platform works, but also why it was designed that way.

---

# Future Decisions

This document is intended to grow throughout the lifetime of the project.

Each new architectural decision should receive a permanent decision number.

Decision numbers should never be reused or renumbered.

As the platform evolves, this document becomes the engineering history of the DNS Measurement Platform.