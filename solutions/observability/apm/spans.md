---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-data-model-spans.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-compress-spans.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
  - id: cloud-serverless
---

# Spans [apm-data-model-spans]

:::{include} _snippets/apm-server-vs-mis.md
:::

% Stateful only until Span Compressions

**Spans** contain information about the execution of a specific code path. They measure from the start to the end of an activity, and they can have a parent/child relationship with other spans.

Agents automatically instrument a variety of libraries to capture these spans from within your application, but you can also use the Agent API for custom instrumentation of specific code paths.

Among other things, spans can contain:

* A `transaction.id` attribute that refers to its parent [transaction](/solutions/observability/apm/transactions.md).
* A `parent.id` attribute that refers to its parent span or transaction.
* Its start time and duration.
* A `name`, `type`, `subtype`, and `action`—see the [span name/type alignment](https://docs.google.com/spreadsheets/d/1SmWeX5AeqUcayrArUauS_CxGgsjwRgMYH4ZY8yQsMhQ/edit#gid=644582948) sheet for span name patterns and examples by {{apm-agent}}. In addition, some APM agents test against a public [span type/subtype spec](https://github.com/elastic/apm/blob/main/tests/agents/json-specs/span_types.json).
* An optional `stack trace`. Stack traces consist of stack frames, which represent a function call on the call stack. They include attributes like function name, file name and path, line number, etc.

::::{tip}
Most agents limit keyword fields, like `span.id`, to 1024 characters, and non-keyword fields, like `span.start.us`, to 10,000 characters.
::::

## Dropped spans [apm-data-model-dropped-spans]

For performance reasons, APM agents can choose to sample or omit spans purposefully. This can be useful in preventing edge cases, like long-running transactions with over 100 spans, that would otherwise overload both the Agent and the {{apm-server-or-mis}}. When this occurs, the Applications UI will display the number of spans dropped.

To configure the number of spans recorded per transaction, see the relevant Agent documentation:

* Android: *Not yet supported*
* Go: [`ELASTIC_APM_TRANSACTION_MAX_SPANS`](apm-agent-go://reference/configuration.md#config-transaction-max-spans)
* iOS: *Not yet supported*
* Java: [`transaction_max_spans`](apm-agent-java://reference/config-core.md#config-transaction-max-spans)
* .NET: [`TransactionMaxSpans`](apm-agent-dotnet://reference/config-core.md#config-transaction-max-spans)
* Node.js: [`transactionMaxSpans`](apm-agent-nodejs://reference/configuration.md#transaction-max-spans)
* PHP: [`transaction_max_spans`](apm-agent-php://reference/configuration-reference.md#config-transaction-max-spans)
* Python: [`transaction_max_spans`](apm-agent-python://reference/configuration.md#config-transaction-max-spans)
* Ruby: [`transaction_max_spans`](apm-agent-ruby://reference/configuration.md#config-transaction-max-spans)

## Missing spans [apm-data-model-missing-spans]

Agents stream spans to the {{apm-server-or-mis}} separately from their transactions. Because of this, unforeseen errors may cause spans to go missing. Agents know how many spans a transaction should have; if the number of expected spans does not equal the number of spans received by the {{apm-server-or-mis}}, the Applications UI will calculate the difference and display a message.

## Data streams [_data_streams]

Spans are stored with transactions in the following data streams:

* Application traces: `traces-apm-<namespace>`
* RUM and iOS agent application traces: `traces-apm.rum-<namespace>`

See [Data streams](/solutions/observability/apm/data-streams.md) to learn more.

## Example span document [_example_span_document]

This example shows what span documents can look like when indexed in {{es}}.

::::{dropdown} Expand {{es}} document
```json
[
    {
        "@timestamp": "2017-05-30T18:53:27.154Z",
        "agent": {
            "name": "elastic-node",
            "version": "3.14.0"
        },
        "ecs": {
            "version": "1.12.0"
        },
        "event": {
            "outcome": "unknown"
        },
        "http": {
            "request": {
                "method": "GET"
            },
            "response": {
                "status_code": 200
            }
        },
        "labels": {
            "span_tag": "something"
        },
        "observer": {
            "hostname": "ix.lan",
            "type": "apm-server",
            "version": "8.0.0"
        },
        "parent": {
            "id": "945254c567a5417e"
        },
        "processor": {
            "event": "span",
            "name": "transaction"
        },
        "service": {
            "environment": "staging",
            "name": "1234_service-12a3"
        },
        "span": {
            "action": "query",
            "db": {
                "instance": "customers",
                "statement": "SELECT * FROM product_types WHERE user_id=?",
                "type": "sql",
                "user": {
                    "name": "readonly_user"
                }
            },
            "duration": {
                "us": 3781
            },
            "http": {
                "method": "GET",
                "response": {
                    "status_code": 200
                }
            },
            "http.url.original": "http://localhost:8000",
            "id": "0aaaaaaaaaaaaaaa",
            "name": "SELECT FROM product_types",
            "stacktrace": [
                {
                    "abs_path": "net.js",
                    "context": {
                        "post": [
                            "    ins.currentTransaction = prev",
                            "    return result",
                            "}"
                        ],
                        "pre": [
                            "  var trans = this.currentTransaction",
                            ""
                        ]
                    },
                    "exclude_from_grouping": false,
                    "filename": "net.js",
                    "function": "onread",
                    "library_frame": true,
                    "line": {
                        "column": 4,
                        "context": "line3",
                        "number": 547
                    },
                    "module": "some module",
                    "vars": {
                        "key": "value"
                    }
                },
                {
                    "exclude_from_grouping": false,
                    "filename": "my2file.js",
                    "line": {
                        "number": 10
                    }
                }
            ],
            "start": {
                "us": 2830
            },
            "subtype": "postgresql",
            "sync": false,
            "type": "db"
        },
        "timestamp": {
            "us": 1496170407154000
        },
        "trace": {
            "id": "945254c567a5417eaaaaaaaaaaaaaaaa"
        },
        "transaction": {
            "id": "945254c567a5417e"
        },
        "url": {
            "original": "http://localhost:8000"
        }
    },
    {
        "@timestamp": "2017-05-30T18:53:42.281Z",
        "agent": {
            "name": "js-base",
            "version": "1.3"
        },
        "destination": {
            "address": "0:0::0:1",
            "ip": "0:0::0:1",
            "port": 5432
        },
        "ecs": {
            "version": "1.12.0"
        },
        "event": {
            "outcome": "unknown"
        },
        "observer": {
            "ephemeral_id": "2f13d8fa-83cd-4356-8123-aabfb47a1808",
            "hostname": "goat",
            "id": "17ad47dd-5671-4c89-979f-ef4533565ba2",
            "type": "apm-server",
            "version": "8.0.0"
        },
        "parent": {
            "id": "85925e55b43f4342"
        },
        "processor": {
            "event": "span",
            "name": "transaction"
        },
        "service": {
            "environment": "staging",
            "name": "serviceabc"
        },
        "span": {
            "action": "query.custom",
            "db": {
                "instance": "customers",
                "statement": "SELECT * FROM product_types WHERE user_id=?",
                "type": "sql",
                "user": {
                    "name": "readonly_user"
                }
            },
            "destination": {
                "service": {
                    "name": "postgresql",
                    "resource": "postgresql",
                    "type": "db"
                }
            },
            "duration": {
                "us": 3781
            },
            "id": "15aaaaaaaaaaaaaa",
            "name": "SELECT FROM product_types",
            "start": {
                "us": 2830
            },
            "subtype": "postgresql",
            "type": "db.postgresql.query"
        },
        "timestamp": {
            "us": 1496170422281000
        },
        "trace": {
            "id": "85925e55b43f4342aaaaaaaaaaaaaaaa"
        },
        "transaction": {
            "id": "85925e55b43f4342"
        }
    },
    {
        "@timestamp": "2017-05-30T18:53:27.154Z",
        "agent": {
            "name": "elastic-node",
            "version": "3.14.0"
        },
        "ecs": {
            "version": "1.12.0"
        },
        "event": {
            "outcome": "unknown"
        },
        "observer": {
            "ephemeral_id": "2f13d8fa-83cd-4356-8123-aabfb47a1808",
            "hostname": "goat",
            "id": "17ad47dd-5671-4c89-979f-ef4533565ba2",
            "type": "apm-server",
            "version": "8.0.0"
        },
        "parent": {
            "id": "945254c567a5417e"
        },
        "processor": {
            "event": "span",
            "name": "transaction"
        },
        "service": {
            "environment": "staging",
            "name": "1234_service-12a3"
        },
        "span": {
            "duration": {
                "us": 32592
            },
            "id": "1aaaaaaaaaaaaaaa",
            "name": "GET /api/types",
            "start": {
                "us": 0
            },
            "subtype": "external",
            "type": "request"
        },
        "timestamp": {
            "us": 1496170407154000
        },
        "trace": {
            "id": "945254c567a5417eaaaaaaaaaaaaaaaa"
        },
        "transaction": {
            "id": "945254c567a5417e"
        }
    },
    {
        "@timestamp": "2017-05-30T18:53:27.154Z",
        "agent": {
            "name": "elastic-node",
            "version": "3.14.0"
        },
        "ecs": {
            "version": "1.12.0"
        },
        "event": {
            "outcome": "unknown"
        },
        "observer": {
            "ephemeral_id": "2f13d8fa-83cd-4356-8123-aabfb47a1808",
            "hostname": "goat",
            "id": "17ad47dd-5671-4c89-979f-ef4533565ba2",
            "type": "apm-server",
            "version": "8.0.0"
        },
        "parent": {
            "id": "945254c567a5417e"
        },
        "processor": {
            "event": "span",
            "name": "transaction"
        },
        "service": {
            "environment": "staging",
            "name": "1234_service-12a3"
        },
        "span": {
            "action": "post",
            "duration": {
                "us": 3564
            },
            "id": "2aaaaaaaaaaaaaaa",
            "name": "GET /api/types",
            "start": {
                "us": 1845
            },
            "subtype": "http",
            "type": "request"
        },
        "timestamp": {
            "us": 1496170407154000
        },
        "trace": {
            "id": "945254c567a5417eaaaaaaaaaaaaaaaa"
        },
        "transaction": {
            "id": "945254c567a5417e"
        }
    },
    {
        "@timestamp": "2017-05-30T18:53:27.154Z",
        "agent": {
            "name": "elastic-node",
            "version": "3.14.0"
        },
        "child": {
            "id": [
                "4aaaaaaaaaaaaaaa"
            ]
        },
        "ecs": {
            "version": "1.12.0"
        },
        "event": {
            "outcome": "unknown"
        },
        "observer": {
            "ephemeral_id": "2f13d8fa-83cd-4356-8123-aabfb47a1808",
            "hostname": "goat",
            "id": "17ad47dd-5671-4c89-979f-ef4533565ba2",
            "type": "apm-server",
            "version": "8.0.0"
        },
        "parent": {
            "id": "945254c567a5417e"
        },
        "processor": {
            "event": "span",
            "name": "transaction"
        },
        "service": {
            "environment": "staging",
            "name": "1234_service-12a3"
        },
        "span": {
            "duration": {
                "us": 13980
            },
            "id": "3aaaaaaaaaaaaaaa",
            "name": "GET /api/types",
            "start": {
                "us": 0
            },
            "type": "request"
        },
        "timestamp": {
            "us": 1496170407154000
        },
        "trace": {
            "id": "945254c567a5417eaaaaaaaaaaaaaaaa"
        },
        "transaction": {
            "id": "945254c567a5417e"
        }
    }
]
```

::::

## Span compression [apm-spans-span-compression]

In some cases, APM agents may collect large amounts of very similar or identical spans in a transaction. For example, this can happen if spans are captured inside a loop or in unoptimized SQL queries that use multiple queries instead of joins to fetch related data.

In such cases, the upper limit of spans per transaction (by default, 500 spans) can be reached quickly, causing the agent to stop capturing potentially more relevant spans for a given transaction.

Capturing similar or identical spans often isn’t helpful, especially if they are of very short duration. They can also clutter the UI, and cause processing and storage overhead.

To address this problem, APM agents can compress similar spans into a single span. The compressed span retains most of the original span information, including the overall duration and number of spans it represents.

Regardless of the compression strategy, a span is eligible for compression if:

* It has not propagated its trace context.
* It is an *exit* span (such as database query spans).
* Its outcome is not `"failure"`.

### Compression strategies [apm-span-compression-strategy]

The {{apm-agent}} selects between two strategies to decide if adjacent spans can be compressed. In both strategies, only one previous span needs to be kept in memory. This ensures that the agent doesn’t require large amounts of memory to enable span compression.

#### Same-Kind strategy [apm-span-compression-same]

The agent uses the same-kind strategy if two adjacent spans have the same:

* span type
* span subtype
* `destination.service.resource` (e.g. database name)

#### Exact-Match strategy [apm-span-compression-exact]

The agent uses the exact-match strategy if two adjacent spans have the same:

* span name
* span type
* span subtype
* `destination.service.resource` (e.g. database name)

### Settings [apm-span-compression-settings]

You can specify the maximum span duration in the agent’s configuration settings. Spans with a duration longer than the specified value will not be compressed.

For the "Same-Kind" strategy, the default maximum span duration is 0 milliseconds, which means that the "Same-Kind" strategy is disabled by default. For the "Exact-Match" strategy, the default limit is 50 milliseconds.

### Agent support [apm-span-compression-support]

Support for span compression is available in the following agents and can be configured using the options listed below:

| Agent | Same-kind config | Exact-match config |
| --- | --- | --- |
| **Go agent** | [`ELASTIC_APM_SPAN_COMPRESSION_SAME_KIND_MAX_DURATION`](apm-agent-go://reference/configuration.md#config-span-compression-exact-match-duration) |
| **Java agent** | [`span_compression_same_kind_max_duration`](apm-agent-java://reference/config-huge-traces.md#config-span-compression-same-kind-max-duration) | [`span_compression_exact_match_max_duration`](apm-agent-java://reference/config-huge-traces.md#config-span-compression-exact-match-max-duration) |
| **.NET agent** | [`SpanCompressionSameKindMaxDuration`](apm-agent-dotnet://reference/config-core.md#config-span-compression-exact-match-max-duration) |
| **Node.js agent** | [`spanCompressionSameKindMaxDuration`](apm-agent-nodejs://reference/configuration.md#span-compression-exact-match-max-duration) |
| **Python agent** | [`span_compression_same_kind_max_duration`](apm-agent-python://reference/configuration.md#config-span-compression-exact-match-max_duration) |

## OpenTelemetry and Elastic APM spans

OpenTelemetry spans are mapped to Elastic APM transactions and spans as follows:

- Root spans, such as entry points, are mapped to APM transactions.
- Child spans, such as internal operations and DB queries, are mapped to APM spans.

The following table summarizes the mapping between OpenTelemetry span kinds and Elastic APM entities.

| OpenTelemetry span kind | Mapped to APM | Example |
|-------------------------|---------------|---------|
| `SERVER` | Transaction | Incoming HTTP request (`GET /users/{id}`) |
| `CONSUMER` | Transaction | Message queue consumer event |
| `CLIENT` | Span | Outgoing database query (`SELECT * FROM users`) |
| `PRODUCER` | Span | Sending a message to a queue |
| `INTERNAL` | Span | Internal function execution |

The following example shows OpenTelemetry spans:

```json
[
  {
    "traceId": "abcd1234",
    "spanId": "root5678",
    "parentId": null,
    "name": "GET /users/{id}",
    "kind": "SERVER"
  },
  {
    "traceId": "abcd1234",
    "spanId": "db1234",
    "parentId": "root5678",
    "name": "SELECT FROM users",
    "kind": "CLIENT"
  }
]
```

The previous OTel spans are stored by Elastic APM as follows:

```
Transaction: GET /users/{id}
 ├── Span: SELECT FROM users
```
