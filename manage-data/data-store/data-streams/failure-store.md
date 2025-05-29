---
applies_to:
  stack: ga 8.19.0
  serverless: ga 9.1.0
---

# Failure store [failure-store]

A failure store is a secondary set of indices inside a data stream, dedicated to storing failed documents. A failed document is any document that, without the failure store enabled, would cause an ingest pipeline exception or that has a structure that conflicts with a data stream's mappings. In the absence of the failure store, a failed document would cause the indexing operation to fail, with an error message returned in the operation response.

When a data stream's failure store is enabled, these failures are instead captured in a separate index and persisted to be analysed later. Clients receive a successful response with a flag indicating the failure was redirected. Failure stores do not capture failures caused by backpressure or document version conflicts. These failures are always returned as-is since they warrant specific action by the client.

## Set up a data stream failure store [set-up-failure-store]

Each data stream has its own failure store that can be enabled to accept failures. By default, this failure store is disabled and any ingestion problems are raised in the response to write operations.

### Set up for new data streams [set-up-failure-store-new]

You can specify in a data stream's [index template](../templates.md) if it should enable the failure store when it is first created.

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

Enabling the failure store via [index templates](../templates.md) can only affect data streams that are newly created. Existing data streams that use a template are not affected by changes to the template's `data_stream_options` field.

To modify an existing data stream's options, use the [put data stream options](./failure-store.md) API:

```console
PUT _data_stream/my-datastream-existing/_options
{
  "failure_store": {
    "enabled": true <1>
  }
}
```

1. The failure store option will now be enabled.


The failure store redirection can be disabled using this API as well. When the failure store is deactivated, only failed document redirection is halted. Any existing failure data in the data stream will remain until removed by manual deletion or by retention.

```console
PUT _data_stream/my-datastream-existing/_options
{
  "failure_store": {
    "enabled": false <1>
  }
}
```

1. Redirecting failed documents into the failure store will now be disabled.

### Enable failure store via cluster setting [set-up-failure-store-cluster-setting]

If you have a large number of existing data streams you may want to enable their failure stores in one place. Instead of updating each of their options individually, set `data_streams.failure_store.enabled` to a list of index patterns in the [cluster settings](./failure-store.md). Any data streams that match one of these patterns will operate with their failure store enabled.

```console
PUT _cluster/settings
{
  "persistent" : {
    "data_streams.failure_store.enabled" : [ "my-datastream-*", "logs-*" ] <1>
  }
}
```
1. Indices that match `my-datastream-*` or `logs-*` will redirect failures to the failure store unless explicitly disabled.

Matching data streams will ignore this configuration if the failure store is explicitly enabled or disabled in their [data stream options](./failure-store.md).

```console
PUT _cluster/settings
{
  "persistent" : {
    "data_streams.failure_store.enabled" : [ "my-datastream-*", "logs-*" ] <1>
  }
}
```
```console
PUT _data_stream/my-datastream-1/_options
{
  "failure_store": {
    "enabled": false <2>
  }
}
```
1. Enabling the failure stores for `my-datastream-*` and `logs-*`
2. The failure store for `my-datastream-1` is disabled even though it matches `my-datastream-*`. The data stream options override the cluster setting.

## Using a failure store [use-failure-store]

The failure store is meant to ease the burden of detecting and handling failures when ingesting data to {{es}}. Clients are less likely to encounter unrecoverable failures when writing documents, and developers are more easily able to troubleshoot faulty pipelines and mappings.

### Failure redirection [use-failure-store-redirect]

Once a failure store is enabled for a data stream it will begin redirecting documents that fail due to common ingestion problems instead of returning errors in write operations. Clients are notified in a non-intrusive way when a document is redirected to the failure store.

Each data stream's failure store is made up of a list of indices that are dedicated to storing failed documents. These failure indices function much like a data stream's normal backing indices: There is a write index that accepts failed documents, they can be rolled over, and are automatically cleaned up over time subject to a lifecycle policy. Failure indices are lazily created the first time they are needed to store a failed document.

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

### Failure document structure [use-failure-store-document]

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

#### Failure document source [use-failure-store-document-source]

The contents of a failure's `document` field is dependent on when the failure occurred in ingestion. When sending data to a data stream, documents can fail in two different phases: during an ingest pipeline and during indexing. 
1. Documents that fail during an ingest pipeline will store the source of the document as it was originally sent to {{es}}. Changes from pipelines are discarded before redirecting the failure.
2. Documents that fail during indexing will store the source of the document as it was during the index operation. Any changes from pipelines will be reflected in the source of the document that is redirected.

To help demonstrate the differences between these kinds of failures, we will use the following pipeline and template definition. 

```console
PUT _ingest/pipeline/my-datastream-example-pipeline
{
  "processors": [
    {
      "set": { <1>
        "override": false,
        "field": "@timestamp",
        "copy_from": "_ingest.timestamp"
      }
    },
    {
      "set": { <2>
        "field": "published",
        "copy_from": "data"
      }
    }
  ]
}
```
1. We use this processor to add a `@timestamp` to the document if one is missing.
2. A simple processor that copies the `data` field to the `published` field.

```console
PUT _index_template/my-datastream-example-template
{
    "index_patterns": ["my-datastream-ingest*"],
    "data_stream": {},
    "template": {
      "settings": {
        "index.default_pipeline": "my-datastream-example-pipeline" // Calling the pipeline by default.
      },
      "mappings": {
        "properties": {
          "published": { // A field of type long to hold our result.
            "type": "long"
          }
        }
      },
      "data_stream_options": {
        "failure_store": {
          "enabled": true // Failure store is enabled.
        }
      }
    }
}
```

