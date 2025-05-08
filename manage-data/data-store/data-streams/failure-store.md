---
applies_to:
  stack: ga 8.19.0
  serverless: ga 9.1.0
---

# Failure store [failure-store]

Failure stores are a secondary set of indices inside a data stream dedicated to storing failed documents. Failed documents are any documents that cause ingest pipeline exceptions or have a structure that conflicts with a data stream's mappings. These failures normally cause the indexing operation to fail, returning the error message in the response. 

When a data stream's failure store is enabled, these failures are instead captured in a separate index and persisted to be analysed later. Clients receive a successful response with a flag indicating the failure was redirected. Failure stores do not capture failures caused by backpressure or document version conflicts. These failures are always returned as-is since they warrant specific action by the client.

## Set up a data stream failure store [set-up-failure-store]

Each data stream has its own failure store that can be enabled to accept failures. By default, this failure store is disabled and any ingestion problems are raised in the response to write operations.

### Set up for new data streams [set-up-failure-store-new]

You can specify on a data stream's template if it should enable the failure store when it is first created. The `data_stream_options` field in a [template](../templates.md) contains the settings required to enable a data stream's failure store.

:::{note}
Unlike the `settings` and `mappings` fields on an [index template](../templates.md) which are repeatedly applied to new data stream write indices on rollover, the `data_stream_options` section of a template is applied to a data stream only once when the data stream is first created. To configure existing data streams, use the put [data stream options API](./failure-store.md).
:::

To enable the failure store on a new data stream, enable it in the `data_stream_options` of the template:

```console
PUT _index_template/my-index-template
{
  "index_patterns": ["my-datastream-*"],
  "data_stream": { },
  "template": {
    "data_stream_options": { <1>
      "failure_store": {
        "enabled": true <2>
      }
    }
  }
}
```

1. The options for a data stream to be applied at creation time.
2. The failure store feature will be enabled for new data streams that match this template.


After a matching data stream is created, its failure store will be enabled.

### Set up for existing data streams [set-up-failure-store-existing]

Enabling the failure store via [index templates](../templates.md) can only affect data streams that are newly created. Existing data streams that use a template will not apply any changes to the template's `data_stream_options` after they have been created.

To modify an existing data stream's options, use the [put data stream options](./failure-store.md) API:

```console
PUT my-datastream-existing/_options
{
  "failure_store": {
    "enabled": true <1>
  }
}
```

1. The failure store option will now be enabled.


The failure store redirection can be disabled using this API as well. When the failure store is deactivated, only failed document redirection is halted. Any existing failure data in the data stream will remain until removed by manual deletion or by retention.

```console
PUT my-datastream-existing/_options
{
  "failure_store": {
    "enabled": false <1>
  }
}
```

1. Redirecting failed documents into the failure store will now be disabled.

### Enable failure store via cluster setting [set-up-failure-store-cluster-setting]

If you have a large number of existing data streams you may want an easier way to control if failures should be redirected. Instead of enabling the failure store using the [put data stream options](./failure-store.md) API, you can instead configure a set of patterns in the [cluster settings](./failure-store.md) which will enable the failure store feature by default.

Configure a list of patterns using the `data_streams.failure_store.enabled` dynamic cluster setting. If a data stream matches a pattern in this setting and does not have the failure store explicitly disabled in its options, then the failure store will default to being enabled for that matching data stream.

```console
PUT _cluster/settings
{
  "persistent" : {
    "data_streams.failure_store.enabled" : [ "my-datastream-*", "logs-*" ] <1>
  }
}
```

1. Indices that match `my-datastream-*` or `logs-*` will redirect failures to the failure store unless explicitly disabled.

## Using a failure store [use-failure-store]

The failure store is meant to ease the burden of detecting and handling failures when ingesting data to {{es}}. Clients are less likely to encounter unrecoverable failures when writing documents, and developers are more easily able to troubleshoot faulty pipelines and mappings.

### Failure redirection [use-failure-store-redirect]

Once a failure store is enabled for a data stream it will begin redirecting documents that fail due to common ingestion problems instead of returning errors in write operations. Clients are notified in a non-intrusive way when a document is redirected to the failure store.

Each data stream's failure store is made up of a list of indices that are dedicated to storing failed documents. These indices function much like a data stream's normal backing indices: There is a write index that accepts failed documents, they can be rolled over, and are automatically cleaned up over time subject to a lifecycle policy.

When a document bound for a data stream encounters a problem during its ingestion, the response is annotated with the `failure_store` field which describes how {{es}} responded to that problem. The `failure_store` field is present on both the [bulk](./failure-store.md) and [index](./failure-store.md) API responses when applicable. Clients can use this information to augment their behavior based on the response from {{es}}.

