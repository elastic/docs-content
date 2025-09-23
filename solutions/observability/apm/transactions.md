---
navigation_title: Transactions
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-data-model-transactions.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
---

# Transactions in Elastic APM [apm-data-model-transactions]

**Transactions** are a special kind of [span](/solutions/observability/apm/spans.md) that have additional attributes associated with them. They describe an event captured by an Elastic {{apm-agent}} instrumenting a service. You can think of transactions as the highest level of work you’re measuring within a service. As an example, a transaction might be a:

* Request to your server
* Batch job
* Background job
* Custom transaction type

Agents decide whether to sample transactions or not, and provide settings to control sampling behavior. If sampled, the [spans](/solutions/observability/apm/spans.md) of a transaction are sent and stored as separate documents. Within one transaction there can be 0, 1, or many spans captured.

A transaction contains:

* The timestamp of the event
* A unique id, type, and name
* Data about the environment in which the event is recorded:

    * Service - environment, framework, language, etc.
    * Host - architecture, hostname, IP, etc.
    * Process - args, PID, PPID, etc.
    * URL - full, domain, port, query, etc.
    * [User](/solutions/observability/apm/metadata.md#apm-data-model-user) - (if supplied) email, ID, username, etc.

* Other relevant information depending on the agent. Example: The JavaScript RUM agent captures transaction marks, which are points in time relative to the start of the transaction with some label.

In addition, agents provide options for users to capture custom [metadata](/solutions/observability/apm/metadata.md). Metadata can be indexed - [`labels`](/solutions/observability/apm/metadata.md#apm-data-model-labels), or not-indexed - [`custom`](/solutions/observability/apm/metadata.md#apm-data-model-custom).

Transactions are grouped by their `type` and `name` in the Applications UI’s [Transaction overview](/solutions/observability/apm/transactions-ui.md). If you’re using a supported framework, APM agents will automatically handle the naming for you. If you’re not, or if you wish to override the default, all agents have API methods to manually set the `type` and `name`.

* `type` should be a keyword of specific relevance in the service’s domain, e.g. `request`, `backgroundjob`, etc.
* `name` should be a generic designation of a transaction in the scope of a single service, e.g. `GET /users/:id`, `UsersController#show`, etc.

::::{tip}
Most agents limit keyword fields (e.g. `labels`) to 1024 characters, non-keyword fields (e.g. `span.db.statement`) to 10,000 characters.
::::

## Data streams [_data_streams_2]

Transactions are stored with spans in the following data streams:

* Application traces: `traces-apm-<namespace>`
* RUM and iOS agent application traces: `traces-apm.rum-<namespace>`

See [Data streams](/solutions/observability/apm/data-streams.md) to learn more.

## Example transaction document [_example_transaction_document]

This example shows what transaction documents can look like when indexed in {{es}}.

::::{dropdown} Expand {{es}} document
```json
[
    {
        "@timestamp": "2017-05-30T18:53:42.281Z",
        "agent": {
            "name": "elastic-node",
            "version": "3.14.0"
        },
        "container": {
            "id": "container-id"
        },
        "ecs": {
            "version": "1.12.0"
        },
        "event": {
            "ingested": "2020-08-11T09:55:04.391451Z",
            "outcome": "unknown"
        },
        "host": {
            "architecture": "x64",
            "ip": ["127.0.0.1"],
            "os": {
                "platform": "darwin"
            }
        },
        "kubernetes": {
            "namespace": "namespace1",
            "pod": {
                "name": "pod-name",
                "uid": "pod-uid"
            }
        },
        "observer": {
            "hostname": "ix.lan",
            "type": "apm-server",
            "version": "8.0.0"
        },
        "process": {
            "args": [
                "node",
                "server.js"
            ],
            "pid": 1234,
            "parent": {
                "pid": 6789
            },
            "title": "node"
        },
        "processor": {
            "event": "transaction",
            "name": "transaction"
        },
        "service": {
            "environment": "staging",
            "framework": {
                "name": "Express",
                "version": "1.2.3"
            },
            "language": {
                "name": "ecmascript",
                "version": "8"
            },
            "name": "1234_service-12a3",
            "node": {
                "name": "container-id"
            },
            "runtime": {
                "name": "node",
                "version": "8.0.0"
            },
            "version": "5.1.3"
        },
        "timestamp": {
            "us": 1496170422281000
        },
        "trace": {
            "id": "85925e55b43f4340aaaaaaaaaaaaaaaa"
        },
        "transaction": {
            "duration": {
                "us": 13980
            },
            "id": "85925e55b43f4340",
            "name": "GET /api/types",
            "result": "failure",
            "sampled": true,
            "span_count": {
                "started": 0
            },
            "type": "request"
        },
        "user": {
            "email": "foo@bar.com",
            "id": "123user",
            "name": "foo"
        }
    },
    {
        "@timestamp": "2017-05-30T18:53:42.281Z",
        "agent": {
            "name": "elastic-node",
            "version": "3.14.0"
        },
        "container": {
            "id": "container-id"
        },
        "ecs": {
            "version": "1.12.0"
        },
        "event": {
            "ingested": "2020-08-11T09:55:04.391639Z",
            "outcome": "unknown"
        },
        "host": {
            "architecture": "x64",
            "ip": "127.0.0.1",
            "os": {
                "platform": "darwin"
            }
        },
        "kubernetes": {
            "namespace": "namespace1",
            "pod": {
                "name": "pod-name",
                "uid": "pod-uid"
            }
        },
        "observer": {
            "ephemeral_id": "fb037b97-0027-401a-9dc4-17d162f2687f",
            "hostname": "goat",
            "id": "a4daf4ca-b280-4ede-90df-bf62482cec37",
            "type": "apm-server",
            "version": "8.0.0"
        },
        "process": {
            "args": [
                "node",
                "server.js"
            ],
            "pid": 1234,
            "parent": {
                "pid": 6789
            },
            "title": "node"
        },
        "processor": {
            "event": "transaction",
            "name": "transaction"
        },
        "service": {
            "environment": "staging",
            "framework": {
                "name": "Express",
                "version": "1.2.3"
            },
            "language": {
                "name": "ecmascript",
                "version": "8"
            },
            "name": "1234_service-12a3",
            "node": {
                "name": "container-id"
            },
            "runtime": {
                "name": "node",
                "version": "8.0.0"
            },
            "version": "5.1.3"
        },
        "timestamp": {
            "us": 1496170422281999
        },
        "trace": {
            "id": "85925e55b43f4342aaaaaaaaaaaaaaaa"
        },
        "transaction": {
            "duration": {
                "us": 13980
            },
            "id": "85925e55b43f4342",
            "name": "GET /api/types",
            "result": "200",
            "sampled": true,
            "span_count": {
                "dropped": 258,
                "started": 1
            },
            "type": "request"
        },
        "user": {
            "email": "foo@bar.com",
            "id": "123user",
            "name": "foo"
        }
    },
    {
        "@timestamp": "2017-05-30T18:53:27.154Z",
        "agent": {
            "name": "js-base",
            "version": "1.3"
        },
        "client": {
            "geo": {
                "continent_name": "North America",
                "country_iso_code": "US",
                "country_name": "United States",
                "location": {
                    "lat": 37.751,
                    "lon": -97.822
                }
            },
            "ip": "8.8.8.8"
        },
        "container": {
            "id": "container-id"
        },
        "ecs": {
            "version": "1.12.0"
        },
        "event": {
            "ingested": "2020-08-11T09:55:04.338986Z",
            "outcome": "unknown"
        },
        "host": {
            "architecture": "x64",
            "ip": "127.0.0.1",
            "os": {
                "platform": "darwin"
            }
        },
        "http": {
            "request": {
                "body": {
                    "original": {
                        "additional": {
                            "bar": 123,
                            "req": "additional information"
                        },
                        "str": "hello world"
                    }
                },
                "cookies": {
                    "c1": "v1",
                    "c2": "v2"
                },
                "env": {
                    "GATEWAY_INTERFACE": "CGI/1.1",
                    "SERVER_SOFTWARE": "nginx"
                },
                "headers": {
                    "Array": [
                        "foo",
                        "bar",
                        "baz"
                    ],
                    "Content-Type": [
                        "text/html"
                    ],
                    "Cookie": [
                        "c1=v1,c2=v2"
                    ],
                    "Some-Other-Header": [
                        "foo"
                    ],
                    "User-Agent": [
                        "Mozilla Chrome Edge"
                    ]
                },
                "method": "POST",
                "referrer": "http://localhost:8000/test/e2e/"
            },
            "response": {
                "finished": true,
                "headers": {
                    "Content-Type": [
                        "application/json"
                    ]
                },
                "headers_sent": true,
                "status_code": 200
            },
            "version": "1.1"
        },
        "kubernetes": {
            "namespace": "namespace1",
            "pod": {
                "name": "pod-name",
                "uid": "pod-uid"
            }
        },
        "labels": {
            "bool_error": false,
            "number_code": 2,
            "organization_uuid": "9f0e9d64-c185-4d21-a6f4-4673ed561ec8"
        },
        "observer": {
            "ephemeral_id": "fb037b97-0027-401a-9dc4-17d162f2687f",
            "hostname": "goat",
            "id": "a4daf4ca-b280-4ede-90df-bf62482cec37",
            "type": "apm-server",
            "version": "8.0.0"
        },
        "process": {
            "args": [
                "node",
                "server.js"
            ],
            "pid": 1234,
            "parent": {
                "pid": 6789
            },
            "title": "node"
        },
        "processor": {
            "event": "transaction",
            "name": "transaction"
        },
        "service": {
            "environment": "staging",
            "framework": {
                "name": "Express",
                "version": "1.2.3"
            },
            "language": {
                "name": "ecmascript",
                "version": "8"
            },
            "name": "serviceabc",
            "node": {
                "name": "special-name"
            },
            "runtime": {
                "name": "javascript",
                "version": "8.0.0"
            },
            "version": "5.1.3"
        },
        "source": {
            "ip": "8.8.8.8"
        },
        "timestamp": {
            "us": 1496170407154000
        },
        "trace": {
            "id": "945254c567a5417eaaaaaaaaaaaaaaaa"
        },
        "transaction": {
            "custom": {
                "(": "not a valid regex and that is fine",
                "and_objects": {
                    "foo": [
                        "bar",
                        "baz"
                    ]
                },
                "my_key": 1,
                "some_other_value": "foo bar"
            },
            "duration": {
                "us": 32592
            },
            "id": "945254c567a5417e",
            "marks": {
                "another_mark": {
                    "some_float": 10,
                    "some_long": 10
                },
                "navigationTiming": {
                    "appBeforeBootstrap": 608.9300000000001,
                    "navigationStart": -21
                }
            },
            "name": "GET /api/types",
            "result": "success",
            "sampled": true,
            "span_count": {
                "dropped": 2,
                "started": 4
            },
            "type": "request"
        },
        "url": {
            "domain": "www.example.com",
            "fragment": "#hash",
            "full": "https://www.example.com/p/a/t/h?query=string#hash",
            "original": "/p/a/t/h?query=string#hash",
            "path": "/p/a/t/h",
            "port": 8080,
            "query": "?query=string",
            "scheme": "https"
        },
        "user": {
            "email": "foo@example.com",
            "id": "99"
        },
        "user_agent": {
            "device": {
                "name": "Other"
            },
            "name": "Other",
            "original": "Mozilla Chrome Edge"
        }
    }
]
```

::::

