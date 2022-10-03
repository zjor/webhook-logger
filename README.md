# Webhook Logger

## Overview
The service stores any JSON POST request to the database and allows to view request history with GET request.

[Demo](https://sleepy-reaches-84241.herokuapp.com/redoc)

### Features
- allows to group webhook logs under `/api/{entity}`
- allows to access stored request by ID
- stores request headers


## API Reference

- Store any payload:

```bash
$> curl -X POST https://sleepy-reaches-84241.herokuapp.com/api/example -H 'Content-Type: application/json' -d '{"paymentId": "abcde", "status": "pending"}'
```

- List stored requests

```bash
curl https://sleepy-reaches-84241.herokuapp.com/api/example
```

- List and limit requests

```bash
curl https://sleepy-reaches-84241.herokuapp.com/api/example?limit=3
```

- Get a single request by ID

```bash
curl https://sleepy-reaches-84241.herokuapp.com/api/example/611b7d4c-cbb1-4e18-9ebe-cc53829d22b0
```

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
- [ ] (?) delete records older then X days
- [x] run locally with docker-compose
- [x] show stats: `...{stats: {distinctNames: N, total: M}}, schemaVersion: 3, ...`
- [ ] add endpoint descriptions
