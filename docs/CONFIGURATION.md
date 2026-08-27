# Gestiva Security — Environment Configuration Reference (`.env`)

This reference manual lists all configuration parameters managed via environment variables and `.env`.

| Variable | Default Value | Description |
| :--- | :--- | :--- |
| `ENVIRONMENT` | `development` | Runtime environment (`development`, `staging`, `production`) |
| `HOST` | `0.0.0.0` | Bind IP address for FastAPI server |
| `PORT` | `8000` | Port for REST API server |
| `LOG_LEVEL` | `INFO` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |
| `DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/gestivasec` | Database connection URL |
| `STORAGE_PATH` | `./storage` | Directory path for evidence and report files |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis event broker URL |
| `SECRET_KEY` | `super-secret-key-change-in-production-2026` | Application secret key |
| `JWT_SECRET` | `super-secret-jwt-key-change-in-production-2026` | Secret key used for signing JWT tokens |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | JWT token expiration time in minutes |
| `CORS_ORIGINS` | `http://localhost:8000,http://localhost:3000` | Allowed CORS origins (comma-separated) |