Here we have a bulk operation that sends two documents. Both are writing to the `id` field which is mapped as a `long` field type. The first document will be accepted, but the second document would cause a failure because the value `invalid_text` cannot be parsed as a `long`. This second document will be redirected to the failure store: 

```console
POST my-datastream/_bulk
{"create":{}}
{"@timestamp": "2025-05-01T00:00:00Z", "id": 1234} <1>
{"create":{}}
{"@timestamp": "2025-05-01T00:00:00Z", "id": "invalid_text"} <2>
```
1. A correctly formatted document.
2. Invalid document that cannot be parsed using the current mapping.

```console-result
{
  "errors": false, <1>
  "took": 400,
  "items": [
    {
      "create": {
        "_index": ".ds-my-datastream-2025.05.01-000001", <2>
        "_id": "YUvQipYB_ZAKuDfZRosB",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 1,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 3,
        "_primary_term": 1,
        "status": 201
      }
    },
    {
      "create": {
        "_index": ".fs-my-datastream-2025.05.01-000002", <3>
        "_id": "lEu8jZYB_ZAKuDfZNouU",
        "_version": 1,
        "result": "created",
        "_shards": {
          "total": 1,
          "successful": 1,
          "failed": 0
        },
        "_seq_no": 10,
        "_primary_term": 1,
        "failure_store": "used", <4>
        "status": 201
      }
    }
  ]
}
```

1. The response code is 200 OK, and the response body does not report any errors encountered.
2. The first document is accepted into the data stream's write index.
3. The second document encountered a problem during ingest and was redirected to the data stream's failure store.
4. The response is annotated with a field indicating that the failure store was used to persist the second document.


If the document was redirected to a data stream's failure store due to a problem, then the `failure_store` field on the response will be `used`, and the response will not return any error information:

```console-result
{
  "_index": ".fs-my-datastream-2025.05.01-000002", <1>
  "_id": "lEu8jZYB_ZAKuDfZNouU",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 11,
  "_primary_term": 1,
  "failure_store": "used" <2>
}
```

1. The document for this index operation was sent to the failure store's write index.
2. The response is annotated with a flag indicating the document was redirected.


If the document could have been redirected to a data stream's failure store but the failure store was disabled, then the `failure_store` field on the response will be `not_enabled`, and the response will display the error encountered as normal.

```console-result
{
  "error": {
    "root_cause": [ <1>
      {
        "type": "document_parsing_exception",
        "reason": "[1:53] failed to parse field [id] of type [long] in document with id 'Y0vQipYB_ZAKuDfZR4sR'. Preview of field's value: 'invalid_text'"
      }
    ],
    "type": "document_parsing_exception",
    "reason": "[1:53] failed to parse field [id] of type [long] in document with id 'Y0vQipYB_ZAKuDfZR4sR'. Preview of field's value: 'invalid_text'",
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "For input string: \"invalid_text\""
    },
    "failure_store": "not_enabled" <2>
  },
  "status": 400 <3>
}
```

1. The failure is returned to the client as normal when the failure store is not enabled.
2. The response is annotated with a flag indicating the failure store could have accepted the document, but it was not enabled.
3. Status of 400 Bad Request due to the mapping problem.


If the document was redirected to a data stream's failure store but that failed document could not be stored (e.g. due to shard unavailability or a similar problem), then the `failure_store` field on the response will be `failed`, and the response will display the error for the original failure, as well as a suppressed error detailing why the failure could not be stored:

```console-result
{
  "error": {
    "root_cause": [
      {
        "type": "document_parsing_exception", <1>
        "reason": "[1:53] failed to parse field [id] of type [long] in document with id 'Y0vQipYB_ZAKuDfZR4sR'. Preview of field's value: 'invalid_text'",
        "suppressed": [
          {
            "type": "cluster_block_exception", <2>
            "reason": "index [.fs-my-datastream-2025.05.01-000002] blocked by: [FORBIDDEN/5/index read-only (api)];"
          }
        ]
      }
    ],
    "type": "document_parsing_exception", <3>
    "reason": "[1:53] failed to parse field [id] of type [long] in document with id 'Y0vQipYB_ZAKuDfZR4sR'. Preview of field's value: 'invalid_text'",
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "For input string: \"invalid_text\""
    },
    "suppressed": [
      {
        "type": "cluster_block_exception",
        "reason": "index [.fs-my-datastream-2025.05.01-000002] blocked by: [FORBIDDEN/5/index read-only (api)];"
      }
    ],
    "failure_store": "failed" <4>
  },
  "status": 400 <5>
}
```

