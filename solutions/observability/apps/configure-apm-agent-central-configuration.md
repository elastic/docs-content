---
navigation_title: "APM agent central configuration"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configure-agent-config.html
applies_to:
  stack: all
---



# Configure APM agent central configuration [apm-configure-agent-config]


::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-yes.svg "")

APM agent central configuration is supported by all APM Server deployment methods, but some options are only supported for APM Server binary users.

::::


APM agent central configuration allows you to fine-tune your APM agents from within the Applications UI. Changes are automatically propagated to your APM agents, so there’s no need to redeploy your applications.

To learn more about this feature, see [APM agent central configuration](apm-agent-central-configuration.md).


## APM agent configuration options [_apm_agent_configuration_options]

**The following options are only supported for APM Server binary users**.

You can specify APM agent configuration options in the `apm-server.agent.config` section of the `apm-server.yml` config file. Here’s a sample configuration:

```yaml
apm-server.agent.config.cache.expiration: 45s
apm-server.agent.config.elasticsearch.api_key: TiNAGG4BaaMdaH1tRfuU:KnR6yE41RrSowb0kQ0HWoA <1>
```

1.  You *must* set the API key to be configured to **Beats**. Base64 encoded API keys are not currently supported in this configuration. For details on how to create and configure a compatible API key, refer to [Create an API key for writing events](grant-access-using-api-keys.md#apm-beats-api-key-publish).



### `apm-server.agent.config.cache.expiration` [apm-agent-config-cache]

When using APM agent central configuration, information fetched from {{es}} will be cached in memory for some time. Specify the cache expiration time via this setting. Defaults to `30s` (30 seconds).


### `apm-server.agent.config.elasticsearch` [apm-agent-config-elasticsearch]

Takes the same options as [output.elasticsearch](configure-elasticsearch-output.md).

For APM Server binary users and Elastic Agent standalone-managed APM Server, APM agent central configuration is automatically fetched from {{es}} using the `output.elasticsearch` configuration. If `output.elasticsearch` isn’t set or doesn’t have sufficient privileges, use these {{es}} options to provide {{es}} access.


### Common problems [_common_problems]


#### HTTP 403 errors [_http_403_errors]

You may see either of the following HTTP 403 errors from APM Server when it attempts to fetch the APM agent central configuration:

APM agent log:

```txt
"Your Elasticsearch configuration does not support agent config queries. Check your configurations at `output.elasticsearch` or `apm-server.agent.config.elasticsearch`."
```

APM Server log:

```txt
rejecting fetch request: no valid elasticsearch config
```

This occurs because the user or API key set in either `apm-server.agent.config.elasticsearch` or `output.elasticsearch` (if `apm-server.agent.config.elasticsearch` is not set) does not have adequate permissions to read source maps from {{es}}.

To fix this error, ensure that APM Server has all the required privileges. For more details, refer to [Create a *central configuration management* role](create-assign-feature-roles-to-apm-server-users.md#apm-privileges-agent-central-config-server).


#### HTTP 401 errors [_http_401_errors]

If you get an HTTP 401 error from APM Server, make sure that you’re using an API key that is configured to **Beats**. For details on how to create and configure a compatible API key, refer to [Create an API key for writing events](grant-access-using-api-keys.md#apm-beats-api-key-publish).
