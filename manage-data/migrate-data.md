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

Transitioning between Elastic deployment types involves migrating your {{es}} data. This page helps you plan your migration by describing the main categories of data you may need to move (ingested user data, {{es}} system data, {{kib}} saved objects, and feature-specific data), the migration methods available for each, and where to find step-by-step guides for your scenario.

## Data types [migration-data-types]

Your migration options depend on the type of data that you need to migrate, which can be categorized into four groups:

- **Ingested user data**: All of the data that you've added into {{es}}, structured or unstructured, for your own applications.

- **{{es}} system data**: Configuration and state information stored in {{es}} [system indices](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#system-indices). This data is used by {{es}} for its internal operations.

- **{{kib}} saved objects**: Dashboards, visualizations, maps, data views, Canvas workpads, and any other objects that you've saved in {{kib}}.

- **Feature and component data**: Data stored in {{es}} that is specific to a given Elastic feature or component. This includes, for example, configuration data for {{fleet}} and {{integrations}}, {{watcher}} data, alerting and security detection rules, security data such as role mappings, API keys, and service tokens, and others.

## Migration options [migration-options]

Depending on the type of data that you need to move, various migration options are available:

 - **Reindex from source**: For your own data, reindexing into your new, destination deployment from the data's original source is typically the most straightforward approach, since it's available without any need to consider differing {{es}} versions or deployment types.
 
    If you still have access to the original data source, outside of your former {{es}} cluster, you can load the data from there. You have the option to use any ingestion method that you want—{{ls}}, {{agent}}, {{beats}}, the {{es}} clients, or whatever works best for you.

    If the original source isn’t available or has other issues that make it non-viable, you can choose from one of the other migration options described here.
 - **Dual ingest**: For data with a limited lifecycle (logs and metrics, for example), another approach is to ingest into both the original and new environment at the same time, for a set duration. You can ingest into both environments for long enough for the data retention period to elapse. Then, after confirming that everything is working well in the new environment, the original environment can be shut down.
 - **Snapshot and restore**: Use a snapshot to create a backup of your running {{es}} cluster, and then migrate by restoring your data into a new cluster.
 - **Reindex API**: Copy documents from a source index to a destination index. You can reindex across clusters and deployment types and transform the data en route. 
 - **{{ls}}**: With {{ls}} you can collect, process, and forward data from a variety of sources to a variety of destinations. It serves as a highly configurable option available for migrating data across any deployment types.
 - **Saved objects API**: Use this API to migrate objects that you've saved in {{kib}}.
 - **{{kib}} saved object management**: You can also use the {{kib}} UI to migrate your saved objects.

The following table describes the migration options available for each data type and where to find guidance.

| Data type | Migration options |
| ------ | ------ |
| Ingested user data | The reindex API, snapshot and restore, and {{ls}} migration options are available for your user data, with some restrictions based on the source and target deployment type. Refer to [User data migration guides](#data-migration-guides) on this page to learn more. |
| {{es}} system data | System indices must be migrated using the snapshot and restore [feature states](/deploy-manage/tools/snapshot-and-restore.md#feature-state) component. Refer to [Migrate system indices](/manage-data/migrate/migrate-internal-indices.md) for detailed migration steps. |
| {{kib}} saved objects | {{kib}} saved objects can be migrated using the snapshot and restore [feature states](/deploy-manage/tools/snapshot-and-restore.md#feature-state) component or the {{kib}} import and export tools. The tools include the import and export endpoints of the [Saved objects API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects) and the [import and export](/explore-analyze/find-and-organize/saved-objects.md#saved-objects-import-and-export) options in the {{kib}} UI.<br><br>Snapshot and restore is generally the preferred migration method due to both speed and ease of use. In case you need to migrate {{fleet}} configuration data through snapshot and restore, this requires also restoring the {{kib}} feature state. |
| Elastic feature and component data | Configuration data for products such as {{fleet}}, {{integrations}}, and {{watcher}} is typically migrated using the snapshot and restore feature. Refer to [Snaphot and restore](/deploy-manage/tools/snapshot-and-restore.md) and to the documentation for each specific product for additional detail. |

<!--
## Data migration guides [data-migration-guides]

Choose one of our guides for detailed steps to migrate your {{es}} data.

Migrate your user data to {{serverless-full}}:

- [Migrate with the reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md)
- [Migrate with {{ls}}](/manage-data/migrate/migrate-with-logstash.md)

Migrate your user data to {{ech}} or {{ece}}:

- [Migrate to {{ech}} or ECE](/manage-data/migrate/migrate-to-ech-or-ece.md)
- [Reindex using a private CA](/manage-data/migrate/migrate-from-a-self-managed-cluster-with-a-self-signed-certificate-using-remote-reindex.md) {applies_to}`ece: unavailable`

Migrate data using snapshot and restore, including system data:

- [Minimal-downtime migration using snapshots](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md)
- [Migrate system indices](/manage-data/migrate/migrate-internal-indices.md)
-->


## User data migration guides [data-migration-guides]

To migrate your {{es}} ingested user data, choose one of the available migration options depending on your source and target deployment types.

**Migrate data to {{ech}}**:

| From | To | Supported Methods |
| --- | --- | --- |
| ECH | ECH | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| ECE | ECH | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| ECK | ECH | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| {{serverless-short}} | ECH | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| Self-managed | ECH | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md)*, [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
* See also [Reindex from a Self-managed cluster using a private CA](https://docs-v3-preview.elastic.dev/elastic/docs-content/pull/4914/manage-data/migrate/migrate-from-a-Self-managed-cluster-with-a-self-signed-certificate-using-remote-reindex)

**Migrate data to {{ece}}**:

| From | To | Supported Methods |
| --- | --- | --- |
| ECH | ECE | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| ECE | ECE | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| ECK | ECE | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| {{serverless-short}} | ECE | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| Self-managed | ECE | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |

**Migrate data to {{eck}}**:

| From | To | Supported Methods |
| --- | --- | --- |
| ECH | ECK | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| ECE | ECK | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| ECK | ECK | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| {{serverless-short}} | ECK | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| Self-managed | ECK | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |

**Migrate data to {{serverless-full}}**:

| From | To | Supported Methods |
| --- | --- | --- |
| ECH | {{serverless-short}} | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md) {applies_to}`serverless: preview 9.3+`, [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| ECE | {{serverless-short}} | [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| ECK | {{serverless-short}} | [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| {{serverless-short}} | {{serverless-short}} | [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| Self-managed | {{serverless-short}} | [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |

**Migrate data to Elastic self-managed**:

| From | To | Supported Methods |
| --- | --- | --- |
| ECH | Self-managed | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |  
| ECE | Self-managed | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| ECK | Self-managed | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| {{serverless-short}} | Self-managed | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |
| Self-managed | Self-managed | [Reindex API](/manage-data/migrate/migrate-data-using-reindex-api.md), [Snapshot and restore](/manage-data/migrate/migrate-data-between-elasticsearch-clusters-with-minimal-downtime.md), [{{ls}}](/manage-data/migrate/migrate-with-logstash.md) |

