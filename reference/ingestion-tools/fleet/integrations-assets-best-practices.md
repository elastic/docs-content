---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/integrations-assets-best-practices.html
---

# Best practices for integration assets [integrations-assets-best-practices]

When you use integrations with {{fleet}} and {{agent}} there are some restrictions to be aware of.

* [Using integration assets with standalone {{agent}}](#assets-restrictions-standalone)
* [Using integration assets without {{agent}}](#assets-restrictions-without-agent)
* [Using {{fleet}} and {{agent}} integration assets in custom integrations](#assets-restrictions-custom-integrations)
* [Copying {{fleet}} and {{agent}} integration assets](#assets-restrictions-copying)
* [Editing assets managed by {{fleet}}](#assets-restrictions-editing-assets)
* [Creating custom component templates](#assets-restrictions-custom-component-templates)
* [Creating a custom ingest pipeline](#assets-restrictions-custom-ingest-pipeline)
* [Cloning the index template of an integration package](#assets-restrictions-cloning-index-template)


## Using integration assets with standalone {{agent}} [assets-restrictions-standalone]

When you use standalone {{agent}} with integrations, the integration assets added to the {{agent}} policy must be installed on the destination {{es}} cluster.

* If {{kib}} is available, the integration assets can be [installed through {{fleet}}](/reference/ingestion-tools/fleet/install-uninstall-integration-assets.md).
* If {{kib}} is not available (for instance if you have a remote cluster without a {{kib}} instance), then the integration assets need to be installed manually.


## Using integration assets without {{agent}} [assets-restrictions-without-agent]

{{fleet}} integration assets are meant to work only with {{agent}}.

The {{fleet}} integration assets are not supposed to work when sending arbitrary logs or metrics collected with other products such as {{filebeat}}, {{metricbeat}} or {{ls}}.


## Using {{fleet}} and {{agent}} integration assets in custom integrations [assets-restrictions-custom-integrations]

While it’s possible to include {{fleet}} and {{agent}} integration assets in a custom integration, this is not recommended nor supported. Assets from another integration should not be referenced directly from a custom integration.

As an example scenario, one may want to ingest Redis logs from Kafka. This can be done using the [Redis integration](integration-docs://docs/reference/redis-intro.md), but only certain files and paths are allowed. It’s technically possible to use the [Custom Kafka Logs integration](integration-docs://docs/reference/kafka_log.md) with a custom ingest pipeline, referencing the ingest pipeline of the Redis integration to ingest logs into the index templates of the Custom Kafka Logs integration data streams.

However, referencing assets of an integration from another custom integration is not recommended nor supported. A configuration as described above can break when the integration is upgraded, as can happen automatically.


## Copying {{fleet}} and {{agent}} integration assets [assets-restrictions-copying]

As an alternative to referencing assets from another integration from within a custom integration, assets such as index templates and ingest pipelines can be copied so that they become standalone.

This way, because the assets are not managed by another integration, there is less risk of a configuration breaking or of an integration asset being deleted when the other integration is upgraded.

Note, however, that creating standalone integration assets based off of {{fleet}} and {{agent}} integrations is considered a custom configuration that is not tested nor supported. Whenever possible it’s recommended to use standard integrations.


## Editing assets managed by {{fleet}} [assets-restrictions-editing-assets]

{{fleet}}-managed integration assets should not be edited. Examples of these assets include an integration index template, the `@package` component templates, and ingest pipelines that are bundled with integrations. Any changes made to these assets will be overwritten when the integration is upgraded.


## Creating custom component templates [assets-restrictions-custom-component-templates]

While creating a `@custom` component template for a package integration is supported, it involves risks which can prevent data from being ingested correctly. This practice can lead to broken indexing, data loss, and breaking of integration package upgrades.

For example:

* If the `@package` component template of an integration is changed from a "normal" datastream to `TSDB` or `LogsDB`, some of the custom settings or mappings introduced may not be compatible with these indexing modes.
* If the type of an ECS field is overridden from, for example, `keyword` to `text`, aggregations based on that field may be prevented for built-in dashboards.

A similar caution against custom index mappings is noted in [Edit the {{es}} index template](/reference/ingestion-tools/fleet/data-streams.md#data-streams-index-templates-edit).


## Creating a custom ingest pipeline [assets-restrictions-custom-ingest-pipeline]

If you create a custom index pipeline (as documented in the [Transform data with custom ingest pipelines](/reference/ingestion-tools/fleet/data-streams-pipeline-tutorial.md) tutorial), Elastic is not responsible for ensuring that it indexes and behaves as expected. Creating a custom pipeline involves custom processing of the incoming data, which should be done with caution and tested carefully.

Refer to [Ingest pipelines](/reference/ingestion-tools/fleet/data-streams.md#data-streams-pipelines) to learn more.


## Cloning the index template of an integration package [assets-restrictions-cloning-index-template]

When you clone the index template of an integration package, this involves risk as any changes made to the original index template when it is upgraded will not be propagated to the cloned version. That is, the structure of the new index template is effectively frozen at the moment that it is cloned. Cloning an index template of an integration package can therefore lead to broken indexing, data loss, and breaking of integration package upgrades.

Additionally, cloning index templates to add or inject additional component templates cannot be tested by Elastic, so we cannot guarantee that the template will work in future releases.

If you want to change the ILM Policy, the number of shards, or other settings for the datastreams of one or more integrations, but the changes do not need to be specific to a given namespace, it’s highly  recommended to use the `package@custom` component templates, as described in [Scenario 1](/reference/ingestion-tools/fleet/data-streams-scenario1.md) and [Scenario 2](/reference/ingestion-tools/fleet/data-streams-scenario2.md) of the Customize data retention policies tutorial, so as to avoid the problems mentioned above.

If you want to change these settings for the data streams in one or more integrations and the changes **need to be namespace specific**, then you can do so following the steps in [Scenario 3](/reference/ingestion-tools/fleet/data-streams-scenario3.md) of the Customize data retention policies tutorial, but be aware of the restrictions mentioned above.
