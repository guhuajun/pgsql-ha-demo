# pgsql-ha-demo
A project for demostrating a PostgreSQL cluster

## Topology

PostgreSQL servers are called P(rimary), R(eplica).
PGPool server are called pgpool.
Demo application are called A.
Utility servers are not included.

```
+---+     +---+
| P |--+--| R |
+---+  |  +---+
       |
+-------------+
|    pgpool   |
+-------------+
       |
     +---+
     | A |
     +---+
```

## Setup

1. Run following commands to start this lab.
```bash
docker-compose up
```

2. Waiting for PostgreSQL server to be started.
```
primary_1     | server started
```


3. Open following url to check dashboard:
```
Grafana: http://localhost:3000 (admin/password)
```

## Test
T.B.D

## Cleanup

Run following command to stop and remove all containers.
```bash
docker-compose down
```

## Note

Please feel free to extend the test steps.

## References
[CrunchyData/crunchy-containers](https://github.com/CrunchyData/crunchy-containers)