1. The root cause of the problem was a mapping mismatch.
2. The document could not be redirected because the failure store was not able to accept writes at this time due to an unforeseeable issue.
3. The complete exception tree is present on the response.
4. The response is annotated with a flag indicating the failure store would have accepted the document, but it was not able to.
5. Status of 400 Bad Request due to the original mapping problem.


### Searching failures [use-failure-store-searching]

Once you have accumulated some failures, they can be searched much like a regular index.

:::{warning}
Documents redirected to the failure store in the event of a failed ingest pipeline will be stored in their original, unprocessed form. If an ingest pipeline normally redacts sensitive information from a document, then failed documents in their original, unprocessed form may contain sensitive information.

Furthermore, failed documents are likely to be structured differently than normal data in a data stream, and thus are not supported by [document level security](./failure-store.md) or [field level security](./failure-store.md).

To limit visibility on potentially sensitive data, users require the [`read_failure_store`](./failure-store.md) index privilege for a data stream in order to search that data stream's failure store data.
:::

Searching a data stream's failure store can be done by making use of the existing search APIs available in {{es}}. 

To indicate that the search should be performed on failure store data, use the [index component selector syntax](./failure-store.md) to indicate which part of the data stream to target in the search operation. Appending the `::failures` suffix to the name of the data stream indicates that the operation should be performed against that data stream's failure store instead of its regular backing indices.

:::::{tab-set}

::::{tab-item} {{esql}}
```console
POST _query?format=txt
{
    "query": """FROM my-datastream::failures | DROP error.stack_trace | LIMIT 1""" <1>
}
```
1. We drop the `error.stack_trace` field here just to keep the example free of newlines.

An example of a search result with the failed document present:

```console-result
       @timestamp       |    document.id     |document.index |document.routing|                                                            error.message                                                            |error.pipeline |error.pipeline_trace|error.processor_tag|error.processor_type|        error.type        
------------------------+--------------------+---------------+----------------+-------------------------------------------------------------------------------------------------------------------------------------+---------------+--------------------+-------------------+--------------------+--------------------------
2025-05-01T12:00:00.000Z|Y0vQipYB_ZAKuDfZR4sR|my-datastream  |null            |[1:45] failed to parse field [id] of type [long] in document with id 'Y0vQipYB_ZAKuDfZR4sR'. Preview of field's value: 'invalid_text'|null           |null                |null               |null                |document_parsing_exception
```

:::{note}
Because the `document.source` field is unmapped, it is absent from the {{esql}} results. 
:::

::::

::::{tab-item} _search API
```console
GET my-datastream::failures/_search
```

An example of a search result with the failed document present:

```console-result
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": ".fs-my-datastream-2025.05.01-000002", <1>
        "_id": "lEu8jZYB_ZAKuDfZNouU",
        "_score": 1,
        "_source": {
          "@timestamp": "2025-05-01T12:00:00.000Z", <2>
          "document": { <3>
            "id": "Y0vQipYB_ZAKuDfZR4sR",
            "index": "my-datastream",
            "source": {
              "@timestamp": "2025-05-01T00:00:00Z",
              "id": "invalid_text"
            }
          },
          "error": { <4>
            "type": "document_parsing_exception",
            "message": "[1:53] failed to parse field [id] of type [long] in document with id 'Y0vQipYB_ZAKuDfZR4sR'. Preview of field's value: 'invalid_text'",
            "stack_trace": """o.e.i.m.DocumentParsingException: [1:53] failed to parse field [id] of type [long] in document with id 'Y0vQipYB_ZAKuDfZR4sR'. Preview of field's value: 'invalid_text'
	at o.e.i.m.FieldMapper.rethrowAsDocumentParsingException(FieldMapper.java:241)
	at o.e.i.m.FieldMapper.parse(FieldMapper.java:194)
	... 24 more
Caused by: j.l.IllegalArgumentException: For input string: "invalid_text"
	at o.e.x.s.AbstractXContentParser.toLong(AbstractXContentParser.java:189)
	at o.e.x.s.AbstractXContentParser.longValue(AbstractXContentParser.java:210)
	... 31 more
"""
          }
        }
      }
    ]
  }
}
```

1. The document belongs to a failure store index on the data stream.
2. The failure document timestamp is when the failure occurred in {{es}}.
3. The document that was sent is captured inside the failure document. Failure documents capture the id of the document at time of failure, along with which data stream the document was being written to, and the contents of the document. The `document.source` fields are unmapped to ensure failures are always captured.
4. The failure document captures information about the error encountered, like the type of error, the error message, and a compressed stack trace.
::::

