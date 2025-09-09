---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-data-security-delete.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Delete sensitive data [apm-data-security-delete]

If you accidentally ingest sensitive data, follow these steps to remove or redact the offending data:

1. Stop collecting the sensitive data. Use the **remedy** column of the [sensitive fields](/solutions/observability/apm/secure-data.md#apm-sensitive-fields) table to determine how to stop collecting the offending data.
2. Delete or redact the ingested data. With data collection fixed, you can now delete or redact the offending data:

    * [Redact specific fields](#apm-redact-field-data)
    * [Delete {{es}} documents](#apm-delete-doc-data)

## Redact specific fields [apm-redact-field-data]

To redact sensitive data in a specific field, use the [update by query API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update-by-query).

For example, the following query removes the `client.ip` address from APM documents in the `logs-apm.error-default` data stream:

```console
POST /logs-apm.error-default/_update_by_query
{
  "query": {
    "exists": {
      "field": "client.ip"
    }
  }
  "script": {
    "source": "ctx._source.client.ip = params.redacted",
    "params": {
      "redacted": "[redacted]"
    }
  }
}
```

Or, perhaps you only want to redact IP addresses from European users:

```console
POST /logs-apm.error-default/_update_by_query
{
  "query": {
    "term": {
      "client.geo.continent_name": {
        "value": "Europe"
      }
    }
  },
  "script": {
    "source": "ctx._source.client.ip = params.redacted",
    "params": {
      "redacted": "[redacted]"
    }
  }
}
```

See [update by query API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update-by-query) for more information and examples.

## Delete {{es}} documents [apm-delete-doc-data]

::::{warning}
This will permanently delete your data. You should test your queries with the [search API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) prior to deleting data.
::::

To delete an {{es}} document, you can use the [delete by query API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete-by-query).

For example, to delete all documents in the `apm-traces-*` data stream with a `user.email` value, run the following query:

```console
POST /apm-traces-*/_delete_by_query
{
  "query": {
    "exists": {
      "field": "user.email"
    }
  }
}
```

See [delete by query API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-delete-by-query) for more information and examples.

