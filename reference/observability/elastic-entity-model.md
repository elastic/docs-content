---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/elastic-entity-model.html
---

# Elastic Entity Model [elastic-entity-model]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


The Elastic Entity Model consists of:

* a data model and related entity indices
* an Entity Discovery Framework, which consists of [transforms](/explore-analyze/transforms.md) and [Ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md) that read from signal indices and write data to entity indices
* a set of management APIs that empower entity-centric Elastic solution features and workflows

In the context of Elastic Observability, an *entity* is an object of interest that can be associated with produced telemetry and identified as unique. Note that this definition is intentionally closely aligned to the work of the [OpenTelemetry Entities SIG](https://github.com/open-telemetry/oteps/blob/main/text/entities/0256-entities-data-model.md#data-model). Examples of entities include (but are not limited to) services, hosts, and containers.

The concept of an entity is important as a means to unify observability signals based on the underlying entity that the signals describe.

::::{note}
* The Elastic Entity Model currently supports the [new Inventory experience](/solutions/observability/apps/inventory.md) limited to service, host, and container entities.
* During Technical Preview, Entity Discovery Framework components are not enabled by default.

::::



## Enable the Elastic Entity Model [_enable_the_elastic_entity_model]

You can enable the Elastic Entity Model from the new [Inventory](/solutions/observability/apps/inventory.md). If already enabled, you will not be prompted to enable the Elastic Entity Model.

The following {{es}} privileges are required:

|     |     |
| --- | --- |
| **Index privileges** | names: [`.entities*`], privileges: [`create_index`, `index`, `create_doc`, `auto_configure`, `read`]<br>names: [`logs-*`, `filebeat*`, `metrics-*`, `metricbeat*`, `traces-*`, `.entities*`], privileges: [`read`, `view_index_metadata`] |
| **Cluster privileges** | `manage_transform`, `manage_ingest_pipelines`, `manage_index_templates` |
| **Application privileges** | application: `kibana-.kibana`, privileges: [`saved_object:entity-definition/*`, `saved_object:entity-discovery-api-key/*`], resources: [*] |

For more information, refer to [Security privileges](elasticsearch://docs/reference/elasticsearch/security-privileges.md) in the {{es}} documentation.


## Disable the Elastic Entity Model [_disable_the_elastic_entity_model]

From the Dev Console, run the command: `DELETE kbn:/internal/entities/managed/enablement`

The following {{es}} privileges are required to delete {{es}} resources:

|     |     |
| --- | --- |
| **Index privileges** | names: [`.entities*`], privileges: [`delete_index`] |
| **Cluster privileges** | `manage_transform`, `manage_ingest_pipelines`, `manage_index_templates` |
| **Application privileges** | application: `kibana-.kibana`, privileges: [`saved_object:entity-definition/delete`, `saved_object:entity-discovery-api-key/delete`], resources: [*] |


## Limitations [elastic-entity-model-limitations]

* [Cross-cluster search (CCS)](/solutions/search/cross-cluster-search.md) is not supported. EEM cannot leverage data stored on a remote cluster.
* Services are only detected from documents where `service.name` is detected in index patterns that match either `logs-*` or `apm-*`.
