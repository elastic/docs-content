---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/data-streams.html
---

# Data streams [data-streams]

{{agent}} uses data streams to store time series data across multiple indices while giving you a single named resource for requests. Data streams are well-suited for logs, metrics, traces, and other continuously generated data. They offer a host of benefits over other indexing strategies:

* **Reduced number of fields per index**: Indices only need to store a specific subset of your data–meaning no more indices with hundreds of thousands of fields. This leads to better space efficiency and faster queries. As an added bonus, only relevant fields are shown in Discover.
* **More granular data control**: For example, file system, load, CPU, network, and process metrics are sent to different indices–each potentially with its own rollover, retention, and security permissions.
* **Flexible**: Use the custom namespace component to divide and organize data in a way that makes sense to your use case or company.
* **Fewer ingest permissions required**: Data ingestion only requires permissions to append data.


## Data stream naming scheme [data-streams-naming-scheme]

{{agent}} uses the Elastic data stream naming scheme to name data streams. The naming scheme splits data into different streams based on the following components:

`type`
:   A generic `type` describing the data, such as `logs`, `metrics`, `traces`, or `synthetics`.

`dataset`
:   The `dataset` is defined by the integration and describes the ingested data and its structure for each index. For example, you might have a dataset for process metrics with a field describing whether the process is running or not, and another dataset for disk I/O metrics with a field describing the number of bytes read.

`namespace`
:   A user-configurable arbitrary grouping, such as an environment (`dev`, `prod`, or `qa`), a team, or a strategic business unit. A `namespace` can be up to 100 bytes in length (multibyte characters will count toward this limit faster). Using a namespace makes it easier to search data from a given source by using a matching pattern. You can also use matching patterns to give users access to data when creating user roles.

    By default the namespace defined for an {{agent}} policy is propagated to all integrations in that policy. if you’d like to define a more granular namespace for a policy:

    1. In {{kib}}, go to **Integrations**.
    2. On the **Installed integrations** tab, select the integration that you’d like to update.
    3. Open the **Integration policies** tab.
    4. From the **Actions** menu next to the integration, select **Edit integration**.
    5. Open the advanced options and update the **Namespace** field. Data streams from the integration will now use the specified namespace rather than the default namespace inherited from the {{agent}} policy.


The naming scheme separates each components with a `-` character:

```text
<type>-<dataset>-<namespace>
```

For example, if you’ve set up the Nginx integration with a namespace of `prod`, {{agent}} uses the `logs` type, `nginx.access` dataset, and `prod` namespace to store data in the following data stream:

```text
logs-nginx.access-prod
```

Alternatively, if you use the APM integration with a namespace of `dev`, {{agent}} stores data in the following data stream:

```text
traces-apm-dev
```

All data streams, and the pre-built dashboards that they ship with, are viewable on the {{fleet}} Data Streams page:

:::{image} images/kibana-fleet-datastreams.png
:alt: Data streams page
:class: screenshot
:::

::::{tip}
If you’re familiar with the concept of indices, you can think of each data stream as a separate index in {{es}}. Under the hood though, things are a bit more complex. All of the juicy details are available in [{{es}} Data streams](/manage-data/data-store/data-streams.md).
::::



## {{data-sources-cap}} [data-streams-data-view]

When searching your data in {{kib}}, you can use a [{{data-source}}](/explore-analyze/find-and-organize/data-views.md) to search across all or some of your data streams.


## Index templates [data-streams-index-templates]

An index template is a way to tell {{es}} how to configure an index when it is created. For data streams, the index template configures the stream’s backing indices as they are created.

{{es}} provides the following built-in, ECS based templates: `logs-*-*`, `metrics-*-*`, and `synthetics-*-*`. {{agent}} integrations can also provide dataset-specific index templates, like `logs-nginx.access-*`. These templates are loaded when the integration is installed, and are used to configure the integration’s data streams.


### Edit the {{es}} index template [data-streams-index-templates-edit]

::::{warning}
Custom index mappings may conflict with the mappings defined by the integration and may break the integration in {{kib}}. Do not change or customize any default mappings.
::::


When you install an integration, {{fleet}} creates two default `@custom` component templates:

* A `@custom` component template allowing customization across all documents of a given data stream type, named following the pattern: `<data_stream_type>@custom`.
* A `@custom` component template for each data stream, named following the pattern: `<name_of_data_stream>@custom`.

The `@custom` component template specific to a datastream has higher precedence over the data stream type `@custom` component template.

You can edit a `@custom` component template to customize your {{es}} indices:

1. Open {{kib}} and navigate to to **{{stack-manage-app}}** > **Index Management** > **Data Streams**.
2. Find and click the name of the integration data stream, such as `logs-cisco_ise.log-default`.
3. Click the index template link for the data stream to see the list of associated component templates.
4. Navigate to **{{stack-manage-app}}** > **Index Management** > **Component Templates**.
5. Search for the name of the data stream’s custom component template and click the edit icon.
6. Add any custom index settings, metadata, or mappings. For example, you may want to:

    * Customize the index lifecycle policy applied to a data stream. See [Configure a custom index lifecycle policy](/solutions/observability/apps/index-lifecycle-management.md#apm-data-streams-custom-policy) in the APM Guide for a walk-through.

        Specify lifecycle name in the **index settings**:

        ```json
        {
          "index": {
            "lifecycle": {
               "name": "my_policy"
             }
          }
        }
        ```

    * Change the number of [replicas](/deploy-manage/distributed-architecture/reading-and-writing-documents.md) per index. Specify the number of replica shards in the **index settings**:

        ```json
        {
          "index": {
            "number_of_replicas": "2"
          }
        }
        ```


Changes to component templates are not applied retroactively to existing indices. For changes to take effect, you must create a new write index for the data stream. You can do this with the {{es}} [Rollover API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover).


## Index lifecycle management ({{ilm-init}}) [data-streams-ilm]

Use the [index lifecycle management](/manage-data/lifecycle/index-lifecycle-management.md) ({{ilm-init}}) feature in {{es}} to manage your {{agent}} data stream indices as they age. For example, create a new index after a certain period of time, or delete stale indices to enforce data retention standards.

Installed integrations may have one or many associated data streams—​each with an associated {{ilm-init}} policy. By default, these data streams use an {{ilm-init}} policy that matches their data type. For example, the data stream `metrics-system.logs-*`, uses the metrics {{ilm-init}} policy as defined in the `metrics-system.logs` index template.

Want to customize your index lifecycle management? See [Tutorials: Customize data retention policies](/reference/ingestion-tools/fleet/data-streams-ilm-tutorial.md).


## Ingest pipelines [data-streams-pipelines]

{{agent}} integration data streams ship with a default [ingest pipeline](/manage-data/ingest/transform-enrich/ingest-pipelines.md) that preprocesses and enriches data before indexing. The default pipeline should not be directly edited as changes can easily break the functionality of the integration.

Starting in version 8.4, all default ingest pipelines call a non-existent and non-versioned "`@custom`" ingest pipeline. If left uncreated, this pipeline has no effect on your data. However, if added to a data stream and customized, this pipeline can be used for custom data processing, adding fields, sanitizing data, and more.

Starting in version 8.12, ingest pipelines can be configured to process events at various levels of customization.

::::{note}
If you create a custom index pipeline, Elastic is not responsible for ensuring that it indexes and behaves as expected. Creating a custom pipeline involves custom processing of the incoming data, which should be done with caution and tested carefully.
::::


`global@custom`
:   Apply processing to all events

    For example, the following [pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline) request adds a new field `my-global-field` for all events:

    ```console
    PUT _ingest/pipeline/global@custom
    {
      "processors": [
        {
          "set": {
            "description": "Process all events",
            "field": "my-global-field",
            "value": "foo"
          }
        }
      ]
    }
    ```


`${type}`
:   Apply processing to all events of a given data type.

    For example, the following request adds a new field `my-logs-field` for all log events:

    ```console
    PUT _ingest/pipeline/logs@custom
    {
      "processors": [
        {
          "set": {
            "description": "Process all log events",
            "field": "my-logs-field",
            "value": "foo"
          }
        }
      ]
    }
    ```


`${type}-${package}.integration`
:   Apply processing to all events of a given type in an integration

    For example, the following request creates a `logs-nginx.integration@custom` pipeline that adds a new field `my-nginx-field` for all log events in the Nginx integration:

    ```console
    PUT _ingest/pipeline/logs-nginx.integration@custom
    {
      "processors": [
        {
          "set": {
            "description": "Process all nginx events",
            "field": "my-nginx-field",
            "value": "foo"
          }
        }
      ]
    }
    ```

    Note that `.integration` is included in the pipeline pattern to avoid possible collision with existing dataset pipelines.


`${type}-${dataset}`
:   Apply processing to a specific dataset.

    For example, the following request creates a `metrics-system.cpu@custom` pipeline that adds a new field `my-system.cpu-field` for all CPU metrics events in the System integration:

    ```console
    PUT _ingest/pipeline/metrics-system.cpu@custom
    {
      "processors": [
        {
          "set": {
            "description": "Process all events in the system.cpu dataset",
            "field": "my-system.cpu-field",
            "value": "foo"
          }
        }
      ]
    }
    ```


Custom pipelines can directly contain processors or you can use the pipeline processor to call other pipelines that can be shared across multiple data streams or integrations. These pipelines will persist across all version upgrades.

::::{warning}
:name: data-streams-pipelines-warning

If you have a custom pipeline defined that matches the naming scheme used for any {{fleet}} custom ingest pipelines, this can produce unintended results. For example, if you have a pipeline named like one of the following:

* `global@custom`
* `traces@custom`
* `traces-apm@custom`

The pipeline may be unexpectedly called for other data streams in other integrations. To avoid this problem, avoid the naming schemes defined above when naming your custom pipelines.

Refer to the breaking change in the 8.12.0 Release Notes for more detail and workaround options.

::::


See [Tutorial: Transform data with custom ingest pipelines](/reference/ingestion-tools/fleet/data-streams-pipeline-tutorial.md) to get started.
