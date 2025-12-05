---
navigation_title: Migrate Elastic Cloud Hosted data to Serverless with Logstash
applies_to:
  stack: ga
  deployment:
    ess: ga
    ece: ga
products:
  - id: elasticsearch
  - id: logstash
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
---

# Migrate {{ech}} data to {{serverless-full}} with {{ls}} [migrate-with-ls]

[{{ls}}](logstash://reference/index.md) is a data collection engine that uses a large ecosystem of [plugins](logstash-docs-md://lsr/index.md) to collect, process, and forward data from a variety of sources to a variety of destinations. Here we focus on using the [Elasticsearch input](logstash-docs-md://lsr/plugins-inputs-elasticsearch.md) plugin to read from your {{ech}} deployment, and the [Elasticsearch output](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md) plugin to write to your {{{serverless-full}} project.

Familiarity with {{ech}}, {{es}}, and {{ls}} is helpful, but not required. 

:::{admonition} Basic migration
This guide focuses on a basic data migration scenario for moving static data from an {{ech}} deployment to a {{serverless-full}} project. 

Dashboards, visualizations, pipelines, templates, and other {{kib}} assets must be migrated separately using the {{kib}} [export/import APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-saved-objects) or recreated manually.
:::

The Elasticsearch input plugin offers [additional configuration options](#additional-config) that can support more advanced use cases and migrations. More information about those options is available near the end of this topic. 

## Prerequisites [migrate-prereqs]

- {{ech}} deployment with data to migrate
- [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md) project configured and running
- {{ls}} [installed](https://www.elastic.co/downloads/logstash) on your local machine or server 
- API keys in {{ls}} format for authentication with both deployments


## Process overview [migration-overview]
* [Configure {{ls}}](#configure-ls)
* [Run {{ls}}](#run-ls)
* [Verify data migration](#verify-migration)


### Step 1: Configure {{ls}} [configure-ls]
Create a new {{ls}} [pipeline configuration file](logstash://reference/creating-logstash-pipeline.md) (_migration.conf_) using the [Elasticsearch input](logstash-docs-md://lsr/plugins-inputs-elasticsearch.md) and the [Elasticsearch output](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md):
- The **input** reads from your {{ech}}.
- The **output** writes to your {{serverless-full}} project.

#### Input: Read from your {{ech}} deployment [read-from-ech]

```
input {
  elasticsearch {
    cloud_id => "<HOSTED_DEPLOYMENT_CLOUD_ID>"   # Connects Logstash to your Elastic Cloud Hosted deployment using its Cloud ID.
    api_key  => "<HOSTED_API_KEY>"               # API key for authenticating the connection.
    index    => "index_pattern*"                 # The index or index pattern (such as logs-*,metrics-*).
    docinfo  => true                             # Includes metadata about each document, such as its original index name or doc ID. This setting preserves index names on the destination cluster. 
  }
}
```

  :::{tip}
  To migrate multiple indexes at the same time, use a wildcard in the index name. For example, `index => "logs-*"` migrates all indices starting with `logs-`.
  :::

#### Output: Write to your {{serverless-full}} project [write-to-serverless]

```
output {
  elasticsearch {
    hosts       => [ "https://<SERVERLESS_HOST_URL>:443" ] # URL for your Serverless project URL, set port as 443
    api_key     => "<SERVERLESS_API_KEY>"                  # API key (in Logstash format) for your Serverless project
    ssl_enabled => true
    index       => "%{[@metadata][input][elasticsearch][_index]}" # Instruction to retain original index names
  }

  stdout { codec => rubydebug { metadata => true } }
}
```

:::{tip}
When you create an [API key for {{ls}}](logstash://reference/connecting-to-serverless.md#api-key), be sure to select **Logstash** from the **API key** format dropdown. This option formats the API key in the correct `id:api_key` format required by {{ls}}.
:::

### Step 2: Run {{ls}} [run-ls]
 
Start {{ls}}:

```
bin/logstash -f migration.conf
```

### Step 3: Verify data migration [verify-migration]

After running {{ls}}, verify that the data has been migrated successfully:

1. Log in to your {{serverless-full}} project.
2. Navigate to Index Management and select the relevant index.
3. Confirm that the migrated data is visible.


## Additional configuration options [additional-config]

The Elasticsearch input includes more [configuration options](logstash-docs-md://lsr/plugins-inputs-elasticsearch.md#plugins-inputs-elasticsearch-options) 
that offer greater flexibility and can handle more advanced migrations.
Some options that can be particularly relevant for a  migration use case are: 

- `size` - Controls how many documents are retrieved per scroll. Larger values increase throughput, but use more memory.
- `slices` - Enables parallel reads from the source index.
- `scroll` - Adjusts how long Elasticsearch keeps the scroll context alive.

### Field tracking options [field-tracking]
{applies_to}`serverless: preview` {applies_to}`stack: preview`

The {{es}} input plugin supports cursor-like pagination functionality, unlocking more advanced migration features, including the ability to resume migration tasks after a {{ls}} restart, and support for ongoing data migration over time. Tracking field options are:
- `tracking_field` - Plugin records the value of a field for the last document retrieved in a run.
- `tracking_field_seed` - Sets the starting value for `tracking_field` if no `last_run_metadata_path` is set. 

Check out the Elasticsearch input plugin documentation for more details and code samples: [Tracking a field's value across runs](logstash-docs-md://lsr/plugins-inputs-elasticsearch.md#plugins-inputs-elasticsearch-cursor).
