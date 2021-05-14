# Cicada Distributed Demos

These are applications to demonstrate use cases of Cicada Distributed.

- [Integration Test Example](rest-api/integration-tests)
- [Load Test Example](rest-api/load-test)
- [Stress Test Example](rest-api/stress-test)

## Example (Running Integration Test)

First, build the application:

```bash
cd rest-api/app
docker-compose build
```

Next, start the services:

```bash
WORKDIR=$(pwd) docker-compose up -d
```

Finally, go to the integration tests and start Cicada (you may have to start
the cluster):

```bash
cd ../integration-tests
cicada-distributed run
```
