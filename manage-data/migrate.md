---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-migrating-data.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-migrating-data.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-migrate-data2.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
---

# Migrate your {{es}} data

Transitioning between Elastic deployment types involves migrating your {{es}} data. The migration method to choose depends on your source and destination deployment types. Choose one of our guides for detailed steps.

Migrate your {{ech}} data to {{serverless-full}}:

- [Migrate with the reindex API](/manage-data/migrate/migrate-with-reindex-api.md)
- [Migrate with {{ls}}](/manage-data/migrate/migrate-with-logstash.md)

Migrate your data to {{ech}} or {{ece}}:

- [Migrate to {{ech}} or ECE](/manage-data/migrate/migrate-to-ech-or-ece.md)
- [Reindex using a private CA](/manage-data/migrate/migrate-from-a-self-managed-cluster-with-a-self-signed-certificate-using-remote-reindex.md) {applies_to}`ece: unavailable`

Migrate your data using snapshot and restore:

- [Minimal-downtime migration using snapshots](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md)
- [Migrate system indices](/manage-data/migrate/migrate-internal-indices.md)



