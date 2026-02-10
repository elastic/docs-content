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

# Migrate your {{es}} data [migrate-your-elasticsearch-data]

Transitioning between Elastic deployment types involves migrating your {{es}} data. Some data can be transfered automatically, for example as part of a snapshot and restore procedure when you restore backed-up data into your new, destination {{es}} cluster.

To make sure that all of the data you want to migrate is moved over successfully, review the data types and migration options described here.


## Data types [migration-data-types]

Your migration options depend on the type of data that you need to migrate, which can be categorized into four groups:

- **Ingested user data**: All of the data that you've added into {{es}}, structured or unstructured, for your own applications.

- **{{es}} system data**: Configuration and state information stored in {{es}} [system indices](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#system-indices). This data is used by {{es}} for its internal operations.

- **{{kib}} saved objects**: Dashboards, visualizations, maps, data views, Canvas workpads, and any other objects that you've saved in {{kib}}.

- **Feature and component data**: Data stored in {{es}} that is specific to a given Elastic feature or component. This includes, for example, configuration data for {{fleet}} and {{integrations}}, {{watcher}} data, alerting rules and security detection rules, security data such as role mappings, API keys, and service tokens, and others.

## Migration options [migration-options]

Depending on the type of data that you need to move, various migration options are available:

 - **Reindex from source**: Reindexing into your destination deployment from the data's original source is often the most straightforward migration path.
 - **Snapshot and restore**: Create a backup of your running {{es}} cluster, and then migrate by restoring your data into a new cluster. Refer to [Snaphot and restore](/deploy-manage/tools/snapshot-and-restore.md) to learn more.
 - **Reindex API**: Copy documents from a source index to a destination index. You can reindex across clusters and deployment types and transform the data en route. 
 - **{{ls}}**: With {{ls}} you can collect, process, and forward data from a variety of sources to a variety of destinations. It serves as a highly configurable option available for migrating data across any deployment types.
 - **[Saved objects](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects) API**: Use this API for your {{kib}} saved 

The following table describes the migration options available for each data type:

| Data type | Migration options |
| ------ | ------ |
| Ingested user data | The reindex API, {{ls}}, and snapshot and restore migration options are available for your user data, with some restrictions based on the source and target deployment type. Refer to the [data migration guides](#data-migration-guides) listed on this page to learn more. |
| {{es}} system data | System indices must be migrated using the snapshot and restore [feature states](/deploy-manage/tools/snapshot-and-restore.md#feature-state) component. Refer to [Migrate system indices](/manage-data/migrate/migrate-internal-indices.md) for detailed migration steps. |
| {{kib}} saved objects | {{kib}} saved objects can be migrated using the Import and Export endpoints of the [Saved objects](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects) API. Refer to the API documentation or to [Import and export](/explore-analyze/find-and-organize/saved-objects.md#saved-objects-import-and-export) in the Explore and Analyze section. |
| Elastic feature and component data | Configuration data for products such as {{fleet}}, {{integrations}}, and {{watcher}} is typically migrated using the snapshot and restore feature. Refer to [Snaphot and restore](/deploy-manage/tools/snapshot-and-restore.md) and to the documentation for each specific product for additional detail. |

## Data migration guides [data-migration-guides]

Choose one of our guides for detailed steps to migrate {{es}} your {{es}} data.

Migrate your user data to {{serverless-full}}:

- [Migrate with the reindex API](/manage-data/migrate/migrate-with-reindex-api.md) {applies_to}`self: unavailable`
- [Migrate with {{ls}}](/manage-data/migrate/migrate-with-logstash.md)

Migrate your user data to {{ech}} or {{ece}}:

- [Migrate to {{ech}} or ECE](/manage-data/migrate/migrate-to-ech-or-ece.md)
- [Reindex using a private CA](/manage-data/migrate/migrate-from-a-self-managed-cluster-with-a-self-signed-certificate-using-remote-reindex.md) {applies_to}`ece: unavailable`

Migrate data using snapshot and restore, including system data:

- [Minimal-downtime migration using snapshots](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md)
- [Migrate system indices](/manage-data/migrate/migrate-internal-indices.md)



