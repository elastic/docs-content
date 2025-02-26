---
navigation_title: "Real User Monitoring (RUM)"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configuration-rum.html
applies_to:
  stack: all
---



# Configure Real User Monitoring (RUM) [apm-configuration-rum]


::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-yes.svg "")

Most options in this section are supported by all APM Server deployment methods.

::::


The [Real User Monitoring (RUM) agent](asciidocalypse://docs/apm-agent-rum-js/docs/reference/index.md) captures user interactions with clients such as web browsers. These interactions are sent as events to the APM Server. Because the RUM agent runs on the client side, the connection between agent and server is unauthenticated. As a security precaution, RUM is therefore disabled by default.

:::::::{tab-set}

::::::{tab-item} APM Server binary
To enable RUM support, set `apm-server.rum.enabled` to `true` in your APM Server configuration file.

Example config:

```yaml
apm-server.rum.enabled: true
apm-server.auth.anonymous.rate_limit.event_limit: 300
apm-server.auth.anonymous.rate_limit.ip_limit: 1000
apm-server.auth.anonymous.allow_service: [your_service_name]
apm-server.rum.allow_origins: ['*']
apm-server.rum.allow_headers: ["header1", "header2"]
apm-server.rum.library_pattern: "node_modules|bower_components|~"
apm-server.rum.exclude_from_grouping: "^/webpack"
apm-server.rum.source_mapping.enabled: true
apm-server.rum.source_mapping.cache.expiration: 5m
apm-server.rum.source_mapping.elasticsearch.api_key: TiNAGG4BaaMdaH1tRfuU:KnR6yE41RrSowb0kQ0HWoA
```
::::::

::::::{tab-item} Fleet-managed
To enable RUM, set [Enable RUM](#apm-rum-enable) to `true`.

Configure and customize Fleet-managed APM settings directly in {{kib}}:

1. In {{kib}}, find **Fleet** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under the **Agent policies** tab, select the policy you would like to configure.
3. Find the Elastic APM integration and select **Actions** > **Edit integration**.
4. Look for these options under **Real User Monitoring**.
::::::

:::::::
In addition, if APM Server is deployed in an origin different than the page’s origin, you will need to configure [Cross-Origin Resource Sharing (CORS)](asciidocalypse://docs/apm-agent-rum-js/docs/reference/configuring-cors.md) in the Agent.


## Configuration reference [apm-enable-rum-support]


### Enable RUM [apm-rum-enable]

To enable RUM support, set to `true`. By default this is disabled. (bool)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.rum.enabled` |
| Fleet-managed | `Enable RUM` |

::::{note}
If an [API key](api-keys.md) or [secret token](secret-token.md) is configured, enabling RUM support will automatically enable [Anonymous authentication](configure-anonymous-authentication.md). Anonymous authentication is required as the RUM agent runs in the browser.

::::



### Allowed Origins [apm-rum-allow-origins]

A list of permitted origins for RUM support. User-agents send an Origin header that will be validated against this list. This is done automatically by modern browsers as part of the [CORS specification](https://www.w3.org/TR/cors/). An origin is made of a protocol scheme, host and port, without the URL path.

Default: `['*']` (allows everything). (text)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.rum.allow_origins` |
| Fleet-managed | `Allowed Origins` |


### Access-Control-Allow-Headers [apm-rum-allow-headers]

HTTP requests made from the RUM agent to the APM Server are limited in the HTTP headers they are allowed to have. If any other headers are added, the request will be rejected by the browser due to Cross-Origin Resource Sharing (CORS) restrictions. Use this setting to allow additional headers. The default list of allowed headers includes "Content-Type", "Content-Encoding", and "Accept"; custom values configured here are appended to the default list and used as the value for the `Access-Control-Allow-Headers` header.

Default: `[]`. (text)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.rum.allow_headers` |
| Fleet-managed | `Access-Control-Allow-Headers` |


### Custom HTTP response headers [apm-rum-response-headers]

Custom HTTP headers to add to RUM responses. This can be useful for security policy compliance.

Values set for the same key will be concatenated.

Default: none. (text)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.rum.response_headers` |
| Fleet-managed | `Custom HTTP response headers` |


### Library Frame Pattern [apm-rum-library-pattern]

RegExp to be matched against a stack trace frame’s `file_name` and `abs_path` attributes. If the RegExp matches, the stack trace frame is considered to be a library frame. When source mapping is applied, the `error.culprit` is set to reflect the *function* and the *filename* of the first non library frame. This aims to provide an entry point for identifying issues.

Default: `"node_modules|bower_components|~"`. (text)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.rum.library_pattern` |
| Fleet-managed | `Library Frame Pattern` |


### Exclude from grouping [_exclude_from_grouping]

RegExp to be matched against a stack trace frame’s `file_name`. If the RegExp matches, the stack trace frame is excluded from being used for calculating error groups.

Default: `"^/webpack"` (excludes stack trace frames that have a filename starting with `/webpack`). (text)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.rum.exclude_from_grouping` |
| Fleet-managed | `Exclude from grouping` |


## Source map configuration options [apm-rum-source-map]

::::{admonition}
![supported deployment methods](../../../images/observability-binary-yes-fm-no.svg "")

Source maps are supported by all APM Server deployment methods, however, the options in this section are only supported by the APM Server binary.

::::



### `source_mapping.enabled` [apm-config-sourcemapping-enabled]

Used to enable/disable [source mapping](create-upload-source-maps-rum.md) for RUM events. When enabled, the APM Server needs additional privileges to read source maps. See [Use feature roles](create-assign-feature-roles-to-apm-server-users.md#apm-privileges-rum-source-mapping) for more details.

Default: `true`


### `source_mapping.elasticsearch` [apm-config-sourcemapping-elasticsearch]

Configure the {{es}} source map retrieval location, taking the same options as [output.elasticsearch](configure-elasticsearch-output.md). This must be set when using an output other than {{es}}, and that output is writing to {{es}}. Otherwise leave this section empty.


### `source_mapping.cache.expiration` [apm-rum-sourcemap-cache]

If a source map has been uploaded to the APM Server, [source mapping](create-upload-source-maps-rum.md) is automatically applied to documents sent to the RUM endpoint. Source maps are fetched from {{es}} and then kept in an in-memory cache for the configured time. Values configured without a time unit are treated as seconds.

Default: `5m` (5 minutes)


### `source_mapping.index_pattern` [_source_mapping_index_pattern]

Previous versions of APM Server stored source maps in `apm-%{[observer.version]}-sourcemap` indices. Search source maps stored in an older version with this setting.

Default: `"apm-*-sourcemap*"`


## Ingest pipelines [_ingest_pipelines]

The default APM Server pipeline includes processors that enrich RUM data prior to indexing in {{es}}. See [Parse data using ingest pipelines](parse-data-using-ingest-pipelines.md) for details on how to locate, edit, or disable this preprocessing.
