#!/bin/bash
docker compose up -d backend
docker compose run \
  --entrypoint "python3 -m pytest" \
  -e "DATABASE_NAME=test_your_app" \
  --rm \
  backend \
  --disable-warnings -p no:cacheprovider "$@"
