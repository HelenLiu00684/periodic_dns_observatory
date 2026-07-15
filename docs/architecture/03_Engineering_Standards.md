# Engineering Standards

**Project:** DNS Measurement Platform

**Version:** 1.0

---

# 1. Purpose

This document defines the engineering standards adopted by the DNS Measurement Platform.

Its purpose is to ensure that every component of the platform follows a consistent architecture, coding style, testing strategy, documentation format, and operational workflow.

These standards apply to all current and future modules, including Database, Collector, Observation, Telemetry, API, Frontend, and supporting infrastructure.

Engineering standards are intended to improve maintainability, readability, extensibility, and long-term project evolution.

---

# 2. Engineering Philosophy

The project is developed as a production-style platform rather than a collection of independent scripts.

Every module must satisfy the following principles:

- Single Responsibility
- Clear Layer Separation
- Platform Independence
- Testability
- Extensibility
- Readability
- Operational Simplicity

The platform emphasizes engineering quality over implementation speed.

---

# 3. Layered Architecture

The platform follows a layered architecture.

Each layer owns a clearly defined responsibility.

```text
Platform Runtime
        │
        ▼
Collector
        │
        ▼
Normalizer
        │
        ▼
Archive Database (SQLite)
        │
        ▼
Telemetry
        │
        ▼
Time-Series Database
        │
        ▼
Visualization
        │
        ▼
REST API
        │
        ▼
Frontend
```

Communication between layers must occur only through well-defined public interfaces.

Internal implementation details must never be accessed directly by higher layers.

---

# 4. Single Responsibility Principle

Every module shall have exactly one primary responsibility.

Examples:

| Module | Responsibility |
|----------|----------------|
| sqlite_connection | Database connection management |
| sqlite_schema | Database schema management |
| sqlite_writer | Archive persistence |
| sqlite_reader | Archive query interface |
| telemetry_builder | Canonical metric generation |
| influx_writer | Time-series persistence |

Modules shall never combine unrelated responsibilities.

---

# 5. Dependency Direction

Dependencies must always flow downward.

```text
Collector
        │
        ▼
Observation
        │
        ▼
SQLite
        │
        ▼
Telemetry
        │
        ▼
InfluxDB
```

Lower layers must never import higher layers.

Examples:

- SQLite must never import Telemetry.
- Database must never import FastAPI.
- Observation must never depend on SQLite.

---

# 6. Canonical Data Models

The platform owns its canonical data models.

External systems must adapt to the platform instead of influencing internal structures.

Canonical models currently include:

- Observation
- Canonical Telemetry Metric

Storage formats such as SQLite rows and InfluxDB Points are considered implementation details.

---

# 7. Naming Convention

Public APIs should clearly describe their intent.

Examples:

```python
insert_measurement()

fetch_raw_observations_after()

build_dns_metrics()

write_metrics()
```

Avoid ambiguous names such as:

```python
process()

handle()

get_data()

run()
```

Function names should explain what they return and why they exist.

---

# 8. Comment Convention

Comments exist to explain engineering decisions rather than obvious implementation details.

Good comments explain:

- Why this design exists
- Module responsibility
- Design assumptions
- Future evolution

Comments should not simply restate what the code already says.

---

# 9. Testing Convention

Every layer must be independently testable.

Testing is organized into four levels.

```text
Unit Test

↓

Integration Test

↓

Pipeline Test

↓

End-to-End Test
```

Production databases shall never be used during automated testing.

Every test should execute inside an isolated environment.

---

# 10. Tooling Convention

Operational tools are considered first-class components of the platform.

Typical operational tools include:

- Database Backup
- Database Reset
- Health Check
- Runtime Status
- Telemetry Import

Operational tools should be deterministic, repeatable, and suitable for automation.

---

# 11. Documentation Convention

Every engineering module should have corresponding documentation.

Documentation should describe:

- Purpose
- Architecture
- Public Interfaces
- Responsibilities
- Testing
- Future Extensions

Documentation should explain engineering design rather than implementation details.

---

# 12. Design Decisions

Significant architectural decisions shall be documented separately.

Each design decision should include:

- Context
- Decision
- Rationale
- Consequences

Architectural decisions become part of the project's long-term engineering knowledge.

---

# 13. Future Evolution

The platform is designed for continuous expansion.

Future modules may include:

- BGP Routing
- Streaming Telemetry
- Traceroute
- SNMP
- Additional Time-Series Databases
- Multiple Frontend Implementations

Future expansion should require minimal modification to existing modules.

---

# 14. Engineering Goal

The objective of this project is not only to build a functional DNS measurement platform, but also to establish a maintainable engineering foundation capable of supporting future network observability systems.

Every engineering decision should prioritize:

- Clarity
- Maintainability
- Extensibility
- Long-term Sustainability