---
navigation_title: Migrate data using snapshots
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: elasticsearch
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
---

# Migrate {{ech}} data using snapshots [migrate-using-snapshots]

A [snapshot](/deploy-manage/tools/snapshot-and-restore.md) is a backup of a running {{es}} cluster that includes both indexed documents and configuration data. As a migration path, you can take a new snapshot or use an existing one, and then restore it into a new, destination cluster. This is the recommended procedure for migrating system indices.

Learn about migrating your {{es}} data between Elastic deployment types by using snapshots:

 - [Minimal-downtime migration using snapshots](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md)

 - [Migrate system indices](/manage-data/migrate/migrate-internal-indices.md)
