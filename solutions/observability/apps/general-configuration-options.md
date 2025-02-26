---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configuration-process.html
applies_to:
  stack: all
---

# General configuration options [apm-configuration-process]

::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-yes.svg "")

Most options on this page are supported by all APM Server deployment methods.

::::


General APM Server configuration options.

:::::::{tab-set}

::::::{tab-item} APM Server binary
**Example config file:**

```yaml
apm-server:
  host: "localhost:8200"
  rum:
    enabled: true

max_procs: 4
```
::::::

::::::{tab-item} Fleet-managed
Configure and customize Fleet-managed APM settings directly in {{kib}}:

1. In {{kib}}, find **Fleet** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under the **Agent policies** tab, select the policy you would like to configure.
3. Find the Elastic APM integration and select **Actions** > **Edit integration**.
4. Look for these settings under **General**.
::::::

:::::::

## Configuration options [apm-configuration-apm-server]


### Host [apm-host]

Defines the host and port the server is listening on. Use `"unix:/path/to.sock"` to listen on a Unix domain socket. Defaults to *localhost:8200*. (text)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.host` |
| Fleet-managed | `Host` |


### URL [_url]

The publicly reachable server URL. For deployments on Elastic Cloud or ECK, the default is unchangeable.

|     |     |
| --- | --- |
| APM Server binary | N/A |
| Fleet-managed | `URL` |


### Max header size [apm-max_header_size]

Maximum permitted size of a request’s header accepted by the server to be processed (in Bytes). Defaults to 1048576 Bytes (1 MB). (int)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.max_header_size` |
| Fleet-managed | `Maximum size of a request's header` |


### Idle timeout [apm-idle_timeout]

Maximum amount of time to wait for the next incoming request before underlying connection is closed. Defaults to `45s` (45 seconds). (text)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.idle_timeout` |
| Fleet-managed | `Idle time before underlying connection is closed` |


### Read timeout [apm-read_timeout]

Maximum permitted duration for reading an entire request. Defaults to `3600s` (3600 seconds). (text)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.read_timeout` |
| Fleet-managed | `Maximum duration for reading an entire request` |


### Write timeout [apm-write_timeout]

Maximum permitted duration for writing a response. Defaults to `30s` (30 seconds). (text)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.write_timeout` |
| Fleet-managed | `Maximum duration for writing a response` |


#### Shutdown timeout [apm-shutdown_timeout]

Maximum duration in seconds before releasing resources when shutting down the server. Defaults to `30s` (30 seconds). (text)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.shutdown_timeout` |
| Fleet-managed | `Maximum duration before releasing resources when shutting down` |


### Max event size [apm-max_event_size]

Maximum permitted size of an event accepted by the server to be processed (in Bytes). Defaults to `307200` Bytes. (int)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.max_event_size` |
| Fleet-managed | `Maximum size per event` |


### Max connections [apm-max_connections]

Maximum number of TCP connections to accept simultaneously. Default value is 0, which means *unlimited*. (int)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.max_connections` |
| Fleet-managed | `Simultaneously accepted connections` |


### Custom HTTP response headers [apm-custom_http_headers]

Custom HTTP headers to add to HTTP responses. Useful for security policy compliance. (text)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.response_headers` |
| Fleet-managed | `Custom HTTP response headers` |


### Capture personal data [apm-capture_personal_data]

If true, APM Server captures the IP of the instrumented service and its User Agent if any. Enabled by default. (bool)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.capture_personal_data` |
| Fleet-managed | `Capture personal data` |


### Default service environment [apm-default_service_environment]

Sets the default service environment to associate with data and requests received from agents which have no service environment defined. Default: none. (text)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.default_service_environment` |
| Fleet-managed | `Default Service Environment` |


### expvar support [apm-expvar.enabled]

When set to true APM Server exposes [golang expvar](https://golang.org/pkg/expvar/) under `/debug/vars`. Disabled by default.

|     |     |
| --- | --- |
| APM Server binary | `apm-server.expvar.enabled` |
| Fleet-managed | `Enable APM Server Golang expvar support` |


### expvar URL [apm-expvar.url]

Configure the URL to expose expvar. Defaults to `debug/vars`.

|     |     |
| --- | --- |
| APM Server binary | `apm-server.expvar.url` |
| Fleet-managed | N/A |


### Data stream namespace [apm-data_streams.namespace]

Change the default namespace. This setting changes the name of the data stream.

For {{fleet}}-managed users, the namespace is inherited from the selected {{agent}} policy.

|     |     |
| --- | --- |
| APM Server binary | `apm-server.data_streams.namespace` |
| Fleet-managed | `Namespace` (Integration settings > Advanced options) |
