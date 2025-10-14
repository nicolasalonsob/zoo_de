#!/bin/bash 

podman run \
  --network pg_net \
  localhost/test_pipeline:v1 \
  --dialect postgresql \
  --user root \
  --psw root \
  --host postgresql_net \
  --port 5432 \
  --db ny_taxi \
  --table_name trips
