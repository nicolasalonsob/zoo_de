#!/bin/bash

podman run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network pg_net \
  --name pgadmin_net \
  dpage/pgadmin4
