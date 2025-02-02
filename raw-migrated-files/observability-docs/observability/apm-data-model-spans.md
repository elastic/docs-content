# Spans [apm-data-model-spans]

**Spans** contain information about the execution of a specific code path. They measure from the start to the end of an activity, and they can have a parent/child relationship with other spans.

Agents automatically instrument a variety of libraries to capture these spans from within your application, but you can also use the Agent API for custom instrumentation of specific code paths.

Among other things, spans can contain:

* A `transaction.id` attribute that refers to its parent [transaction](../../../solutions/observability/apps/transactions.md).
* A `parent.id` attribute that refers to its parent span or transaction.
* Its start time and duration.
* A `name`, `type`, `subtype`, and `action`—see the [span name/type alignment](https://docs.google.com/spreadsheets/d/1SmWeX5AeqUcayrArUauS_CxGgsjwRgMYH4ZY8yQsMhQ/edit#gid=644582948) sheet for span name patterns and examples by {{apm-agent}}. In addition, some APM agents test against a public [span type/subtype spec](https://github.com/elastic/apm/blob/main/tests/agents/json-specs/span_types.json).
* An optional `stack trace`. Stack traces consist of stack frames, which represent a function call on the call stack. They include attributes like function name, file name and path, line number, etc.

::::{tip}
Most agents limit keyword fields, like `span.id`, to 1024 characters, and non-keyword fields, like `span.start.us`, to 10,000 characters.
::::



## Dropped spans [apm-data-model-dropped-spans]

For performance reasons, APM agents can choose to sample or omit spans purposefully. This can be useful in preventing edge cases, like long-running transactions with over 100 spans, that would otherwise overload both the Agent and the APM Server. When this occurs, the Applications UI will display the number of spans dropped.

To configure the number of spans recorded per transaction, see the relevant Agent documentation:

* Android: *Not yet supported*
* Go: [`ELASTIC_APM_TRANSACTION_MAX_SPANS`](https://www.elastic.co/guide/en/apm/agent/go/{{apm-go-branch}}/configuration.html#config-transaction-max-spans)
* iOS: *Not yet supported*
* Java: [`transaction_max_spans`](https://www.elastic.co/guide/en/apm/agent/java/{{apm-java-branch}}/config-core.html#config-transaction-max-spans)
* .NET: [`TransactionMaxSpans`](https://www.elastic.co/guide/en/apm/agent/dotnet/{{apm-dotnet-branch}}/config-core.html#config-transaction-max-spans)
* Node.js: [`transactionMaxSpans`](https://www.elastic.co/guide/en/apm/agent/nodejs/{{apm-node-branch}}/configuration.html#transaction-max-spans)
* PHP: [`transaction_max_spans`](https://www.elastic.co/guide/en/apm/agent/php/{{apm-php-branch}}/configuration-reference.html#config-transaction-max-spans)
* Python: [`transaction_max_spans`](https://www.elastic.co/guide/en/apm/agent/python/{{apm-py-branch}}/configuration.html#config-transaction-max-spans)
* Ruby: [`transaction_max_spans`](https://www.elastic.co/guide/en/apm/agent/ruby/{{apm-ruby-branch}}/configuration.html#config-transaction-max-spans)


## Missing spans [apm-data-model-missing-spans]

Agents stream spans to the APM Server separately from their transactions. Because of this, unforeseen errors may cause spans to go missing. Agents know how many spans a transaction should have; if the number of expected spans does not equal the number of spans received by the APM Server, the Applications UI will calculate the difference and display a message.


## Data streams [_data_streams]

Spans are stored with transactions in the following data streams:

* Application traces: `traces-apm-<namespace>`
* RUM and iOS agent application traces: `traces-apm.rum-<namespace>`

See [Data streams](../../../solutions/observability/apps/data-streams.md) to learn more.


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

In some cases, APM agents may collect large amounts of very similar or identical spans in a transaction. For example, this can happen if spans are captured inside of a loop, or in unoptimized SQL queries that use multiple queries instead of joins to fetch related data. In such cases, the upper limit of spans per transaction (by default, 500 spans) can be reached quickly, causing the agent to stop capturing potentially more relevant spans for a given transaction.

Such repeated similar spans often aren’t very relevant for themselves, especially if they are of very short duration. They also can clutter the UI, and cause processing and storage overhead.

To address this problem, the APM agents can compress such spans into a single span. The compressed span retains most of the original span information, such as overall duration and the number of spans it represents.

Regardless of the compression strategy, a span is eligible for compression if:

* It has not propagated its trace context.
* Is an *exit* span (such as database query spans).
* Its outcome is not `"failure"`.


### Compression strategies [apm-span-compression-strategy]

The {{apm-agent}} can select between two strategies to decide if two adjacent spans can be compressed. Both strategies have the benefit that only one previous span needs to be kept in memory. This is important to ensure that the agent doesn’t require large amounts of memory to enable span compression.


#### Same-Kind strategy [apm-span-compression-same]

The agent selects this strategy if two adjacent spans have the same:

* span type
* span subtype
* `destination.service.resource` (e.g. database name)


#### Exact-Match strategy [apm-span-compression-exact]

The agent selects this strategy if two adjacent spans have the same:

* span name
* span type
* span subtype
* `destination.service.resource` (e.g. database name)


### Settings [apm-span-compression-settings]

The agent has configuration settings to define upper thresholds in terms of span duration for both strategies. For the "Same-Kind" strategy, the default limit is 0 milliseconds, which means that the "Same-Kind" strategy is disabled by default. For the "Exact-Match" strategy, the default limit is 50 milliseconds. Spans with longer duration are not compressed. Please refer to the agent documentation for specifics.


### Agent support [apm-span-compression-support]

Support for span compression is available in these agents:

| Agent | Same-kind config | Exact-match config |
| --- | --- | --- |
| **Go agent** | [`ELASTIC_APM_SPAN_COMPRESSION_SAME_KIND_MAX_DURATION`](https://www.elastic.co/guide/en/apm/agent/go/{{apm-go-branch}}/configuration.html#config-span-compression-same-kind-duration) | [`ELASTIC_APM_SPAN_COMPRESSION_EXACT_MATCH_MAX_DURATION`](https://www.elastic.co/guide/en/apm/agent/go/{{apm-go-branch}}/configuration.html#config-span-compression-exact-match-duration) |
| **Java agent** | [`span_compression_same_kind_max_duration`](https://www.elastic.co/guide/en/apm/agent/java/{{apm-java-branch}}/config-huge-traces.html#config-span-compression-same-kind-max-duration) | [`span_compression_exact_match_max_duration`](https://www.elastic.co/guide/en/apm/agent/java/{{apm-java-branch}}/config-huge-traces.html#config-span-compression-exact-match-max-duration) |
| **.NET agent** | [`SpanCompressionSameKindMaxDuration`](https://www.elastic.co/guide/en/apm/agent/dotnet/{{apm-dotnet-branch}}/config-core.html#config-span-compression-same-kind-max-duration) | [`SpanCompressionExactMatchMaxDuration`](https://www.elastic.co/guide/en/apm/agent/dotnet/{{apm-dotnet-branch}}/config-core.html#config-span-compression-exact-match-max-duration) |
| **Node.js agent** | [`spanCompressionSameKindMaxDuration`](https://www.elastic.co/guide/en/apm/agent/nodejs/{{apm-node-branch}}/configuration.html#span-compression-same-kind-max-duration) | [`spanCompressionExactMatchMaxDuration`](https://www.elastic.co/guide/en/apm/agent/nodejs/{{apm-node-branch}}/configuration.html#span-compression-exact-match-max-duration) |
| **Python agent** | [`span_compression_same_kind_max_duration`](https://www.elastic.co/guide/en/apm/agent/python/{{apm-py-branch}}/configuration.html#config-span-compression-same-kind-max-duration) | [`span_compression_exact_match_max_duration`](https://www.elastic.co/guide/en/apm/agent/python/{{apm-py-branch}}/configuration.html#config-span-compression-exact-match-max_duration) |