During ingestion, documents are first processed by any applicable ingest pipelines. This process modifies a copy of the document and only saves the changes to the original document after all pipelines have completed. If a document is sent to the failure store because of a failure during an ingest pipeline, any changes to the document made by the pipelines it has been through will be discarded before redirecting the failure. This means that the document will be in the same state as when it was originally sent by the client. This has the benefit of being able to see the document before any pipelines have run on it, and allows for the original document to be used in simulate operations to further troubleshoot any problems in the ingest pipeline.

Using the pipeline and template defined above, we will send a document that is missing a required field for the pipeline. The document will fail:

```console
POST my-datastream-ingest/_doc
{
  "random": 42 // Not the field we're looking for.
}
```

```console-result
{
  "_index": ".fs-my-datastream-ingest-2025.05.09-000002",
  "_id": "eXS-tpYBwrYNjPmat9Cx",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 0,
  "_primary_term": 1,
  "failure_store": "used" // The document failed and went to the failure store.
}
```

Inspecting the corresponding failure document will show the document in its original form as it was sent to {{es}}. 

```console
GET my-datastream-ingest::failures/_search
```

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
        "_index": ".fs-my-datastream-ingest-2025.05.09-000002",
        "_id": "eXS-tpYBwrYNjPmat9Cx",
        "_score": 1,
        "_source": {
          "@timestamp": "2025-05-09T20:31:13.759Z",
          "document": { <1>
            "index": "my-datastream-ingest",
            "source": {
              "random": 42
            }
          },
          "error": {
            "type": "illegal_argument_exception",
            "message": "field [data] not present as part of path [data]", <2>
            "stack_trace": """j.l.IllegalArgumentException: field [data] not present as part of path [data]
	at o.e.i.IngestDocument.getFieldValue(IngestDocument.java:202)
	at o.e.i.c.SetProcessor.execute(SetProcessor.java:86)
	... 14 more
""",
            "pipeline_trace": [
              "my-datastream-example-pipeline"
            ],
            "pipeline": "my-datastream-example-pipeline",
            "processor_type": "set"
          }
        }
      }
    ]
  }
}
```
1. The `document` field shows the state of the document is from before any pipeline executions.
2. The pipeline failed after the timestamp would have been added.

We can see that the document failed on the second processor in the pipeline. The first processor would have added a `@timestamp` field. Since the pipeline failed, we find that it has no `@timestamp` field added because it did not save any changes from before the pipeline failed.

The second place failures can occur is during indexing. After the documents have been processed by any applicable pipelines, they are parsed using the index mappings before being indexed into the shard. If a document is sent to the failure store due to a failure in this process, then it will be stored as it was after any ingestion had occurred. This is because the original document is overwritten by the ingest pipeline changes by this point. This has the benefit of being able to see what the document looked like during the mapping and indexing phase of the write operation.

Building on the example above, we send a document that has a text value where we expect a numeric value:

```console
POST my-datastream-ingest/_doc
{
  "data": "this field is invalid" <1>
}
```
1. The mappings above expect this field to have been a numeric value.

```console-result
{
  "_index": ".fs-my-datastream-ingest-2025.05.09-000002",
  "_id": "sXTVtpYBwrYNjPmaFNAY",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 0,
  "_primary_term": 1,
  "failure_store": "used" <1>
}
```
1. The document failed and was sent to the failure store.

If we obtain the corresponding failure document, we can see that the document stored has had the default pipeline applied to it. 

```console
GET my-datastream-ingest::failures/_search
```

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
        "_index": ".fs-my-datastream-ingest-2025.05.09-000002",
        "_id": "sXTVtpYBwrYNjPmaFNAY",
        "_score": 1,
        "_source": {
          "@timestamp": "2025-05-09T20:55:38.943Z",
          "document": { <1>
            "id": "sHTVtpYBwrYNjPmaEdB5",
            "index": "my-datastream-ingest",
            "source": {
              "@timestamp": "2025-05-09T20:55:38.362486755Z",
              "data": "this field is invalid",
              "published": "this field is invalid"
            }
          },
          "error": {
            "type": "document_parsing_exception", <2>
            "message": "[1:91] failed to parse field [published] of type [long] in document with id 'sHTVtpYBwrYNjPmaEdB5'. Preview of field's value: 'this field is invalid'",
            "stack_trace": """o.e.i.m.DocumentParsingException: [1:91] failed to parse field [published] of type [long] in document with id 'sHTVtpYBwrYNjPmaEdB5'. Preview of field's value: 'this field is invalid'
	at o.e.i.m.FieldMapper.rethrowAsDocumentParsingException(FieldMapper.java:241)
	at o.e.i.m.FieldMapper.parse(FieldMapper.java:194)
	... 24 more
Caused by: j.l.IllegalArgumentException: For input string: "this field is invalid"
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
1. The `document` field reflects the document after the ingest pipeline has run.
2. The document failed to be indexed because of a mapping mismatch.

The `document` field attempts to show the effective input to whichever process led to the failure occurring. This gives you all the information you need to reproduce the problem.

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

When something goes wrong during ingestion it is often not an isolated event. Included for your convenience are some examples of how you can use the failure store to quickly respond to ingestion failures and get your indexing back on track.

### Troubleshooting nested ingest pipelines [recipes-nested-ingest-troubleshoot]

When a document fails in an ingest pipeline it can be difficult to figure out exactly what when wrong and where. When these failures are captured by the failure store during this part of the ingestion process, they will contain additional debugging information. Failed documents will note the type of processor and which pipeline was executing when the failure occurred. Failed documents will also contain a pipeline trace which keeps track of any nested pipeline calls that the document was in at time of failure. 

To demonstrate this, we will follow a failed document through an unfamiliar data stream and ingest pipeline:
```console
POST my-datastream-ingest/_doc
{
    "@timestamp": "2025-04-21T00:00:00Z",
    "important": {
      "info": "The rain in Spain falls mainly on the plain"
    }
}
```

```console-result
{
  "_index": ".fs-my-datastream-ingest-2025.05.09-000001",
  "_id": "F3S3s5YBwrYNjPmayMr9",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 2,
  "_primary_term": 1,
  "failure_store": "used" // The document was sent to the failure store
}
```

Now we search the failure store to check the failure document to see what went wrong.
```console
GET my-datastream-ingest::failures/_search
```

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
        "_index": ".fs-my-datastream-ingest-2025.05.09-000001",
        "_id": "F3S3s5YBwrYNjPmayMr9",
        "_score": 1,
        "_source": {
          "@timestamp": "2025-05-09T06:24:48.381Z",
          "document": {
            "index": "my-datastream-ingest",
            "source": { // When an ingest pipeline fails, the document stored is what was originally sent to the cluster.
              "important": {
                "info": "The rain in Spain falls mainly on the plain" // The important info that we failed to find was originally present on the document.
              },
              "@timestamp": "2025-04-21T00:00:00Z"
            }
          },
          "error": {
            "type": "illegal_argument_exception",
            "message": "field [info] not present as part of path [important.info]", // The info field was not present when the failure occurred.
            "stack_trace": """j.l.IllegalArgumentException: field [info] not present as part of path [important.info]
	at o.e.i.IngestDocument.getFieldValue(IngestDocument.java:202)
	at o.e.i.c.SetProcessor.execute(SetProcessor.java:86)
	... 19 more
""",
            "pipeline_trace": [ // The first pipeline called the second pipeline.
              "ingest-step-1",
              "ingest-step-2"
            ],
            "pipeline": "ingest-step-2", // The document failed in the second pipeline.
            "processor_type": "set" // It failed in the pipeline's set processor.
          }
        }
      }
    ]
  }
}
```

