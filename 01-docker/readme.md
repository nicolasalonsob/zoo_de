# 🐳 Docker Networking Explained

## 🌐 1. What Is a Docker Network?
Docker creates **virtual networks** so that containers can communicate with each other securely and efficiently. Think of it as a **private Wi-Fi** for your containers.

---

## 🏠 2. Analogy: Your Home Network
Imagine your home setup:

| Concept | Real World | Docker Equivalent |
|----------|-------------|------------------|
| Router | Your Wi-Fi router | Docker network (bridge) |
| Devices | Laptop, TV, phone | Containers (pgadmin, postgres, etc.) |
| Device name | smart-tv.local | Container name (postgres) |
| Public IP + port forwarding | Router’s external IP + port 8080 | Host port mapping (`5433:5432`) |

All your home devices can talk to each other using private IPs — that’s your **internal network**. But if someone outside your home wants to access something, they need to go through your router’s public IP and an **exposed port**.

---

## 🧩 3. Docker Network Basics

- **Bridge network (default):** The private network Docker creates for containers in the same `docker-compose`.
- **Container names = DNS hostnames:** Containers can talk to each other using their service names.
  ```bash
  # Example: inside pgadmin container
  ping postgres
  ```
- **Each container gets its own IP** in the bridge network.
  ```bash
  docker inspect postgres | grep IPAddress
  ```

---

## 🧭 4. Internal vs External Access

| From | Connect To | How |
|------|-------------|-----|
| Another container | `postgres:5432` | Internal Docker network |
| Host machine (your laptop) | `localhost:5433` | Port forwarding defined in docker-compose |
| Outside your host (Internet) | ❌ Not accessible by default | Must expose ports explicitly |

---

## 🧱 5. Example docker-compose.yml
```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - '8080:80'
```

### 🔗 Connection Summary
| Client | Hostname | Port |
|---------|-----------|------|
| **pgadmin → postgres** | `postgres` | `5432` |
| **Host (laptop) → postgres** | `localhost` | `5433` |
| **Host (laptop) → pgadmin** | `localhost` | `8080` |

---

## 🕸️ 6. Diagram – Internal vs External Network

```text
                   ┌───────────────────────────────┐
                   │        Host Machine            │
                   │                               │
                   │  localhost:5433  ─────┐       │
                   │  localhost:8080  ───┐ │       │
                   └──────────┬─────────┘ │       │
                              │           │
                              ▼           ▼
                     ┌───────────────────────────────┐
                     │      Docker Bridge Network     │
                     │    (Private Internal Network)  │
                     │                               │
                     │  [postgres] :5432   ◄────────────┐
                     │  [pgadmin]  :80     ─────────────►│
                     │                               │
                     └───────────────────────────────┘
```

---

## 🧱 7. Multiple Databases in One Network
You can have multiple Postgres containers without conflict:
```yaml
services:
  postgres_1:
    image: postgres
  postgres_2:
    image: postgres
```
Each gets a unique internal IP (e.g. `172.18.0.2`, `172.18.0.3`) and can be reached by its container name.

---

## 🧠 8. Key Takeaways
- Docker creates **private virtual networks** for containers.
- Containers communicate internally using **service names**.
- Port mappings (`HOST:CONTAINER`) are for external access.
- Multiple containers can coexist without conflict thanks to isolated IPs.

---

✅ **Summary:** Think of Docker networking like your home Wi-Fi — private inside, accessible outside only if you open the door (ports).