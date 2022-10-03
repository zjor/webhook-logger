# Webhook Logger

## Overview
TODO

## API Reference
TODO

## How to

### Run dockerized version locally

1. `docker build -t webhook-logger .`
2. `docker run --rm -e DATABASE_URL=$DATABASE_URL -p 8000:8000 webhook-logger`

### Run with docker-compose

- `$> docker-compose up`

## TODO
- [x] store headers
- [x] add get entity by ID endpoint
- [x] accept limit param for number of entities
- [] (?) delete records older then X days
- [x] run locally with docker-compose
- [x] show stats: `...{stats: {distinctNames: N, total: M}}, schemaVersion: 3, ...`