Despite not knowing the pipelines beforehand, we have some places to start looking. The `ingest-step-2` pipeline cannot find the `important.info` field despite it being present on the document that was sent to the cluster. If we pull that pipeline definition we find the following:

```console
GET _ingest/pipeline/ingest-step-2
```

```console-result
{
  "ingest-step-2": {
    "processors": [
      {
        "set": { // There is only one processor here.
          "field": "copy.info",
          "copy_from": "important.info" // This field was missing from the document at this point. 
        }
      }
    ]
  }
}
```

There is only a set processor in the `ingest-step-2` pipeline so this is likely not where the root problem is. Remembering the `pipeline_trace` field on the failure we find that `ingest-step-1` was the original pipeline called for this document. It is likely the data stream's default pipeline. Pulling its definition we find the following:

```console
GET _ingest/pipeline/ingest-step-1
```

```console-result
{
  "ingest-step-1": {
    "processors": [
      {
        "remove": {
          "field": "important.info" // A remove processor that is incorrectly getting rid of our important field.
        }
      },
      {
        "pipeline": {
          "name": "ingest-step-2" // The call to the second pipeline.
        }
      }
    ]
  }
}
```

We find a remove processor in the first pipeline that is the root cause of the problem! The pipeline should be updated to not remove important data, or the downstream pipeline should be changed to not expect the important data to be always present.

### Troubleshooting complicated ingest pipelines [recipes-complicated-ingest-troubleshoot]

Ingest processors can be labeled with [tags](./failure-store.md). These tags are user provided information that names or describes the processor's purpose in the pipeline. When documents are redirected to the failure store due to a processor issue, they capture the tag from the processor in which the failure occurred if it exists. Because of this, it is a good practice to tag the processors in your pipeline so that the location of a failure can be identified quickly.

Here we have a needlessly complicated pipeline. It is made up of several set and remove processors. Beneficially, they are all tagged with descriptive names.
```console
PUT _ingest/pipeline/complicated-processor
{
  "processors": [
    {
      "set": {
        "tag": "initialize counter",
        "field": "counter",
        "value": "1"
      }
    },
    {
      "set": {
        "tag": "copy counter to new",
        "field": "new_counter",
        "copy_from": "counter"
      }
    },
    {
      "remove": {
        "tag": "remove old counter",
        "field": "counter"
      }
    },
    {
      "set": {
        "tag": "transfer counter back",
        "field": "counter",
        "copy_from": "new_counter"
      }
    },
    {
      "remove": {
        "tag": "remove counter again",
        "field": "counter"
      }
    },
    {
      "set": {
        "tag": "copy to new counter again",
        "field": "new_counter",
        "copy_from": "counter"
      }
    }
  ]
}
```

We ingest some data and find that it was sent to the failure store
```console
POST my-datastream-ingest/_doc?pipeline=complicated-processor
{
    "@timestamp": "2025-04-21T00:00:00Z",
    "counter_name": "test"
}
```

```console-result
{
  "_index": ".fs-my-datastream-ingest-2025.05.09-000001",
  "_id": "HnTJs5YBwrYNjPmaFcri",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 1,
  "_primary_term": 1,
  "failure_store": "used"
}
```

