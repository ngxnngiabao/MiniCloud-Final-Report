# MiniCloud System Architecture
Dự án mô phỏng hệ thống Cloud Computing thu nhỏ với 9 thành phần Server.

## Công nghệ sử dụng
- Docker & Docker Compose
- Nginx (Reverse Proxy & Load Balancing)
- Flask (API Microservice)
- MariaDB (Database)
- Keycloak (SSO/OIDC)
- MinIO (Object Storage)
- Prometheus & Grafana (Monitoring)
- Bind9 (Internal DNS)

## Hướng dẫn cài đặt
1. Clone repo này về máy.
2. Chạy lệnh: `docker compose up -d --build`
3. Truy cập Web: `http://localhost:8080`