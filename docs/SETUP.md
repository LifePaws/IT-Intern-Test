# Local WP + Import Notes

## Environment

- Docker + docker compose
- `docker-compose.yml` runs MySQL 8 + WordPress 6.6 (PHP 8.2) + a WP-CLI sidecar

## Run

```bash
docker compose up -d
./scripts/setup.sh            # or: pwsh scripts/setup.ps1
```
