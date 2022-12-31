#!/bin/bash

start() {
  docker compose up backend frontend "$@"
}

stop() {
  docker compose down
}

dump() {
  docker compose down --volumes
}

dev_data () {
  docker compose run --rm backend python3 app/dev_data.py
}

shell() {
  if [[ "$1" = "mongo" ]]; then
    docker compose exec -it mongo mongosh -u mongod -p Password123!
  else
    docker compose exec -it "$1" /bin/sh
  fi
}

if [[ $# -eq 0 ]]; then
  start "$@"
else
  CMD=$1
  shift
  $CMD "$@"
fi