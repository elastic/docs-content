---
navigation_title: Migrate data using Logstash
applies_to:
  deployment:
    ech: ga
    ece: ga
    eck: ga
    self: ga
  serverless: ga
products:
  - id: elasticsearch
  - id: logstash
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
---

# Migrate {{es}} data using {{ls}} [migrate-with-ls]

[{{ls}}](logstash://reference/index.md) can copy documents between {{es}} deployments by reading them with the [{{es}} input plugin](logstash-docs-md://lsr/plugins-inputs-elasticsearch.md) and writing them with the [{{es}} output plugin](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md). This guide uses {{ech}} and {{serverless-full}} in both directions as examples. You can adapt the connection settings for {{ece}}, {{eck}}, and self-managed clusters.

This process copies ingested user data. It does not copy cluster settings, index mappings, index templates, ingest pipelines, or {{kib}} saved objects.

## Before you begin [migrate-prereqs]

- Make sure that the source and destination deployments are running and reachable from the host where you run {{ls}}.
- [Install {{ls}}](https://www.elastic.co/downloads/logstash).
- Create credentials that give the [{{es}} input plugin](logstash-docs-md://lsr/plugins-inputs-elasticsearch.md#plugins-inputs-elasticsearch-auth) read access to the source and the [{{es}} output plugin](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md#plugins-outputs-elasticsearch-auth) write access to the destination.
- Estimate the amount of data to migrate and make sure that the {{ls}} host, network, and destination have enough capacity.
- Prepare the destination before copying documents:
    - Create indices and mappings when you don't want to rely on dynamic mapping.
    - Add the required index templates and data stream definitions.
    - Configure the lifecycle policy that applies to the destination. {{serverless-full}} uses data stream lifecycle ({{dlm-init}}), not {{ilm}} ({{ilm-init}}).

Migrate {{kib}} saved objects, ingest pipelines, and feature configuration separately. To migrate saved objects, use the {{kib}} [import and export APIs]({{kib-apis}}group/endpoint-saved-objects) or [saved object management](/explore-analyze/find-and-organize/saved-objects.md#saved-objects-import-and-export).

## Choose connection settings [logstash-migration-connection-settings]

Both plugins support the same connection settings. Select settings based on the deployment that each plugin connects to:

| Deployment | Connection | Authentication |
| --- | --- | --- |
| {{serverless-full}} | Set `hosts` to the project's {{es}} endpoint over HTTPS and explicitly use port `443`. | Use `api_key`. User-based authentication settings are not supported. |
| {{ech}} | Use `cloud_id`, or use `hosts` with the {{es}} endpoint. Use `hosts` when connecting through a private endpoint. Don't set both options. | An API key is recommended. `cloud_auth` with a `username:password` value is also supported. |
| {{ece}} | Use the deployment's `cloud_id` or `hosts` with its {{es}} endpoint. Don't set both options. | Use an API key or user credentials. |
| {{eck}} or self-managed | Use `hosts` with an endpoint that the {{ls}} host can reach. | Use an API key or user credentials. Configure certificate authority settings when the endpoint does not use a publicly trusted certificate. |

API keys use the `id:api_key` format. When you create an [API key for {{ls}}](logstash://reference/connecting-to-serverless.md#api-key), select **{{ls}}** from the **API key** format dropdown.

API key authentication requires SSL/TLS. A `cloud_id` enables TLS automatically. With `hosts`, TLS is inferred when every URL uses `https`, or you can set `ssl_enabled => true`. The `cloud_auth` setting does not enable TLS by itself. For other TLS configurations, refer to the SSL settings for the [input plugin](logstash-docs-md://lsr/plugins-inputs-elasticsearch.md#plugins-inputs-elasticsearch-ssl_enabled) and [output plugin](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md#plugins-outputs-elasticsearch-ssl_enabled).

## Migrate your data [migrate-data-logstash]

### Step 1: Configure {{ls}} [configure-ls]

Create a {{ls}} [pipeline configuration file](logstash://reference/creating-logstash-pipeline.md) named `migration.conf`. Select the example that matches your migration direction.

::::{tab-set}
:::{tab-item} ECH to {{serverless-short}}

```ruby
input {
  elasticsearch {
    cloud_id       => "<ECH_CLOUD_ID>"
    api_key        => "<ECH_SOURCE_API_KEY>"
    index          => "index_pattern*"
    docinfo        => true
    docinfo_target => "[@metadata][input][elasticsearch]"
  }
}

output {
  elasticsearch {
    hosts       => [ "https://<SERVERLESS_ELASTICSEARCH_ENDPOINT>:443" ]
    api_key     => "<SERVERLESS_DESTINATION_API_KEY>"
    index       => "%{[@metadata][input][elasticsearch][_index]}"
    document_id => "%{[@metadata][input][elasticsearch][_id]}"
  }

  stdout { codec => rubydebug { metadata => true } }
}
```

:::
:::{tab-item} {{serverless-short}} to ECH

```ruby
input {
  elasticsearch {
    hosts          => [ "https://<SERVERLESS_ELASTICSEARCH_ENDPOINT>:443" ]
    api_key        => "<SERVERLESS_SOURCE_API_KEY>"
    index          => "index_pattern*"
    docinfo        => true
    docinfo_target => "[@metadata][input][elasticsearch]"
  }
}

output {
  elasticsearch {
    cloud_id    => "<ECH_CLOUD_ID>"
    api_key     => "<ECH_DESTINATION_API_KEY>"
    index       => "%{[@metadata][input][elasticsearch][_index]}"
    document_id => "%{[@metadata][input][elasticsearch][_id]}"
  }

  stdout { codec => rubydebug { metadata => true } }
}
```

:::
::::

The examples preserve the source index name and document ID. Replace `index_pattern*` with the index or index pattern to migrate. For example, `logs-*` selects all indices whose names start with `logs-`.

The examples target regular indices. To write to a data stream, create a matching data stream template on the destination and configure the [output plugin to use data streams](logstash-docs-md://lsr/plugins-outputs-elasticsearch.md#plugins-outputs-elasticsearch-data-streams).

When the destination is {{serverless-short}}, omit user-based authentication and all `ilm_*` output settings. For a data stream destination, configure {{dlm-init}} in the destination project.

### Step 2: Run {{ls}} [run-ls]

Run the pipeline:

```sh
bin/logstash -f migration.conf
```

For a static migration, stop writes to the source before the final run or plan a final synchronization before cutover.

### Step 3: Verify the migration [verify-migration]

1. Check the {{ls}} output for failed events.
2. In the destination deployment, find **{{index-manage-app}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. Confirm that the destination indices contain the expected documents.
4. Run representative searches and application queries against the destination before directing production traffic to it.

## Tune or resume a migration [additional-config]

The {{es}} input plugin provides options for larger or long-running migrations:

- `size` controls how many documents each page retrieves. Larger values can improve throughput but use more memory.
- `slices` enables parallel reads. Don't configure more slices than the number of primary shards.
- `search_api` controls whether the plugin uses `search_after` or scroll pagination. The default `auto` option uses `search_after` with supported {{es}} versions.

### Track progress across runs [field-tracking]

:::{warning}
Field tracking is a technical preview feature. Its configuration and behavior might change.
:::

Use `tracking_field` to record the last value that the input plugin retrieves. The plugin can inject that value into the next query, which supports resuming after a restart or periodically copying new documents. Use `tracking_field_seed` to set the initial value when no previous tracking metadata exists.

Tracking progress can result in duplicate documents after a failure. Preserve document IDs on the destination so that repeated events overwrite the same documents instead of creating copies.

For configuration details and examples, refer to [Tracking a field's value across runs](logstash-docs-md://lsr/plugins-inputs-elasticsearch.md#plugins-inputs-elasticsearch-cursor).