::::{tab-item} SQL
```console
POST _sql?format=txt
{
    "query": """SELECT * FROM "my-datastream::failures" LIMIT 1"""
}
```

An example of a search result with the failed document present:

```console-result
       @timestamp       |    document.id     |document.index |document.routing|                                                            error.message                                                            |error.pipeline |error.pipeline_trace|error.processor_tag|error.processor_type|                                                                                                                                                                                                                                                                            error.stack_trace                                                                                                                                                                                                                                                                            |        error.type        
------------------------+--------------------+---------------+----------------+-------------------------------------------------------------------------------------------------------------------------------------+---------------+--------------------+-------------------+--------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------
2025-05-05T20:49:10.899Z|sXk1opYBL1dfU_1htCAE|my-datastream  |null            |[1:45] failed to parse field [id] of type [long] in document with id 'sXk1opYBL1dfU_1htCAE'. Preview of field's value: 'invalid_text'|null           |null                |null               |null                |o.e.i.m.DocumentParsingException: [1:45] failed to parse field [id] of type [long] in document with id 'sXk1opYBL1dfU_1htCAE'. Preview of field's value: 'invalid_text'
	at o.e.i.m.FieldMapper.rethrowAsDocumentParsingException(FieldMapper.java:241)
	at o.e.i.m.FieldMapper.parse(FieldMapper.java:194)
	... 19 more
Caused by: j.l.IllegalArgumentException: For input string: "invalid_text"
	at o.e.x.s.AbstractXContentParser.toLong(AbstractXContentParser.java:189)
	at o.e.x.s.AbstractXContentParser.longValue(AbstractXContentParser.java:210)
	... 26 more
|document_parsing_exception
```

:::{note}
Because the `document.source` field is unmapped, it is absent from the SQL results.
:::
::::
:::::

Failure documents have a uniform structure that is handled internally by {{es}}.

`@timestamp`
:   (`date`) The timestamp at which the document encountered a failure in {{es}}.

`document`
:   (`object`) The document at time of failure. If the document failed in an ingest pipeline, then the document will be the unprocessed version of the document as it arrived in the original indexing request. If the document failed due to a mapping issue, then the document will be as it was after any ingest pipelines were applied to it.
    
    `document.id`
    :   (`keyword`) The id of the original document at the time of failure.
    
    `document.routing`
    :   (`keyword`, optional) The routing of the original document at the time of failure if it was specified.
    
    `document.index`
    :   (`keyword`) The index that the document was being written to when it failed.

    `document.source`
    :   (unmapped object) The body of the original document. This field is unmapped and only present in the failure document's source. This prevents mapping conflicts in the failure store when redirecting failed documents. If you need to include fields from the original document's source in your queries, use [runtime fields](./failure-store.md) on the search request.

`error`
:   (`object`) Information about the failure that prevented this document from being indexed.

    `error.message`
    :   (`match_only_text`) The error message that describes the failure.

    `error.stack_trace`
    :   (`text`) A compressed stack trace from {{es}} for the failure.

    `error.type`
    :   (`keyword`) The type classification of failure. Values are the same type returned within failed indexing API responses.

    `error.pipeline`
    :   (`keyword`, optional) If the failure occurred in an ingest pipeline, this will contain the name of the pipeline.

    `error.pipeline_trace`
    :   (`keyword`, optional array) If the failure occurred in an ingest pipeline, this will contain the list of pipelines that the document had visited up until the failure.

    `error.processor_tag`
    :   (`keyword`, optional) If the failure occurred in an ingest processor that is annotated with a [tag](./failure-store.md), the tag contents will be present here.

    `error.processor_type`
    :   (`keyword`, optional) If the failure occurred in an ingest processor, this will contain the processor type. (e.g. `script`, `append`, `enrich`, etc.)
    

## Manage a data stream's failure store [manage-failure-store]

Failure data can accumulate in a data stream over time. To help manage this accumulation, most administrative operations that can be done on a data stream can be applied to the data stream's failure store.

### Failure store rollover [manage-failure-store-rollover]

A data stream treats its failure store much like a secondary set of [backing indices](./failure-store.md). Multiple dedicated hidden indices serve search requests for the failure store, while one index acts as the current write index. You can use the [rollover](./failure-store.md) API to rollover the failure store. Much like the regular indices in a data stream, a new write index will be created in the failure store to accept new failure documents.

```console
POST my-datastream::failures/_rollover
```

