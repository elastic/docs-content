---
navigation_title: "Instrumentation"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configuration-instrumentation.html
applies_to:
  stack: all
---



# Configure APM instrumentation [apm-configuration-instrumentation]


::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-no.svg "")

Instrumentation of APM Server is not yet supported for Fleet-managed APM.

::::


APM Server uses the Elastic APM Go Agent to instrument its publishing pipeline. To gain insight into the performance of APM Server, you can enable this instrumentation and send trace data to APM Server. Currently, only the {{es}} output is instrumented.

Example configuration with instrumentation enabled:

```yaml
instrumentation:
  enabled: true
  environment: production
  hosts:
    - "http://localhost:8200"
  api_key: L5ER6FEvjkmlfalBealQ3f3fLqf03fazfOV
```


## Configuration options [_configuration_options]

You can specify the following options in the `instrumentation` section of the `apm-server.yml` config file:


### `enabled` [_enabled]

Set to `true` to enable instrumentation of APM Server. Defaults to `false`.


### `environment` [_environment]

Set the environment in which APM Server is running, for example, `staging`, `production`, `dev`, etc. Environments can be filtered in the [{{kib}} Applications UI](overviews.md).


### `hosts` [_hosts]

The [APM Server](get-started-with-apm.md) hosts to report instrumentation data to. Defaults to `http://localhost:8200`.


### `api_key` [_api_key]

[API key](api-keys.md) used to secure communication with the APM Server(s). If `api_key` is set then `secret_token` will be ignored.


### `secret_token` [_secret_token_2]

[Secret token](secret-token.md) used to secure communication with the APM Server(s).

