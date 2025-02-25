---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-reduce-apm-storage.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-reduce-your-data-usage.html
---

# Reduce storage [apm-reduce-apm-storage]

The richness and volume of APM data provides unique insights into your applications, but it can also mean higher costs and more noise when analyzing data. There are a couple strategies you can use to reduce your data usage while continuing to get the full value of APM data.


## Reduce the sample rate [apm-reduce-sample-rate]

Distributed tracing can generate a substantial amount of data. More data can mean higher costs and more noise. Sampling aims to lower the amount of data ingested and the effort required to analyze that data.

See [Transaction sampling](../../../solutions/observability/apps/transaction-sampling.md) to learn more.


## Enable span compression [enable_span_compression]

In some cases, APM agents may collect large amounts of very similar or identical spans in a transaction. These repeated, similar spans often don’t provide added benefit, especially if they are of very short duration. Span compression takes these similar spans and compresses them into a single span-- retaining important information but reducing processing and storage overhead.

See [Span compression](/solutions/observability/apps/spans.md#apm-spans-span-compression) to learn more.


## Reduce collected stack trace information [observability-apm-reduce-stacktrace]

Elastic APM agents collect `stacktrace` information under certain circumstances. This can be very helpful in identifying issues in your code, but it also comes with an overhead at collection time and increases your storage usage.

Stack trace collection settings are managed in each APM agent. You can enable and disable this feature, or set specific configuration limits, like the maximum number of stacktrace frames to collect, or the minimum duration of a stacktrace to collect.

% Stateful only after this?

## Delete data [delete_data]
```{applies_to}
stack: all
```

You might want to only keep data for a defined time period. This might mean deleting old documents periodically, deleting data collected for specific services or customers, or deleting specific indices.

Depending on your use case, you can delete data:

* periodically with [{{ilm}}](../../../solutions/observability/apps/reduce-storage.md#apm-delete-data-with-ilm)
* [matching a query](../../../solutions/observability/apps/reduce-storage.md#apm-delete-data-query)
* with the [{{kib}} Index Management UI](../../../solutions/observability/apps/reduce-storage.md#apm-delete-data-in-kibana)

If you want to delete data for security or privacy reasons, see [Secure data](../../../solutions/observability/apps/application-data-security.md).


### Delete data with {{ilm}} ({{ilm-init}}) [apm-delete-data-with-ilm]

Index lifecycle management enables you to automate how you want to manage your indices over time. You can base actions on factors such as shard size and performance requirements. See [{{ilm-cap}}](../../../solutions/observability/apps/index-lifecycle-management.md) to learn more.


### Delete data matching a query [apm-delete-data-query]

You can delete all APM documents matching a specific query with the [Delete By Query API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete-by-query). For example, to delete all documents with a given `service.name`, use the following request:

```console
POST /.ds-*-apm*/_delete_by_query
{
  "query": {
    "term": {
      "service.name": {
        "value": "old-service-name"
      }
    }
  }
}
```


### Delete data with {{kib}} Index Management [apm-delete-data-in-kibana]

{{kib}}'s [Index Management](../../../manage-data/lifecycle/index-lifecycle-management/index-management-in-kibana.md) allows you to manage your cluster’s indices, data streams, index templates, and much more.

To open **Index Management**, find **Stack Management** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Select **Data Streams**. Select the data streams you want to delete, and click **Delete data streams**.


## Update existing data [apm-update-data]
```{applies_to}
stack: all
```

You might want to update documents that are already indexed. For example, if you your service name was set incorrectly.

To do this, you can use the [Update By Query API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update-by-query). To rename a service, send the following request:

```console
POST /.ds-*-apm*/_update_by_query?expand_wildcards=all
{
  "query": {
    "term": {
      "service.name": {
        "value": "current-service-name"
      }
    }
  },
  "script": {
    "source": "ctx._source.service.name = 'new-service-name'",
    "lang": "painless"
  }
}
```

::::{tip}
Remember to also change the service name in the [{{apm-agent}} configuration](https://www.elastic.co/guide/en/apm/agent/index.html).
::::