```console-result
{
  "acknowledged": true,
  "shards_acknowledged": true,
  "old_index": ".fs-my-datastream-2025.05.01-000002",
  "new_index": ".fs-my-datastream-2025.05.01-000003",
  "rolled_over": true,
  "dry_run": false,
  "lazy": false,
  "conditions": {}
}
```

### Failure store lifecycle [manage-failure-store-lifecycle]

Failure stores have their retention managed using an internal [data stream lifecycle](./failure-store.md). A thirty day (30d) retention is applied to failure store data. You can view the active lifecycle for a failure store index by calling the [get data stream API](./failure-store.md):

```console
GET _data_stream/my-datastream
```

```console-result
{
  "data_streams": [
    {
      "name": "my-datastream",
      "timestamp_field": {
        "name": "@timestamp"
      },
      "indices": [
        {
          "index_name": ".ds-my-datastream-2025.05.01-000001",
          "index_uuid": "jUbUNf-8Re-Nca8vJkHnkA",
          "managed_by": "Data stream lifecycle",
          "prefer_ilm": true,
          "index_mode": "standard"
        }
      ],
      "generation": 2,
      "status": "GREEN",
      "template": "my-datastream-template",
      "lifecycle": {
        "enabled": true
      },
      "next_generation_managed_by": "Data stream lifecycle",
      "prefer_ilm": true,
      "hidden": false,
      "system": false,
      "allow_custom_routing": false,
      "replicated": false,
      "rollover_on_write": false,
      "index_mode": "standard",
      "failure_store": { <1>
        "enabled": true,
        "rollover_on_write": false,
        "indices": [
          {
            "index_name": ".fs-my-datastream-2025.05.05-000002",
            "index_uuid": "oYS2WsjkSKmdazWuS4RP9Q",
            "managed_by": "Data stream lifecycle"  <2>
          }
        ],
        "lifecycle": {
          "enabled": true,
          "effective_retention": "30d",  <3> 
          "retention_determined_by": "default_failures_retention"  <4>
        }
      }
    }
  ]
}
```
1. Information about the failure store is presented in the response under its own field.
2. Indices are managed by data stream lifecycles by default.
3. An effective retention period of thirty days (30d) is present by default.
4. The retention is currently determined by the default.  

:::{note}
The default retention respects any maximum retention values. If [maximum retention](./failure-store.md) is configured lower than thirty days then the maximum retention will be used as the default value.
:::

You can update the default retention period for failure stores in your deployment by updating the `data_streams.lifecycle.retention.failures_default` cluster setting. New and existing data streams that have no retention configured on their failure stores will use this value to determine their retention period.

```console
PUT _cluster/settings
{
  "persistent": {
    "data_streams.lifecycle.retention.failures_default": "15d"
  }
}
```

You can also specify the failure store retention period for a data stream on its data stream options. These can be specified via the index template for new data streams, or via the [put data stream options](./failure-store.md) API for existing data streams.

```console
PUT _data_stream/my-datastream/_options
{
    "failure_store": {
        "enabled": true, <1>
        "lifecycle": {
            "data_retention": "10d" <2>
        }
    }
}
```
1. Ensure that the failure store remains enabled.
2. Set only this data stream's failure store retention to ten days.

### Add and remove from failure store [manage-failure-store-indices]

Failure stores support adding and removing indices from them using the [modify data stream](./failure-store.md) API.

```console
POST _data_stream/_modify
{
  "actions":[   
    {
      "remove_backing_index": { <1>
        "data_stream": "my-datastream", 
        "index": ".fs-my-datastream-2025.05.05-000002", <2>
        "failure_store": true <3>
      }
    },
    {
      "add_backing_index": { <4>
        "data_stream": "my-datastream",
        "index": "restored-failure-index", <5>
        "failure_store": true <6>
      }
    }
  ]
}
```
1. Action to remove a backing index.
2. The name of an auto-generated failure store index that should be removed.
3. Set `failure_store` to true to have the modify API target operate on the data stream's failure store.
4. Action to add a backing index.
5. The name of an index that should be added to the failure store.
6. Set `failure_store` to true to have the modify API target operate on the data stream's failure store.

This API gives you fine-grained control over the indices in your failure store, allowing you to manage backup and restoration operations as well as isolate failure data for later remediation.

## Failure store recipes and use cases [recipes]

TBD

### Troubleshooting ingest pipelines effectively [recipes-ingest-troubleshoot]

TBD

### Alerting on failed ingestion [recipes-alerting]

TBD

### Data remediation [recipes-remediation]

TBD

# WIP [wip]

Placeholder link