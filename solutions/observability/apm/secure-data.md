---
navigation_title: Secure data
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-data-security.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
---

# Application data security [apm-data-security]

When setting up Elastic APM, it’s essential to review all captured data carefully to ensure it doesn’t contain sensitive information like passwords, credit card numbers, or health data. In addition, you may wish to filter out other identifiable information, like IP addresses, user agent information, or form field data.

Depending on the type of data, we offer several different ways to filter, manipulate, or obfuscate sensitive information during or before ingestion:

* [Built-in data filters](#apm-built-in-data-filters)
* [Custom filters](#apm-custom-data-filters)

In addition to utilizing filters, you should regularly review the [sensitive fields](#apm-sensitive-fields) table to ensure sensitive data is not being ingested. If it is, it’s possible to remove or redact it. See [Delete sensitive data](/solutions/observability/apm/delete-sensitive-data.md) for more information.

## Built-in data filters [apm-built-in-data-filters]

Built-in data filters allow you to filter or turn off ingestion of the following types of data:

| Data type | Common sensitive data |
| --- | --- |
| [HTTP headers](/solutions/observability/apm/built-in-data-filters.md#apm-filters-http-header) | Passwords, credit card numbers, authorization, etc. |
| [HTTP bodies](/solutions/observability/apm/built-in-data-filters.md#apm-filters-http-body) | Passwords, credit card numbers, etc. |
| [Personal data](/solutions/observability/apm/built-in-data-filters.md#apm-filters-personal-data) | Client IP address and user agent. |
| [Real user monitoring data](/solutions/observability/apm/built-in-data-filters.md#apm-filters-real-user-data) | URLs visited, click events, user browser errors, resources used, etc. |
| [Database statements](/solutions/observability/apm/built-in-data-filters.md#apm-filters-database-statements) | Sensitive user or business information |

## Custom filters [apm-custom-data-filters]

Custom filters allow you to filter or redact other types of APM data on ingestion:

|     |     |
| --- | --- |
| [Ingest pipelines](/solutions/observability/apm/custom-filters.md#apm-filters-ingest-pipeline) | Applied at ingestion time.All agents and fields are supported. Data leaves the instrumented service.There are no performance overhead implications on the instrumented service. |
| [{{apm-agent}} filters](/solutions/observability/apm/custom-filters.md#apm-filters-in-agent) | Not supported by all agents.Data is sanitized before leaving the instrumented service.Potential overhead implications on the instrumented service |

## Sensitive fields [apm-sensitive-fields]

You should review the following fields regularly to ensure sensitive data is not being captured:

| Field | Description | Remedy |
| --- | --- | --- |
| `client.ip` | The client IP address, as forwarded by proxy. | [Personal data](/solutions/observability/apm/built-in-data-filters.md#apm-filters-personal-data) |
| `http.request.body.original` | The body of the monitored HTTP request. | [HTTP bodies](/solutions/observability/apm/built-in-data-filters.md#apm-filters-http-body) |
| `http.request.headers` | The canonical headers of the monitored HTTP request. | [HTTP headers](/solutions/observability/apm/built-in-data-filters.md#apm-filters-http-header) |
| `http.request.socket.remote_address` | The address of the last proxy or end-user (if no proxy). | [Custom filters](/solutions/observability/apm/custom-filters.md) |
| `http.response.headers` | The canonical headers of the monitored HTTP response. | [HTTP headers](/solutions/observability/apm/built-in-data-filters.md#apm-filters-http-header) |
| `process.args` | Process arguments. | [Database statements](/solutions/observability/apm/built-in-data-filters.md#apm-filters-database-statements) |
| `span.db.statement` | Database statement. | [Database statements](/solutions/observability/apm/built-in-data-filters.md#apm-filters-database-statements) |
| `stacktrace.vars` | A flat mapping of local variables captured in the stack frame | [Custom filters](/solutions/observability/apm/custom-filters.md) |
| `url.query` | The query string of the request, e.g. `?pass=hunter2`. | [Custom filters](/solutions/observability/apm/custom-filters.md) |
| `user.*` | Logged-in user information. | [Custom filters](/solutions/observability/apm/custom-filters.md) |
| `user_agent.*` | Device and version making the network request. | [Personal data](/solutions/observability/apm/built-in-data-filters.md#apm-filters-personal-data) |