Upon checking the failure, we can quickly identify the tagged processor that caused the problem
```console
GET my-datastream-ingest::failures/_search
```

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
        "_index": ".fs-my-datastream-ingest-2025.05.09-000001",
        "_id": "HnTJs5YBwrYNjPmaFcri",
        "_score": 1,
        "_source": {
          "@timestamp": "2025-05-09T06:41:24.775Z",
          "document": {
            "index": "my-datastream-ingest",
            "source": {
              "@timestamp": "2025-04-21T00:00:00Z",
              "counter_name": "test"
            }
          },
          "error": {
            "type": "illegal_argument_exception",
            "message": "field [counter] not present as part of path [counter]",
            "stack_trace": """j.l.IllegalArgumentException: field [counter] not present as part of path [counter]
	at o.e.i.IngestDocument.getFieldValue(IngestDocument.java:202)
	at o.e.i.c.SetProcessor.execute(SetProcessor.java:86)
	... 14 more
""",
            "pipeline_trace": [
              "complicated-processor"
            ],
            "pipeline": "complicated-processor",
            "processor_type": "set", // Helpful, but which set processor on the pipeline could it be?
            "processor_tag": "copy to new counter again" // The tag of the exact processor that it failed on.
          }
        }
      }
    ]
  }
}
```

Without tags in place it would not be as clear where in the pipeline we encountered the problem. Tags provide a unique identifier for a processor that can be quickly referenced in case of an ingest failure.

### Alerting on failed ingestion [recipes-alerting]

Since failure stores can be searched just like a normal data stream, we can use them as inputs to [alerting rules](./failure-store.md) in Kibana. Here is a simple alerting example to trigger on more than ten failures in the last five minutes for a data stream:

:::::{stepper}

::::{step} Create a failure store data view
If you want to use KQL or Lucene query types, you should first create a data view for your failure store data.
If you plan to use {{esql}} or the Query DSL query types, this step is not required.

Navigate to the data view page in Kibana and add a new data view. Set the index pattern to your failure store using the selector syntax.

:::{image} /manage-data/images/elasticsearch-reference-management_failure_store_alerting_create_data_view.png
:alt: create a data view using the failure store syntax in the index name
:::
::::

::::{step} Create new rule
Navigate to Management / Alerts and Insights / Rules. Create a new rule. Choose the Elasticsearch query option.

:::{image} /manage-data/images/elasticsearch-reference-management_failure_store_alerting_create_rule.png
:alt: create a new alerting rule and select the elasticsearch query option 
:::
::::

::::{step} Pick your query type
Choose which query type you wish to use

For KQL/Lucene queries, reference the data view that contains your failure store.

:::{image} /manage-data/images/elasticsearch-reference-management_failure_store_alerting_kql.png
:alt: use the data view created in the previous step as the input to the kql query
:::

For Query DSL queries, use the `::failures` suffix on your data stream name.

:::{image} /manage-data/images/elasticsearch-reference-management_failure_store_alerting_dsl.png
:alt: use the ::failures suffix in the data stream name in the query dsl
:::

For {{esql}} queries, use the `::failures` suffix on your data stream name in the `FROM` command.

:::{image} /manage-data/images/elasticsearch-reference-management_failure_store_alerting_esql.png
:alt: use the ::failures suffix in the data stream name in the from command
:::
::::

::::{step} Test
Configure schedule, actions, and details of the alert before saving the rule.

:::{image} /manage-data/images/elasticsearch-reference-management_failure_store_alerting_finish.png
:alt: complete the rule configuration and save it
:::
::::

::::{step} Done
::::

:::::

### Data remediation [recipes-remediation]

If you've encountered a long span of ingestion failures you may find that a sizeable gap of events has appeared in your data stream. If the failure store is enabled, the documents that should fill those gaps would be tucked away in the data stream's failure store. Because failure stores are made up of regular indices and the failure documents contain the document source that failed, the failure documents can often times be replayed into your production data streams. 

::::{warning} 
Care should be taken when replaying data into a data stream from a failure store. Any failures during the replay process may generate new failures in the failure store which can duplicate and obscure the original events.
::::

We recommend a few best practices for remediating failure data.

**Separate your failures beforehand.** As described in the [failure document source](#use-failure-store-document-source) section above, failure documents are structured differently depending on when the document failed during ingestion. We recommend to separate documents by ingest pipeline failures and indexing failures at minimum. Ingest pipeline failures often need to have the original pipeline re-executed, while index failures should skip any pipelines. Further separating failures by index or specific failure type may also be beneficial.

**Perform a failure store rollover.** Consider rolling over the failure store before attempting to remediate failures. This will create a new failure index that will collect any new failures during the remediation process. 

**Use an ingest pipeline to convert failure documents back into their original document.** Failure documents store failure information along with the document that failed ingestion. The first step for remediating documents should be to use an ingest pipeline to extract the original source from the failure document and discard any other info on it.

**Simulate first to avoid repeat failures.** If you must execute a pipeline as part of your remediation process, it is best to simulate the pipeline against the failure first. This will catch any unforeseen issues that may fail the document a second time. Remember, ingest pipeline failures will capture the document before an ingest pipeline was applied to it, which can further complicate remediation when a failure document becomes nested inside a new failure.

#### Remediating ingest node failures [recipes-remediation-ingest]

Failures that occurred during an ingest processor will be stored as they were before any pipelines were executed. To replay the document into the data stream we will need to rerun any applicable pipelines for the document.

:::::{stepper}

::::{step} Separate out which failures to replay

Start off by constructing a query that can be used to consistently identify which failures will be remediated.

```console
POST my-datastream-ingest-example::failures/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "exists": { <1>
            "field": "error.pipeline"
          }
        },
        {
          "match": { <2>
            "document.index": "my-datastream-ingest-example"
          }
        },
        {
          "match": { <3>
            "error.type": "illegal_argument_exception"
          }
        },
        {
          "range": { <4>
            "@timestamp": {
              "gt": "2025-05-01T00:00:00Z",
              "lte": "2025-05-02T00:00:00Z"
            }
          }
        }
      ]
    }
  }
}
```
1. Require the `error.pipeline` field to exist. This filters to ingest pipeline failures only.
2. Filter on the data stream name to remediate documents headed for a specific index.
3. Further narrow which kind of failure you are attempting to remediate. In this example we are targeting a specific type of error.
4. Filter on timestamp to only retrieve failures before a certain point in time. This provides a stable set of documents.

Take note of the documents that are returned. We can use these to simulate that our remediation logic makes sense
```console-result
{
  "took": 14,
  "timed_out": false,
  "_shards": {
    "total": 2,
    "successful": 2,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 2.575364,
    "hits": [
      {
        "_index": ".fs-my-datastream-ingest-example-2025.05.16-000001",
        "_id": "cOnR2ZYByIwDXH-g6GpR",
        "_score": 2.575364,
        "_source": {
          "@timestamp": "2025-05-01T15:58:53.522Z", <1>
          "document": {
            "index": "my-datastream-ingest-example",
            "source": {
              "@timestamp": "2025-05-01T00:00:00Z",
              "data": {
                "counter": 42 <2>
              }
            }
          },
          "error": {
            "type": "illegal_argument_exception",
            "message": "field [id] not present as part of path [data.id]", <3>
            "stack_trace": """j.l.IllegalArgumentException: field [id] not present as part of path [data.id]
	at o.e.i.IngestDocument.getFieldValue(IngestDocument.java:202)
	at o.e.i.c.SetProcessor.execute(SetProcessor.java:86)
	... 14 more
""",
            "pipeline_trace": [
              "my-datastream-default-pipeline"
            ],
            "pipeline": "my-datastream-default-pipeline", <4>
            "processor_type": "set"
          }
        }
      }
    ]
  }
}
```
1. This document is what we'll use for our simulations.
2. It had a counter value.
3. The document was missing a required field.
4. The document failed in the `my-data-stream-default-pipeline`
::::

::::{step} Fix the original problem
Because ingest pipeline failures need to be reprocessed by their original pipelines, any problems with those pipeline should be fixed before remediating failures. Investigating the pipeline mentioned in the example above shows that there is a processor that expects a field to be present that is not always present.

```console-result
{
  "my-datastream-default-pipeline": {
    "processors": [
      {
        "set": { <1>
          "field": "identifier",
          "copy_from": "data.id"
        }
      }
    ]
  }
}
```
1. The `data.id` field is expected to be present. If it isn't present this pipeline will fail.

Fixing a failure's root cause is a often a bespoke process. In this example, instead of discarding the data, we will make this identifier field optional.

```console
PUT _ingest/pipeline/my-datastream-default-pipeline
{
  "processors": [
    {
      "set": {
        "field": "identifier",
        "copy_from": "data.id",
        "if": "ctx.data?.id != null" <1>
      }
    }
  ]
}
```
1. Only conditionally run the processor if the field exists. 

::::

::::{step} Create a pipeline to convert failure documents

We must convert our failure documents back into their original forms and send them off to be reprocessed. We will create a pipeline to do this:

```console
PUT _ingest/pipeline/my-datastream-remediation-pipeline
{
  "processors": [
    {
      "script": {
      "lang": "painless",
      "source": """
          ctx._index = ctx.document.index; <1>
          ctx._routing = ctx.document.routing;
          def s = ctx.document.source; <2>
          ctx.remove("error"); <3>
          ctx.remove("document"); <4>
          for (e in s.entrySet()) { <5>
            ctx[e.key] = e.value;
          }"""
      }
    },
    {
      "reroute": { <6>
        "destination": "my-datastream-ingest-example"
      }
    }
  ]
}
```
1. Copy the original index name from the failure document over into the document's metadata. If you use custom document routing, copy that over too.
2. Capture the source of the original document.
3. Discard the `error` field since it wont be needed for the remediation.
4. Also discard the `document` field.
5. We extract all the fields from the original document's source back to the root of the document.
6. Since the pipeline that failed was the default pipeline on `my-datastream-ingest-example`, we will use the `reroute` processor to send any remediated documents to that data stream's default pipeline again to be reprocessed.

::::

::::{step} Test your pipelines
Before sending data off to be reindexed, be sure to test the pipelines in question with an example document to make sure they work. First, test to make sure the resulting document from the remediation pipeline is shaped how you expect. We can use the [simulate pipeline API](./failure-store.md) for this.

```console
POST _ingest/pipeline/_simulate
{
  "pipeline": { <1>
    "processors": [
      {
        "script": {
        "lang": "painless",
        "source": """
            ctx._index = ctx.document.index;
            ctx._routing = ctx.document.routing;
            def s = ctx.document.source;
            ctx.remove("error");
            ctx.remove("document");
            for (e in s.entrySet()) {
              ctx[e.key] = e.value;
            }"""
        }
      },
      {
        "reroute": {
          "destination": "my-datastream-ingest-example"
        }
      }
    ]
  },
  "docs": [ <2>
    {
        "_index": ".fs-my-datastream-ingest-example-2025.05.16-000001",
        "_id": "cOnR2ZYByIwDXH-g6GpR",
        "_source": {
          "@timestamp": "2025-05-01T15:58:53.522Z",
          "document": {
            "index": "my-datastream-ingest-example",
            "source": {
              "@timestamp": "2025-05-01T00:00:00Z",
              "data": {
                "counter": 42
              }
            }
          },
          "error": {
            "type": "illegal_argument_exception",
            "message": "field [id] not present as part of path [data.id]",
            "stack_trace": """j.l.IllegalArgumentException: field [id] not present as part of path [data.id]
	at o.e.i.IngestDocument.getFieldValue(IngestDocument.java:202)
	at o.e.i.c.SetProcessor.execute(SetProcessor.java:86)
	... 14 more
""",
            "pipeline_trace": [
              "my-datastream-default-pipeline"
            ],
            "pipeline": "my-datastream-default-pipeline",
            "processor_type": "set"
          }
        }
      }
  ]
}
```
1. The contents of the remediation pipeline written in the previous step.
2. The contents of an example failure document we identified in the previous steps.

```console-result
{
  "docs": [
    {
      "doc": {
        "_index": "my-datastream-ingest-example", <1>
        "_version": "-3",
        "_id": "cOnR2ZYByIwDXH-g6GpR", <2>
        "_source": { <3>
          "data": {
            "counter": 42
          },
          "@timestamp": "2025-05-01T00:00:00Z"
        },
        "_ingest": {
          "timestamp": "2025-05-01T20:58:03.566210529Z"
        }
      }
    }
  ]
}
```
1. The index has been updated via the reroute processor.
2. The id has stayed the same.
3. The source should cleanly match what the original document should have been.

Now that the remediation pipeline has been tested, be sure to test the end to end ingestion to verify that no further problems will arise. To do this, we will use the [simulate ingestion API](./failure-store.md) to test multiple pipeline executions.

```console
POST _ingest/_simulate?pipeline=my-datastream-remediation-pipeline <1>
{
  "pipeline_substitutions": {
    "my-datastream-remediation-pipeline": { <2>
      "processors": [
        {
          "script": {
            "lang": "painless",
            "source": """
                ctx._index = ctx.document.index;
                ctx._routing = ctx.document.routing;
                def s = ctx.document.source;
                ctx.remove("error");
                ctx.remove("document");
                for (e in s.entrySet()) {
                  ctx[e.key] = e.value;
                }"""
          }
        },
        {
          "reroute": {
            "destination": "my-datastream-ingest-example"
          }
        }
      ]
    }
  },
  "docs": [ <3>
    {
        "_index": ".fs-my-datastream-ingest-example-2025.05.16-000001",
        "_id": "cOnR2ZYByIwDXH-g6GpR",
        "_source": {
          "@timestamp": "2025-05-01T15:58:53.522Z",
          "document": {
            "index": "my-datastream-ingest-example",
            "source": {
              "@timestamp": "2025-05-01T00:00:00Z",
              "data": {
                "counter": 42
              }
            }
          },
          "error": {
            "type": "illegal_argument_exception",
            "message": "field [id] not present as part of path [data.id]",
            "stack_trace": """j.l.IllegalArgumentException: field [id] not present as part of path [data.id]
	at o.e.i.IngestDocument.getFieldValue(IngestDocument.java:202)
	at o.e.i.c.SetProcessor.execute(SetProcessor.java:86)
	... 14 more
""",
            "pipeline_trace": [
              "my-datastream-default-pipeline"
            ],
            "pipeline": "my-datastream-default-pipeline",
            "processor_type": "set"
          }
        }
      }
  ]
}
```
1. Set the pipeline to be the remediation pipeline name, otherwise, the default pipeline for the document's index is used.
2. The contents of the remediation pipeline in previous steps.
3. The contents of the previously identified example failure document. 

```console-result
{
  "docs": [
    {
      "doc": {
        "_id": "cOnR2ZYByIwDXH-g6GpR",
        "_index": "my-datastream-ingest-example", <1>
        "_version": -3,
        "_source": { <2>
          "@timestamp": "2025-05-01T00:00:00Z",
          "data": {
            "counter": 42
          }
        },
        "executed_pipelines": [ <3>
          "my-datastream-remediation-pipeline",
          "my-datastream-default-pipeline"
        ]
      }
    }
  ]
}
```
1. The index name has been updated.
2. The source is as expected after the default pipeline has run.
3. Ensure that both the new remediation pipeline and the original default pipeline have successfully run.

::::

::::{step} Reindex the failure documents
Combine the remediation pipeline with the failure store query together in a [reindex operation](./failure-store.md) to replay the failures.

```console
POST _reindex
{
  "source": {
    "index": "my-datastream-ingest-example::failures", <1>
    "query": {
      "bool": { <2>
        "must": [
          {
            "exists": {
              "field": "error.pipeline"
            }
          },
          {
            "match": {
              "document.index": "my-datastream-ingest-example"
            }
          },
          {
            "match": {
              "error.type": "illegal_argument_exception"
            }
          },
          {
            "range": {
              "@timestamp": {
                "gt": "2025-05-01T00:00:00Z",
                "lte": "2025-05-17T00:00:00Z"
              }
            }
          }
        ]
      }
    }
  },
  "dest": {
    "index": "my-datastream-ingest-example", <3>
    "op_type": "create",
    "pipeline": "my-datastream-remediation-pipeline" <4>
  }
}
```
1. Read from the failure store.
2. Only reindex failure documents that match the ones we are replaying.
3. Set the destination to the data stream the failures originally were sent to.
4. Replace the pipeline with the remediation pipeline.

```console-result
{
  "took": 469,
  "timed_out": false,
  "total": 1,
  "updated": 0,
  "created": 1, <1>
  "deleted": 0,
  "batches": 1,
  "version_conflicts": 0,
  "noops": 0,
  "retries": {
    "bulk": 0,
    "search": 0
  },
  "throttled_millis": 0,
  "requests_per_second": -1,
  "throttled_until_millis": 0,
  "failures": []
}
```
1. The failures have been remediated.

:::{tip}
Since the failure store is enabled on this data stream, it would be wise to check it for any further failures from the reindexing process. Failures that happen at this point in the process may end up as nested failures in the failure store. Remediating nested failures can quickly become a hassle as the original document gets nested multiple levels deep in the failure document. For this reason, it is suggested to remediate data during a quiet period where no other failures will arise. Furthermore, rolling over the failure store before executing the remediation would allow easier discarding of any new nested failures and only operate on the original failure documents.
:::

::::{step} Done
::::

:::::

#### Remediating mapping and shard failures [recipes-remediation-mapping]

As described in the [failure document source](#use-failure-store-document-source) section above, failures that occur due to a mapping or indexing issue will be stored as they were after any pipelines had executed. This means that to replay the document into the data stream we will need to make sure to skip any pipelines that have already run.

:::{tip}
You can greatly simplify this remediation process by writing any ingest pipelines to be idempotent. In that case, any document that has already be processed that passes through a pipeline again would be unchanged.
:::

:::::{stepper}

::::{step} Separate out which failures to replay

Start off by constructing a query that can be used to consistently identify which failures will be remediated.

```console
POST my-datastream-indexing-example::failures/_search
{
  "query": {
    "bool": {
      "must_not": [
        {
          "exists": { <1>
            "field": "error.pipeline"
          }
        }
      ],
      "must": [
        {
          "match": { <2>
            "document.index": "my-datastream-indexing-example"
          }
        },
        {
          "match": { <3>
            "error.type": "document_parsing_exception"
          }
        },
        {
          "range": { <4>
            "@timestamp": {
              "gt": "2025-05-01T00:00:00Z",
              "lte": "2025-05-02T00:00:00Z"
            }
          }
        }
      ]
    }
  }
}
```
1. Require the `error.pipeline` field to not exist. This filters out any ingest pipeline failures, and only returns indexing failures.
2. Filter on the data stream name to remediate documents headed for a specific index.
3. Further narrow which kind of failure you are attempting to remediate. In this example we are targeting a specific type of error.
4. Filter on timestamp to only retrieve failures before a certain point in time. This provides a stable set of documents.

Take note of the documents that are returned. We can use these to simulate that our remediation logic makes sense
```console-result
{
  "took": 1,
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
    "max_score": 1.5753641,
    "hits": [
      {
        "_index": ".fs-my-datastream-indexing-example-2025.05.16-000002",
        "_id": "_lA-GJcBHLe506UUGL0I",
        "_score": 1.5753641,
        "_source": { <1>
          "@timestamp": "2025-05-02T18:53:31.153Z",
          "document": {
            "id": "_VA-GJcBHLe506UUFL2i",
            "index": "my-datastream-indexing-example",
            "source": {
              "processed": true, <2>
              "data": {
                "counter": 37
              }
            }
          },
          "error": {
            "type": "document_parsing_exception", <3>
            "message": "[1:40] failed to parse: data stream timestamp field [@timestamp] is missing",
            "stack_trace": """o.e.i.m.DocumentParsingException: [1:40] failed to parse: data stream timestamp field [@timestamp] is missing
	at o.e.i.m.DocumentParser.wrapInDocumentParsingException(DocumentParser.java:265)
	at o.e.i.m.DocumentParser.internalParseDocument(DocumentParser.java:162)
	... 19 more
Caused by: j.l.IllegalArgumentException: data stream timestamp field [@timestamp] is missing
	at o.e.i.m.DataStreamTimestampFieldMapper.extractTimestampValue(DataStreamTimestampFieldMapper.java:210)
	at o.e.i.m.DataStreamTimestampFieldMapper.postParse(DataStreamTimestampFieldMapper.java:223)
	... 20 more
"""
          }
        }
      }
    ]
  }
}
```
1. This document is what we'll use for our simulations.
2. The document was missing a required `@timestamp` field.
3. The document failed with a `document_parsing_exception` because of the missing timestamp.

::::

::::{step} Fix the original problem

There are a broad set of possible indexing failures. Most of these problems stem from incorrect values for a particular mapping. Sometimes a large number of new fields are dynamically mapped and the maximum number of mapping fields is reached and no more can be added. In our example above, the document being indexed is missing a required timestamp.

These problems can occur in a number of places: Data sent from a client may be incomplete, ingest pipelines may not be producing the correct result, or the index mapping may need to be updated to account for changes in data.

Once all clients and pipelines are producing complete and correct documents, and your mappings are correctly configured for your incoming data, proceed with the remediation. 

::::

::::{step} Create a pipeline to convert failure documents

We must convert our failure documents back into their original forms and send them off to be reprocessed. We will create a pipeline to do this. Since the example failure was due to not having a timestamp on the document, we will simply use the timestamp at the time of failure for the document since the original timestamp is missing. This solution assumes that the documents we are remediating were created very closely to when the failure occurred. Your remediation process may need adjustments if this is not applicable for you.

```console
PUT _ingest/pipeline/my-datastream-remediation-pipeline
{
  "processors": [
    {
      "script": {
      "lang": "painless",
      "source": """
          ctx._index = ctx.document.index; <1>
          ctx._routing = ctx.document.routing;
          def s = ctx.document.source; <2>
          ctx.remove("error"); <3>
          ctx.remove("document"); <4>
          for (e in s.entrySet()) { <5>
            ctx[e.key] = e.value;
          }"""
      }
    }
  ]
}
```
1. Copy the original index name from the failure document over into the document's metadata. If you use custom document routing, copy that over too.
2. Capture the source of the original document.
3. Discard the `error` field since it wont be needed for the remediation.
4. Also discard the `document` field.
5. We extract all the fields from the original document's source back to the root of the document. The `@timestamp` field is not overwritten and thus will be present in the final document.

:::{important}
Remember that a document that has failed during indexing has already been processed by the ingest processor! It shouldn't need to be processed again unless you made changes to your pipeline to fix the original problem. Make sure that any fixes applied to the ingest pipeline is reflected in the pipeline logic here.
:::

::::

::::{step} Test your pipeline
Before sending data off to be reindexed, be sure to test the remedial pipeline with an example document to make sure it works. Most importantly, make sure the resulting document from the remediation pipeline is shaped how you expect. We can use the [simulate pipeline API](./failure-store.md) for this.

```console
POST _ingest/pipeline/_simulate
{
  "pipeline": { <1>
    "processors": [
      {
        "script": {
        "lang": "painless",
        "source": """
            ctx._index = ctx.document.index;
            ctx._routing = ctx.document.routing;
            def s = ctx.document.source;
            ctx.remove("error");
            ctx.remove("document");
            for (e in s.entrySet()) {
              ctx[e.key] = e.value;
            }"""
        }
      }
    ]
  },
  "docs": [ <2>
    {
        "_index": ".fs-my-datastream-indexing-example-2025.05.16-000002",
        "_id": "_lA-GJcBHLe506UUGL0I",
        "_score": 1.5753641,
        "_source": {
          "@timestamp": "2025-05-02T18:53:31.153Z",
          "document": {
            "id": "_VA-GJcBHLe506UUFL2i",
            "index": "my-datastream-indexing-example",
            "source": {
              "processed": true,
              "data": {
                "counter": 37
              }
            }
          },
          "error": {
            "type": "document_parsing_exception",
            "message": "[1:40] failed to parse: data stream timestamp field [@timestamp] is missing",
            "stack_trace": """o.e.i.m.DocumentParsingException: [1:40] failed to parse: data stream timestamp field [@timestamp] is missing
	at o.e.i.m.DocumentParser.wrapInDocumentParsingException(DocumentParser.java:265)
	at o.e.i.m.DocumentParser.internalParseDocument(DocumentParser.java:162)
	... 19 more
Caused by: j.l.IllegalArgumentException: data stream timestamp field [@timestamp] is missing
	at o.e.i.m.DataStreamTimestampFieldMapper.extractTimestampValue(DataStreamTimestampFieldMapper.java:210)
	at o.e.i.m.DataStreamTimestampFieldMapper.postParse(DataStreamTimestampFieldMapper.java:223)
	... 20 more
"""
          }
        }
      }
  ]
}
```
1. The contents of the remediation pipeline written in the previous step.
2. The contents of an example failure document we identified in the previous steps.

```console-result
{
  "docs": [
    {
      "doc": {
        "_index": "my-datastream-indexing-example", <1>
        "_version": "-3",
        "_id": "_lA-GJcBHLe506UUGL0I",
        "_source": { <2>
          "processed": true,
          "@timestamp": "2025-05-28T18:53:31.153Z", <3>
          "data": {
            "counter": 37
          }
        },
        "_ingest": {
          "timestamp": "2025-05-28T19:14:50.457560845Z"
        }
      }
    }
  ]
}
```
1. The index has been updated via the script processor.
2. The source should reflect any fixes and match the expected document shape for the final index.
3. In this example case, we find that the failure timestamp has stayed in the source.

::::

::::{step} Reindex the failure documents
Combine the remediation pipeline with the failure store query together in a [reindex operation](./failure-store.md) to replay the failures.

```console
POST _reindex
{
  "source": {
    "index": "my-datastream-indexing-example::failures", <1>
    "query": {
      "bool": { <2>
        "must_not": [
          {
            "exists": {
              "field": "error.pipeline"
            }
          }
        ],
        "must": [
          {
            "match": {
              "document.index": "my-datastream-indexing-example"
            }
          },
          {
            "match": {
              "error.type": "document_parsing_exception"
            }
          },
          {
            "range": {
              "@timestamp": {
                "gt": "2025-05-01T00:00:00Z",
                "lte": "2025-05-28T19:00:00Z"
              }
            }
          }
        ]
      }
    }
  },
  "dest": {
    "index": "my-datastream-indexing-example", <3>
    "op_type": "create",
    "pipeline": "my-datastream-remediation-pipeline" <4>
  }
}
```
1. Read from the failure store.
2. Only reindex failure documents that match the ones we are replaying.
3. Set the destination to the data stream the failures originally were sent to. The remediation pipeline above updates the index to be the correct one, but a destination is still required.
4. Replace the pipeline with the remediation pipeline. This will keep any default pipelines from running.

```console-result
{
  "took": 469,
  "timed_out": false,
  "total": 1,
  "updated": 0,
  "created": 1, <1>
  "deleted": 0,
  "batches": 1,
  "version_conflicts": 0,
  "noops": 0,
  "retries": {
    "bulk": 0,
    "search": 0
  },
  "throttled_millis": 0,
  "requests_per_second": -1,
  "throttled_until_millis": 0,
  "failures": []
}
```
1. The failures have been remediated.

:::{tip}
Since the failure store is enabled on this data stream, it would be wise to check it for any further failures from the reindexing process. Failures that happen at this point in the process may end up as nested failures in the failure store. Remediating nested failures can quickly become a hassle as the original document gets nested multiple levels deep in the failure document. For this reason, it is suggested to remediate data during a quiet period where no other failures will arise. Furthermore, rolling over the failure store before executing the remediation would allow easier discarding of any new nested failures and only operate on the original failure documents.
:::

::::{step} Done
::::

:::::

Once any failures have been remediated, you may wish to purge the failures from the failure store to clear up space and to avoid warnings about failed data that has already been replayed. Otherwise, your failures will stay available until the maximum failure store retention should you need to reference them.