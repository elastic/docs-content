---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/use-elasticsearch-for-time-series-data.html
---

# Use case: use Elasticsearch to manage time series data [use-elasticsearch-for-time-series-data]

{{es}} offers features to help you store, manage, and search time series data, such as logs and metrics. Once in {{es}}, you can analyze and visualize your data using {{kib}} and other {{stack}} features.


## Set up data tiers [set-up-data-tiers]

{{es}}'s [{{ilm-init}}](lifecycle/index-lifecycle-management.md) feature uses [data tiers](lifecycle/data-tiers.md) to automatically move older data to nodes with less expensive hardware as it ages. This helps improve performance and reduce storage costs.

The hot and content tiers are required. The warm, cold, and frozen tiers are optional.

Use high-performance nodes in the hot and warm tiers for faster indexing and faster searches on your most recent data. Use slower, less expensive nodes in the cold and frozen tiers to reduce costs.

The content tier is not typically used for time series data. However, it’s required to create system indices and other indices that aren’t part of a data stream.

The steps for setting up data tiers vary based on your deployment type:

:::::::{tab-set}

::::::{tab-item} {{ech}}
1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
2. Add or select your deployment from the {{ecloud}} home page or the **Deployments** page.
3. From your deployment menu, select **Edit deployment**.
4. To enable a data tier, click **Add capacity**.

**Enable autoscaling**

[Autoscaling](../deploy-manage/autoscaling.md) automatically adjusts your deployment’s capacity to meet your storage needs. To enable autoscaling, select **Autoscale this deployment** on the **Edit deployment** page. Autoscaling is only available for {{ech}}.
::::::

