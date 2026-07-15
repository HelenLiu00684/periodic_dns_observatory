# System Architecture

**Project:** DNS Measurement Platform

**Version:** 1.0

---

# 1. Purpose

This document describes the overall architecture of the DNS Measurement Platform.

The platform is designed as a cloud-native observability system for collecting, archiving, processing, and visualizing DNS measurement data.

Rather than focusing on DNS resolution itself, the platform focuses on **network observability**, providing a standardized pipeline for transforming raw measurement data into searchable archives, telemetry metrics, dashboards, and APIs.

---

# 2. High-Level Architecture

```text
                    Platform Runtime
                           │
                           ▼
                    Service Manager
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
   Collector          Docker Runtime     Health Monitor
        │                  │                  │
        └──────────────────┴──────────────────┘
                           │
                           ▼
                Observation Normalizer
                           │
                           ▼
                 Canonical Observation
                           │
                           ▼
                  SQLite Archive Database
                           │
            ┌──────────────┼──────────────┐
            ▼              ▼              ▼
      Archive Tools   Telemetry Pipeline   FastAPI
                            │
                            ▼
                 Canonical Telemetry Metrics
                            │
                            ▼
                      InfluxDB Writer
                            │
                            ▼
                         InfluxDB
                            │
                            ▼
                         Grafana
                            │
                            ▼
                     REST API / Frontend
                            │
                            ▼
                       React Dashboard
```

---

# 3. Platform Components

The platform consists of several independent components.

Each component owns a single responsibility and communicates with other components through well-defined interfaces.

| Component | Responsibility |
|-----------|----------------|
| Platform Runtime | Start and manage platform services |
| Collector | Download measurement data |
| Observation Normalizer | Convert external data into the canonical observation model |
| SQLite Archive | Store normalized observations |
| Telemetry Pipeline | Generate canonical telemetry metrics |
| InfluxDB Writer | Store telemetry metrics |
| Grafana | Visualize telemetry data |
| FastAPI | Provide REST APIs |
| React Frontend | Present dashboards and interactive views |

---

# 4. Data Flow

The platform processes DNS measurements through a series of independent stages.

```text
RIPE Atlas

        │

        ▼

Collector

        │

        ▼

Observation Normalizer

        │

        ▼

Canonical Observation

        │

        ▼

SQLite Archive

        │

        ▼

Telemetry Pipeline

        │

        ▼

Canonical Telemetry Metrics

        │

        ▼

InfluxDB

        │

        ▼

Grafana

        │

        ▼

REST API

        │

        ▼

React Frontend
```

Each stage performs one clearly defined task.

Data always flows in a single direction.

---

# 5. Layer Responsibilities

The platform follows a layered architecture.

Each layer owns exactly one primary responsibility.

```text
Platform Runtime

↓

Collection

↓

Normalization

↓

Archive

↓

Telemetry

↓

Time-Series Storage

↓

Visualization

↓

API

↓

Frontend
```

No layer should bypass another layer.

For example:

- Grafana never reads SQLite directly.
- The Collector never writes to InfluxDB.
- The Database Layer never generates telemetry metrics.
- Frontend applications never access SQLite directly.

---

# 6. Canonical Models

The platform defines two canonical data models.

## Canonical Observation

The Observation model represents a complete normalized network observation.

Every supported protocol must first be transformed into this common format before entering the archive.

## Canonical Telemetry Metric

Telemetry metrics are generated from archived observations.

These metrics remain independent of any particular time-series database.

Storage-specific writers convert canonical metrics into backend-specific formats.

---

# 7. Platform Runtime

The Platform Runtime is responsible for coordinating the entire system.

Typical responsibilities include:

- Initialize platform configuration
- Create the archive database
- Initialize database schema
- Start required Docker containers
- Launch the collector
- Import historical observations
- Start backend services
- Perform health checks
- Shut down services gracefully

The Platform Runtime serves as the orchestration layer for the entire platform.

---

# 8. Future Expansion

The architecture is intentionally designed for long-term evolution.

Future components may include:

- BGP Routing Platform
- Traceroute Measurements
- Streaming Telemetry
- SNMP Collection
- AI Analytics
- Additional Time-Series Databases
- Alternative Frontend Implementations

These additions should integrate into the existing architecture without requiring major redesign.

---

# 9. Architecture Principles

The DNS Measurement Platform follows several fundamental engineering principles.

- Single Responsibility
- Layer Separation
- Platform Independence
- Canonical Data Models
- Testability
- Extensibility
- Operational Simplicity

Every architectural decision should reinforce these principles.

---

# 10. Summary

The DNS Measurement Platform is designed as a modular observability platform rather than a collection of independent scripts.

By separating collection, normalization, archival storage, telemetry generation, visualization, and runtime management into independent components, the platform remains maintainable, testable, and extensible as additional network technologies are introduced.