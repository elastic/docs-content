---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-filtering.html
---

# Built-in data filters [apm-filtering]

Built-in data filters allow you to filter or turn off ingestion of the following types of data:

| Data type | Common sensitive data |
| --- | --- |
| [HTTP headers](#apm-filters-http-header) | Passwords, credit card numbers, authorization, etc. |
| [HTTP bodies](#apm-filters-http-body) | Passwords, credit card numbers, etc. |
| [Personal data](#apm-filters-personal-data) | Client IP address and user agent. |
| [Real user monitoring data](#apm-filters-real-user-data) | URLs visited, click events, user browser errors, resources used, etc. |
| [Database statements](#apm-filters-database-statements) | Sensitive user or business information |


## HTTP headers [apm-filters-http-header]

By default, APM agents capture HTTP request and response headers (including cookies). Most Elastic APM agents provide the ability to sanitize HTTP header fields, including cookies and `application/x-www-form-urlencoded` data (POST form fields). Query string and captured request bodies, like `application/json` data, are not sanitized.

The default list of sanitized fields attempts to target common field names for data relating to passwords, credit card numbers, authorization, etc., but can be customized to fit your data. This sensitive data never leaves the instrumented service.

This setting supports [Central configuration](apm-agent-central-configuration.md), which means the list of sanitized fields can be updated without needing to redeploy your services:

* Go: [`ELASTIC_APM_SANITIZE_FIELD_NAMES`](asciidocalypse://docs/apm-agent-go/docs/reference/configuration.md#config-sanitize-field-names)
* Java: [`sanitize_field_names`](asciidocalypse://docs/apm-agent-java/docs/reference/config-core.md#config-sanitize-field-names)
* .NET: [`sanitizeFieldNames`](asciidocalypse://docs/apm-agent-dotnet/docs/reference/config-core.md#config-sanitize-field-names)
* Node.js: [`sanitizeFieldNames`](asciidocalypse://docs/apm-agent-nodejs/docs/reference/configuration.md#sanitize-field-names)
* Python: [`sanitize_field_names`](asciidocalypse://docs/apm-agent-python/docs/reference/configuration.md#config-sanitize-field-names)
* Ruby: [`sanitize_field_names`](asciidocalypse://docs/apm-agent-ruby/docs/reference/configuration.md#config-sanitize-field-names)

Alternatively, you can completely disable the capturing of HTTP headers. This setting also supports [Central configuration](apm-agent-central-configuration.md):

* Go: [`ELASTIC_APM_CAPTURE_HEADERS`](asciidocalypse://docs/apm-agent-go/docs/reference/configuration.md#config-capture-headers)
* Java: [`capture_headers`](asciidocalypse://docs/apm-agent-java/docs/reference/config-core.md#config-capture-headers)
* .NET: [`CaptureHeaders`](asciidocalypse://docs/apm-agent-dotnet/docs/reference/config-http.md#config-capture-headers)
* Node.js: [`captureHeaders`](asciidocalypse://docs/apm-agent-nodejs/docs/reference/configuration.md#capture-headers)
* Python: [`capture_headers`](asciidocalypse://docs/apm-agent-python/docs/reference/configuration.md#config-capture-headers)
* Ruby: [`capture_headers`](asciidocalypse://docs/apm-agent-ruby/docs/reference/configuration.md#config-capture-headers)


## HTTP bodies [apm-filters-http-body]

By default, the body of HTTP requests is not recorded. Request bodies often contain sensitive data like passwords or credit card numbers, so use care when enabling this feature.

This setting supports [Central configuration](apm-agent-central-configuration.md), which means the list of sanitized fields can be updated without needing to redeploy your services:

* Go: [`ELASTIC_APM_CAPTURE_BODY`](asciidocalypse://docs/apm-agent-go/docs/reference/configuration.md#config-capture-body)
* Java: [`capture_body`](asciidocalypse://docs/apm-agent-java/docs/reference/config-core.md#config-capture-body)
* .NET: [`CaptureBody`](asciidocalypse://docs/apm-agent-dotnet/docs/reference/config-http.md#config-capture-body)
* Node.js: [`captureBody`](asciidocalypse://docs/apm-agent-nodejs/docs/reference/configuration.md#capture-body)
* Python: [`capture_body`](asciidocalypse://docs/apm-agent-python/docs/reference/configuration.md#config-capture-body)
* Ruby: [`capture_body`](asciidocalypse://docs/apm-agent-ruby/docs/reference/configuration.md#config-capture-body)


## Personal data [apm-filters-personal-data]

By default, the APM Server captures some personal data associated with trace events:

* `client.ip`: The client’s IP address. Typically derived from the HTTP headers of incoming requests. `client.ip` is also used in conjunction with the [`geoip` processor](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/enrich-processor/geoip-processor.md) to assign geographical information to trace events. To learn more about how `client.ip` is derived, see [Deriving an incoming request’s `client.ip` address](anonymous-authentication.md#apm-derive-client-ip).
* `user_agent`: User agent data, including the client operating system, device name, vendor, and version.

The capturing of this data can be turned off by setting **Capture personal data** to `false`.


## Real user monitoring data [apm-filters-real-user-data]

Protecting user data is important. For that reason, individual RUM instrumentations can be disabled in the RUM agent with the [`disableInstrumentations`](asciidocalypse://docs/apm-agent-rum-js/docs/reference/configuration.md#disable-instrumentations) configuration variable. Disabled instrumentations produce no spans or transactions.

| Disable | Configuration value |
| --- | --- |
| HTTP requests | `fetch` and `xmlhttprequest` |
| Page load metrics including static resources | `page-load` |
| JavaScript errors on the browser | `error` |
| User click events including URLs visited, mouse clicks, and navigation events | `eventtarget` |
| Single page application route changes | `history` |


## Database statements [apm-filters-database-statements]

For SQL databases, APM agents do not capture the parameters of prepared statements. Note that Elastic APM currently does not make an effort to strip parameters of regular statements. Not using prepared statements makes your code vulnerable to SQL injection attacks, so be sure to use prepared statements.

For non-SQL data stores, such as {{es}} or MongoDB, Elastic APM captures the full statement for queries. For inserts or updates, the full document is not stored. To filter or obfuscate data in non-SQL database statements, or to remove the statement entirely, you can set up an ingest node pipeline.


## Agent-specific options [apm-filters-agent-specific]

Certain agents offer additional filtering and obfuscating options:

**Agent configuration options**

* (Node.js) Remove errors raised by the server-side process: disable with [captureExceptions](asciidocalypse://docs/apm-agent-nodejs/docs/reference/configuration.md#capture-exceptions).
* (Java) Remove process arguments from transactions: disabled by default with [`include_process_args`](asciidocalypse://docs/apm-agent-java/docs/reference/config-reporter.md#config-include-process-args).
