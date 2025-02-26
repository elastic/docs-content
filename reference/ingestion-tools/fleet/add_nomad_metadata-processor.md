---
navigation_title: "add_nomad_metadata"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add_nomad_metadata-processor.html
---

# Add Nomad metadata [add_nomad_metadata-processor]


::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


The `add_nomad_metadata` processor adds fields with relevant metadata for applications deployed in Nomad.

Each event is annotated with the following information:

* Allocation name, identifier, and status
* Job name and type
* Namespace where the job is deployed
* Datacenter and region where the agent running the allocation is located.


## Example [_example_9]

```yaml
  - add_nomad_metadata: ~
```


## Configuration settings [_configuration_settings_11]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `address` | No | `http://127.0.0.1:4646` | URL of the agent API used to request the metadata. |
| `namespace` | No |  | Namespace to watch. If set, only events for allocations in this namespace are annotated. |
| `region` | No |  | Region to watch. If set, only events for allocations in this region are annotated. |
| `secret_id` | No |  | SecretID to use when connecting with the agent API. This is an example ACL policy to apply to the token.<br><br>```json<br>namespace "*" {<br>  policy = "read"<br>}<br>node {<br>  policy = "read"<br>}<br>agent {<br>  policy = "read"<br>}<br>```<br> |
| `refresh_interval` | No | `30s` | Interval used to update the cached metadata. |
| `cleanup_timeout` | No | `60s` | Time to wait before cleaning up an allocation’s associated resources after it has been removed.This is useful if you expect to receive events after an allocation has been removed, which can happen when collecting logs. |
| `scope` | No | `node` | Scope of the resources to watch.Specify `node` to get metadata for the allocations in a single agent, or `global`, to get metadata for allocations running on any agent. |
| `node` | No |  | When using `scope: node`, use `node` to specify the name of the local node if it cannot be discovered automatically.<br><br>For example, you can use the following configuration when {{agent}} is collecting events from all the allocations in the cluster:<br><br>```yaml<br>  - add_nomad_metadata:<br>      scope: global<br>```<br> |


## Indexers and matchers [_indexers_and_matchers]

Indexers and matchers are used to correlate fields in events with actual metadata. {{agent}} uses this information to know what metadata to include in each event.


### Indexers [_indexers_2]

Indexers use allocation metadata to create unique identifiers for each one of the Pods.

Available indexers are:

`allocation_name`
:   Identifies allocations by their name and namespace (as `<namespace>/<name>`)

`allocation_uuid`
:   Identifies allocations by their unique identifier.


### Matchers [_matchers_2]

Matchers are used to construct the lookup keys that match with the identifiers created by indexes.


#### `field_format` [_field_format]

Looks up allocation metadata using a key created with a string format that can include event fields.

This matcher has an option `format` to define the string format. This string format can contain placeholders for any field in the event.

For example, the following configuration uses the `allocation_name` indexer to identify the allocation metadata by its name and namespace, and uses custom fields existing in the event as match keys:

```yaml
- add_nomad_metadata:
    ...
    default_indexers.enabled: false
    default_matchers.enabled: false
    indexers:
      - allocation_name:
    matchers:
      - field_format:
          format: '%{[labels.nomad_namespace]}/%{[fields.nomad_alloc_name]}'
```


#### `fields` [_fields]

Looks up allocation metadata using as key the value of some specific fields. When multiple fields are defined, the first one included in the event is used.

This matcher has an option `lookup_fields` to define the fields whose value will be used for lookup.

For example, the following configuration uses the `allocation_uuid` indexer to identify allocations, and defines a matcher that uses some fields where the allocation UUID can be found for lookup, the first it finds in the event:

```yaml
- add_nomad_metadata:
    ...
    default_indexers.enabled: false
    default_matchers.enabled: false
    indexers:
      - allocation_uuid:
    matchers:
      - fields:
          lookup_fields: ['host.name', 'fields.nomad_alloc_uuid']
```


#### `logs_path` [_logs_path]

Looks up allocation metadata using identifiers extracted from the log path stored in the `log.file.path` field.

This matcher has an optional `logs_path` option with the base path of the directory containing the logs for the local agent.

The default configuration is able to lookup the metadata using the allocation UUID when the logs are collected under `/var/lib/nomad`.

For example the following configuration would use the allocation UUID when the logs are collected from `/var/lib/NomadClient001/alloc/<alloc UUID>/alloc/logs/...`.

```yaml
- add_nomad_metadata:
    ...
    default_indexers.enabled: false
    default_matchers.enabled: false
    indexers:
      - allocation_uuid:
    matchers:
      - logs_path:
          logs_path: '/var/lib/NomadClient001'
```

