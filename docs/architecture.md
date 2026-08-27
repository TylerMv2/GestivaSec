# Gestiva Observability & Security Platform - Architectural Guide

This platform functions as a lightweight NOC/SOC operational dashboard running entirely in localhost on a Kali Linux environment. It is designed to monitor authorized components of the `gestivaone.com` infrastructure.

```
                  ┌─────────────────────────────────────┐
                  │          KALI LINUX HOST            │
                  │                                     │
                  │   ┌─────────────────────────────┐   │
                  │   │        Web Frontend         │   │
                  │   │   (HTML5, CSS3, JS, SVG)    │   │
                  │   └──────────────┬──────────────┘   │
                  │                  │                  │
                  │            REST Telemetry           │
                  │                  │                  │
                  │   ┌──────────────▼──────────────┐   │
                  │   │      FastAPI Gateway        │   │
                  │   └──────────────┬──────────────┘   │
                  │                  │                  │
                  │                  ├────────────────┐ │
                  │                  │                │ │
                  │   ┌──────────────▼──────────────┐ │ │
                  │   │    SQLite Database Engine   │ │ │
                  │   │     (gestiva_obs.db)        │ │ │
                  │   └──────────────▲──────────────┘ │ │
                  │                  │                │ │
                  │              Write Logs           │ │
                  │                  │                │ │
                  │   ┌──────────────┴──────────────┐ │ │
                  │   │      Collector Runner       │◄┘ │
                  │   │ (Asynchronous background)   │   │
                  │   └──────────────▲──────────────┘   │
                  │                  │                  │
                  └──────────────────┼──────────────────┘
                                     │
                             ICMP, SSL, DNS, TCP
                                     │
                                     ▼
                      ┌─────────────────────────────┐
                      │      gestivaone.com         │
                      │  (Authorized Target Assets) │
                      └─────────────────────────────┘
```

## Backend Engine (FastAPI)
The server initiates on `http://127.0.0.1:8000`. On load:
1. It validates the presence of SQLite database tables and seeds mock/default configuration values.
2. It launches an asynchronous `CollectorRunner` scheduler which spawns monitoring loops in independent daemon threads.
3. It opens HTTP routes for CRUD asset tracking, Kibana-style logs lookup, alerts lifecycle tracking, and SVG topology definitions.

## Collectors Layer
- **System Telemetry**: Localhost status is monitored via `psutil` which reports CPU, Memory, Disk, and Net IO throughput parameters.
- **Port Auditing**: Socket checks determine whether non-authorized TCP ports have been exposed.
- **TLS/SSL Audit**: SSL sockets verify validity windows and cipher suites negotiability.
- **Traffic Sniffing**: Uses `scapy` raw interface capture (falls back to high-fidelity simulated metadata packet flows if non-root).
