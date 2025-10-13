#!/bin/bash

HOST_DATA_PATH="./ny_taxi_postgres_data"

podman run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v "$HOST_DATA_PATH":/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
