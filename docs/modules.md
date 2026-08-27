# Gestiva Observability & Security Platform - Modular Description

## Backend Modules

### 1. `backend/config/settings.py`
Parses environment definitions from `.env`. Sets up defaults for ports, connection paths, and credential paths.

### 2. `backend/database/`
- `connection.py`: Manages SQLAlchemy sessions and connects to local SQLite.
- `db_init.py`: Seeds initial targets (Cloudflare external domain and local Kali Linux box) and default user models (Admin, Operator, ReadOnly).

### 3. `backend/models/`
Sets up ORM entities corresponding to the SQLite tables:
- `host.py`
- `service.py`
- `alert.py`
- `event.py`
- `traffic.py`
- `history.py`
- `log.py`
- `inventory.py`
- `certificate.py`
- `user.py`
- `config.py`
- `settings.py`

### 4. `backend/collectors/`
- `base.py`: Declares log wrappers and alert handlers.
- `ping_collector.py`: Collects ICMP status.
- `dns_collector.py`: Measures DNS lookup times.
- `http_collector.py` & `https_collector.py`: Evaluates web servers response headers and code.
- `tls_collector.py`: Resolves public TLS metadata.
- `ssh_collector.py`: Checks SSH server baners and attempts login logic.
- `port_collector.py`: Audits active port exposures.
- `system_collector.py`: Tracks local Kali system resources.
- `traffic_collector.py`: Sniffs TCP packets and models IP flow summaries.

## Frontend Templates
All UI templates use the responsive Cyberpunk style layout with custom neon components:
- `index.html`: NOC/SOC summary.
- `technical.html`: NOC details panel.
- `executive.html`: High level metrics.
- `health.html`: Component state indicators.
- `inventory.html`: Active hosts registration.
- `logs.html`: Kibana-style logs view.
- `alerts.html`: Alert boards.
- `topology.html`: Mapped network paths.
- `settings.html`: Collector intervals.