::::::{tab-item} Self-managed
To assign a node to a data tier, add the respective [node role](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/node-settings.md#node-roles) to the node’s `elasticsearch.yml` file. Changing an existing node’s roles requires a [rolling restart](../deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling).

```yaml
# Content tier
node.roles: [ data_content ]

# Hot tier
node.roles: [ data_hot ]

# Warm tier
node.roles: [ data_warm ]

# Cold tier
node.roles: [ data_cold ]

# Frozen tier
node.roles: [ data_frozen ]
```

We recommend you use dedicated nodes in the frozen tier. If needed, you can assign other nodes to more than one tier.

```yaml
node.roles: [ data_content, data_hot, data_warm ]
```

Assign your nodes any other roles needed for your cluster. For example, a small cluster may have nodes with multiple roles.

```yaml
node.roles: [ master, ingest, ml, data_hot, transform ]
```
::::::

:::::::

## Register a snapshot repository [register-snapshot-repository]

The cold and frozen tiers can use [{{search-snaps}}](../deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md) to reduce local storage costs.

To use {{search-snaps}}, you must register a supported snapshot repository. The steps for registering this repository vary based on your deployment type and storage provider:

:::::::{tab-set}

::::::{tab-item} {{ech}}
When you create a cluster, {{ech}} automatically registers a default [`found-snapshots`](../deploy-manage/tools/snapshot-and-restore.md) repository. This repository supports {{search-snaps}}.

The `found-snapshots` repository is specific to your cluster. To use another cluster’s default repository, refer to the Cloud [Snapshot and restore](../deploy-manage/tools/snapshot-and-restore.md) documentation.

You can also use any of the following custom repository types with {{search-snaps}}:

* [Google Cloud Storage (GCS)](../deploy-manage/tools/snapshot-and-restore/ec-gcs-snapshotting.md)
* [Azure Blob Storage](../deploy-manage/tools/snapshot-and-restore/ec-azure-snapshotting.md)
* [Amazon Web Services (AWS)](../deploy-manage/tools/snapshot-and-restore/ec-aws-custom-repository.md)
::::::

::::::{tab-item} Self-managed
Use any of the following repository types with searchable snapshots:

* [AWS S3](../deploy-manage/tools/snapshot-and-restore/s3-repository.md)
* [Google Cloud Storage](../deploy-manage/tools/snapshot-and-restore/google-cloud-storage-repository.md)
* [Azure Blob Storage](../deploy-manage/tools/snapshot-and-restore/azure-repository.md)
* [Hadoop Distributed File Store (HDFS)](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch-plugins/repository-hdfs.md)
* [Shared filesystems](../deploy-manage/tools/snapshot-and-restore/shared-file-system-repository.md) such as NFS
* [Read-only HTTP and HTTPS repositories](../deploy-manage/tools/snapshot-and-restore/read-only-url-repository.md)

You can also use alternative implementations of these repository types, for instance [MinIO](../deploy-manage/tools/snapshot-and-restore/s3-repository.md#repository-s3-client), as long as they are fully compatible. Use the [Repository analysis](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-repository-analyze) API to analyze your repository’s suitability for use with searchable snapshots.
::::::

:::::::

## Create or edit an index lifecycle policy [create-edit-index-lifecycle-policy]

A [data stream](data-store/data-streams.md) stores your data across multiple backing indices. {{ilm-init}} uses an [index lifecycle policy](lifecycle/index-lifecycle-management/index-lifecycle.md) to automatically move these indices through your data tiers.

If you use {{fleet}} or {{agent}}, edit one of {{es}}'s built-in lifecycle policies. If you use a custom application, create your own policy. In either case, ensure your policy:

* Includes a phase for each data tier you’ve configured.
* Calculates the threshold, or `min_age`, for phase transition from rollover.
* Uses {{search-snaps}} in the cold and frozen phases, if wanted.
* Includes a delete phase, if needed.

:::::::{tab-set}

::::::{tab-item} Fleet or Elastic Agent
{{fleet}} and {{agent}} use the following built-in lifecycle policies:

* `logs`
* `metrics`
* `synthetics`

You can customize these policies based on your performance, resilience, and retention requirements.

To edit a policy in {{kib}}, open the main menu and go to **Stack Management > Index Lifecycle Policies**. Click the policy you’d like to edit.

You can also use the [update lifecycle policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle).

```console
PUT _ilm/policy/logs
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_primary_shard_size": "50gb"
          }
        }
      },
      "warm": {
        "min_age": "30d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          }
        }
      },
      "cold": {
        "min_age": "60d",
        "actions": {
          "searchable_snapshot": {
            "snapshot_repository": "found-snapshots"
          }
        }
      },
      "frozen": {
        "min_age": "90d",
        "actions": {
          "searchable_snapshot": {
            "snapshot_repository": "found-snapshots"
          }
        }
      },
      "delete": {
        "min_age": "735d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```
::::::

::::::{tab-item} Custom application
To create a policy in {{kib}}, open the main menu and go to **Stack Management > Index Lifecycle Policies**. Click **Create policy**.

You can also use the [update lifecycle policy API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle).

```console
PUT _ilm/policy/my-lifecycle-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_primary_shard_size": "50gb"
          }
        }
      },
      "warm": {
        "min_age": "30d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          },
          "forcemerge": {
            "max_num_segments": 1
          }
        }
      },
      "cold": {
        "min_age": "60d",
        "actions": {
          "searchable_snapshot": {
            "snapshot_repository": "found-snapshots"
          }
        }
      },
      "frozen": {
        "min_age": "90d",
        "actions": {
          "searchable_snapshot": {
            "snapshot_repository": "found-snapshots"
          }
        }
      },
      "delete": {
        "min_age": "735d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```
::::::

:::::::

## Create component templates [create-ts-component-templates]

::::{tip}
If you use {{fleet}} or {{agent}}, skip to [Search and visualize your data](#search-visualize-your-data). {{fleet}} and {{agent}} use built-in templates to create data streams for you.
::::


If you use a custom application, you need to set up your own data stream. A data stream requires a matching index template. In most cases, you compose this index template using one or more component templates. You typically use separate component templates for mappings and index settings. This lets you reuse the component templates in multiple index templates.

When creating your component templates, include:

* A [`date`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/date.md) or [`date_nanos`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/date_nanos.md) mapping for the `@timestamp` field. If you don’t specify a mapping, {{es}} maps `@timestamp` as a `date` field with default options.
* Your lifecycle policy in the `index.lifecycle.name` index setting.

::::{tip}
Use the [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current) when mapping your fields. ECS fields integrate with several {{stack}} features by default.

If you’re unsure how to map your fields, use [runtime fields](data-store/mapping/define-runtime-fields-in-search-request.md) to extract fields from [unstructured content](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/keyword.md#mapping-unstructured-content) at search time. For example, you can index a log message to a `wildcard` field and later extract IP addresses and other data from this field during a search.

::::


To create a component template in {{kib}}, open the main menu and go to **Stack Management > Index Management**. In the **Index Templates** view, click **Create component template**.

You can also use the [create component template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template).

```console
# Creates a component template for mappings
PUT _component_template/my-mappings
{
  "template": {
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date",
          "format": "date_optional_time||epoch_millis"
        },
        "message": {
          "type": "wildcard"
        }
      }
    }
  },
  "_meta": {
    "description": "Mappings for @timestamp and message fields",
    "my-custom-meta-field": "More arbitrary metadata"
  }
}

# Creates a component template for index settings
PUT _component_template/my-settings
{
  "template": {
    "settings": {
      "index.lifecycle.name": "my-lifecycle-policy"
    }
  },
  "_meta": {
    "description": "Settings for ILM",
    "my-custom-meta-field": "More arbitrary metadata"
  }
}
```


## Create an index template [create-ts-index-template]

Use your component templates to create an index template. Specify:

* One or more index patterns that match the data stream’s name. We recommend using our [data stream naming scheme](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/data-streams.md#data-streams-naming-scheme).
* That the template is data stream enabled.
* Any component templates that contain your mappings and index settings.
* A priority higher than `200` to avoid collisions with built-in templates. See [Avoid index pattern collisions](data-store/templates.md#avoid-index-pattern-collisions).

To create an index template in {{kib}}, open the main menu and go to **Stack Management > Index Management**. In the **Index Templates** view, click **Create template**.

You can also use the [create index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template). Include the `data_stream` object to enable data streams.

```console
PUT _index_template/my-index-template
{
  "index_patterns": ["my-data-stream*"],
  "data_stream": { },
  "composed_of": [ "my-mappings", "my-settings" ],
  "priority": 500,
  "_meta": {
    "description": "Template for my time series data",
    "my-custom-meta-field": "More arbitrary metadata"
  }
}
```


## Add data to a data stream [add-data-to-data-stream]

[Indexing requests](data-store/data-streams/use-data-stream.md#add-documents-to-a-data-stream) add documents to a data stream. These requests must use an `op_type` of `create`. Documents must include a `@timestamp` field.

To automatically create your data stream, submit an indexing request that targets the stream’s name. This name must match one of your index template’s index patterns.

```console
PUT my-data-stream/_bulk
{ "create":{ } }
{ "@timestamp": "2099-05-06T16:21:15.000Z", "message": "192.0.2.42 - - [06/May/2099:16:21:15 +0000] \"GET /images/bg.jpg HTTP/1.0\" 200 24736" }
{ "create":{ } }
{ "@timestamp": "2099-05-06T16:25:42.000Z", "message": "192.0.2.255 - - [06/May/2099:16:25:42 +0000] \"GET /favicon.ico HTTP/1.0\" 200 3638" }

POST my-data-stream/_doc
{
  "@timestamp": "2099-05-06T16:21:15.000Z",
  "message": "192.0.2.42 - - [06/May/2099:16:21:15 +0000] \"GET /images/bg.jpg HTTP/1.0\" 200 24736"
}
```


## Search and visualize your data [search-visualize-your-data]

To explore and search your data in {{kib}}, open the main menu and select **Discover**. See {{kib}}'s [Discover documentation](../explore-analyze/discover.md).

Use {{kib}}'s **Dashboard** feature to visualize your data in a chart, table, map, and more. See {{kib}}'s [Dashboard documentation](../explore-analyze/dashboards.md).

You can also search and aggregate your data using the [search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search). Use [runtime fields](data-store/mapping/define-runtime-fields-in-search-request.md) and [grok patterns](../explore-analyze/scripting/grok.md) to dynamically extract data from log messages and other unstructured content at search time.

```console
GET my-data-stream/_search
{
  "runtime_mappings": {
    "source.ip": {
      "type": "ip",
      "script": """
        String sourceip=grok('%{IPORHOST:sourceip} .*').extract(doc[ "message" ].value)?.sourceip;
        if (sourceip != null) emit(sourceip);
      """
    }
  },
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "@timestamp": {
              "gte": "now-1d/d",
              "lt": "now/d"
            }
          }
        },
        {
          "range": {
            "source.ip": {
              "gte": "192.0.2.0",
              "lte": "192.0.2.255"
            }
          }
        }
      ]
    }
  },
  "fields": [
    "*"
  ],
  "_source": false,
  "sort": [
    {
      "@timestamp": "desc"
    },
    {
      "source.ip": "desc"
    }
  ]
}
```

{{es}} searches are synchronous by default. Searches across frozen data, long time ranges, or large datasets may take longer. Use the [async search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-async-search-submit) to run searches in the background. For more search options, see [*The search API*](../solutions/search/querying-for-search.md).

```console
POST my-data-stream/_async_search
{
  "runtime_mappings": {
    "source.ip": {
      "type": "ip",
      "script": """
        String sourceip=grok('%{IPORHOST:sourceip} .*').extract(doc[ "message" ].value)?.sourceip;
        if (sourceip != null) emit(sourceip);
      """
    }
  },
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "@timestamp": {
              "gte": "now-2y/d",
              "lt": "now/d"
            }
          }
        },
        {
          "range": {
            "source.ip": {
              "gte": "192.0.2.0",
              "lte": "192.0.2.255"
            }
          }
        }
      ]
    }
  },
  "fields": [
    "*"
  ],
  "_source": false,
  "sort": [
    {
      "@timestamp": "desc"
    },
    {
      "source.ip": "desc"
    }
  ]
}
```
