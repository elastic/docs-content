# Edit APM user settings [ec-manage-apm-settings]

Change how Elastic APM runs by providing your own user settings. Starting in {{stack}} version 8.0, how you change APM settings and the settings that are available to you depend on how you spin up Elastic APM. There are two modes:

{{fleet}}-managed APM integration
:   New deployments created in {{stack}} version 8.0 and later will be managed by {{fleet}}.

    Check [APM configuration reference](/solutions/observability/apps/configure-apm-server.md) for information on how to configure Elastic APM in this mode.


Standalone APM Server (legacy)
:   Deployments created prior to {{stack}} version 8.0 are in legacy mode. Upgrading to or past {{stack}} 8.0 will not remove you from legacy mode.

    Check [Edit standalone APM settings (legacy)](../../../solutions/observability/apps/configure-apm-server.md#ec-edit-apm-standalone-settings) and [Supported standalone APM settings (legacy)](../../../solutions/observability/apps/configure-apm-server.md#ec-apm-settings) for information on how to configure Elastic APM in this mode.


To learn more about the differences between these modes, or to switch from Standalone APM Server (legacy) mode to {{fleet}}-managed, check [Switch to the Elastic APM integration](/solutions/observability/apps/switch-to-elastic-apm-integration.md).

## Edit standalone APM settings (legacy) [ec-edit-apm-standalone-settings]

User settings are appended to the `apm-server.yml` configuration file for your instance and provide custom configuration options.

To add user settings:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. Find your deployment on the home page in the **Hosted deployments** card and select **Manage** to access it directly. Or, select **Hosted deployments** to go to the **Deployments** page to view all of your deployments.

    On the **Deployments** page you can narrow your deployments by name, ID, or choose from several other filters. To customize your view, use a combination of filters, or change the format from a grid to a list.

3. From your deployment menu, go to the **Edit** page.
4. In the **APM** section, select **Edit user settings**. (For existing deployments with user settings, you may have to expand the **Edit apm-server.yml** caret instead.)
5. Update the user settings.
6. Select **Save changes**.

::::{note}
If a setting is not supported by {{ech}}, you will get an error message when you try to save.
::::



## Supported standalone APM settings (legacy) [ec-apm-settings]

{{ech}} supports the following setting when running APM in standalone mode (legacy).

::::{tip}
Some settings that could break your cluster if set incorrectly are blocklisted. The following settings are generally safe in cloud environments. For detailed information about APM settings, check the [APM documentation](/solutions/observability/apps/configure-apm-server.md).
::::


### Version 8.0+ [ec_version_8_0_3]

This stack version removes support for some previously supported settings. These are all of the supported settings for this version:

`apm-server.agent.config.cache.expiration`
:   When using APM agent configuration, determines cache expiration from information fetched from Kibana. Defaults to `30s`.

`apm-server.aggregation.transactions.*`
:   This functionality is experimental and may be changed or removed completely in a future release. When enabled, APM Server produces transaction histogram metrics that are used to power the APM app. Shifting this responsibility from APM app to APM Server results in improved query performance and removes the need to store unsampled transactions.

The following `apm-server.auth.anonymous.*` settings can be configured to restrict anonymous access to specified agents and/or services. This is primarily intended to allow limited access for untrusted agents, such as Real User Monitoring. Anonymous auth is automatically enabled when RUM is enabled. Otherwise, anonymous auth is disabled. When anonymous auth is enabled, only agents matching `allow_agent` and services matching `allow_service` are allowed. See below for details on default values for these.

`apm-server.auth.anonymous.allow_agent`
:   Allow anonymous access only for specified agents.

`apm-server.auth.anonymous.allow_service`
:   Allow anonymous access only for specified service names. By default, all service names are allowed. This is replacing the config option `apm-server.rum.allow_service_names`, previously available for `7.x` deployments.

`apm-server.auth.anonymous.rate_limit.event_limit`
:   Rate limiting is defined per unique client IP address, for a limited number of IP addresses. Sites with many concurrent clients should consider increasing this limit. Defaults to 1000. This is replacing the config option `apm-server.rum.event_rate.limit`, previously available for `7.x` deployments.

`apm-server.auth.anonymous.rate_limit.ip_limit`
:   Defines the maximum amount of events allowed per IP per second. Defaults to 300. The overall maximum event throughput for anonymous access is (event_limit * ip_limit). This is replacing the config option `apm-server.rum.event_rate.lru_size`, previously available for `7.x` deployments.

`apm-server.auth.api_key.enabled`
:   Enables agent authorization using Elasticsearch API Keys. This is replacing the config option `apm-server.api_key.enabled`, previously available for `7.x` deployments.

`apm-server.auth.api_key.limit`
:   Restrict how many unique API keys are allowed per minute. Should be set to at least the amount of different API keys configured in your monitored services. Every unique API key triggers one request to Elasticsearch. This is replacing the config option `apm-server.api_key.limit`, previously available for `7.x` deployments.

`apm-server.capture_personal_data`
:   When set to `true`, the server captures the IP of the instrumented service and its User Agent. Enabled by default.

`apm-server.default_service_environment`
:   If specified, APM Server will record this value in events which have no service environment defined, and add it to agent configuration queries to Kibana when none is specified in the request from the agent.

`apm-server.max_event_size`
:   Specifies the maximum allowed size of an event for processing by the server, in bytes. Defaults to `307200`.

`apm-server.rum.allow_headers`
:   A list of Access-Control-Allow-Headers to allow RUM requests, in addition to "Content-Type", "Content-Encoding", and "Accept".

`apm-server.rum.allow_origins`
:   A list of permitted origins for real user monitoring. User-agents will send an origin header that will be validated against this list. An origin is made of a protocol scheme, host, and port, without the URL path. Allowed origins in this setting can have a wildcard `*` to match anything (for example: `http://*.example.com`). If an item in the list is a single `*`, all origins will be allowed.

`apm-server.rum.enabled`
:   Enable Real User Monitoring (RUM) Support. By default RUM is enabled. RUM does not support token based authorization. Enabled RUM endpoints will not require any authorization configured for other endpoints.

`apm-server.rum.exclude_from_grouping`
:   A regexp to be matched against a stacktrace frame’s `file_name`. If the regexp matches, the stacktrace frame is not used for calculating error groups. The default pattern excludes stacktrace frames that have a filename starting with `/webpack`

`apm-server.rum.library_pattern`
:   A regexp to be matched against a stacktrace frame’s `file_name` and `abs_path` attributes. If the regexp matches, the stacktrace frame is considered to be a library frame.

`apm-server.rum.source_mapping.enabled`
:   If a source map has previously been uploaded, source mapping is automatically applied to all error and transaction documents sent to the RUM endpoint. Sourcemapping is enabled by default when RUM is enabled.

`apm-server.rum.source_mapping.cache.expiration`
:   The `cache.expiration` determines how long a source map should be cached in memory. Note that values configured without a time unit will be interpreted as seconds.

`apm-server.sampling.tail.enabled`
:   Set to `true` to enable tail based sampling. Disabled by default.

`apm-server.sampling.tail.policies`
:   Criteria used to match a root transaction to a sample rate.

`apm-server.sampling.tail.interval`
:   Synchronization interval for multiple APM Servers. Should be in the order of tens of seconds or low minutes.

`logging.level`
:   Sets the minimum log level. The default log level is error. Available log levels are: error, warning, info, or debug.

`logging.selectors`
:   Enable debug output for selected components. To enable all selectors use ["*"]. Other available selectors are "beat", "publish", or "service". Multiple selectors can be chained.

`logging.metrics.enabled`
:   If enabled, apm-server periodically logs its internal metrics that have changed in the last period. For each metric that changed, the delta from the value at the beginning of the period is logged. Also, the total values for all non-zero internal metrics are logged on shutdown. The default is false.

`logging.metrics.period`
:   The period after which to log the internal metrics. The default is 30s.

`max_procs`
:   Sets the maximum number of CPUs that can be executing simultaneously. The default is the number of logical CPUs available in the system.

`output.elasticsearch.flush_interval`
:   The maximum duration to accumulate events for a bulk request before being flushed to Elasticsearch. The value must have a duration suffix. The default is 1s.

`output.elasticsearch.flush_bytes`
:   The bulk request size threshold, in bytes, before flushing to Elasticsearch. The value must have a suffix. The default is 5MB.


### Version 7.17+ [ec_version_7_17]

This stack version includes all of the settings from 7.16 and the following:

Allow anonymous access only for specified agents and/or services. This is primarily intended to allow limited access for untrusted agents, such as Real User Monitoring. Anonymous auth is automatically enabled when RUM is enabled. Otherwise, anonymous auth is disabled. When anonymous auth is enabled, only agents matching allow_agent and services matching allow_service are allowed. See below for details on default values for these.

`apm-server.auth.anonymous.allow_agent`
:   Allow anonymous access only for specified agents.

`apm-server.auth.anonymous.allow_service`
:   Allow anonymous access only for specified service names. By default, all service names are allowed. This will be replacing the config option `apm-server.rum.allow_service_names` from `8.0` on.

`apm-server.auth.anonymous.rate_limit.event_limit`
:   Rate limiting is defined per unique client IP address, for a limited number of IP addresses. Sites with many concurrent clients should consider increasing this limit. Defaults to 1000. This will be replacing the config option`apm-server.rum.event_rate.limit` from `8.0` on.

`apm-server.auth.anonymous.rate_limit.ip_limit`
:   Defines the maximum amount of events allowed per IP per second. Defaults to 300. The overall maximum event throughput for anonymous access is (event_limit * ip_limit). This will be replacing the config option `apm-server.rum.event_rate.lru_size` from `8.0` on.

`apm-server.auth.api_key.enabled`
:   Enables agent authorization using Elasticsearch API Keys.  This will be replacing the config option `apm-server.api_key.enabled` from `8.0` on.

`apm-server.auth.api_key.limit`
:   Restrict how many unique API keys are allowed per minute. Should be set to at least the amount of different API keys configured in your monitored services. Every unique API key triggers one request to Elasticsearch. This will be replacing the config option `apm-server.api_key.limit` from `8.0` on.


### Supported versions before 8.x [ec_supported_versions_before_8_x_3]

`apm-server.aggregation.transactions.*`
:   This functionality is experimental and may be changed or removed completely in a future release. When enabled, APM Server produces transaction histogram metrics that are used to power the APM app. Shifting this responsibility from APM app to APM Server results in improved query performance and removes the need to store unsampled transactions.

`apm-server.default_service_environment`
:   If specified, APM Server will record this value in events which have no service environment defined, and add it to agent configuration queries to Kibana when none is specified in the request from the agent.

`apm-server.rum.allow_service_names`
:   A list of service names to allow, to limit service-specific indices and data streams created for unauthenticated RUM events. If the list is empty, any service name is allowed.

`apm-server.ilm.setup.mapping`
:   ILM policies now support configurable index suffixes. You can append the `policy_name` with an `index_suffix` based on the `event_type`, which can be one of `span`, `transaction`, `error`, or `metric`.

`apm-server.rum.allow_headers`
:   List of Access-Control-Allow-Headers to allow RUM requests, in addition to "Content-Type", "Content-Encoding", and "Accept".

`setup.template.append_fields`
:   A list of fields to be added to the Elasticsearch template and Kibana data view (formerly *index pattern*).

`apm-server.api_key.enabled`
:   Enabled by default. For any requests where APM Server accepts a `secret_token` in the authorization header, it now alternatively accepts an API Key.

`apm-server.api_key.limit`
:   Configure how many unique API keys are allowed per minute. Should be set to at least the amount of different API keys used in monitored services. Default value is 100.

`apm-server.ilm.setup.enabled`
:   When enabled, APM Server creates aliases, event type specific settings and ILM policies. If disabled, event type specific templates need to be managed manually.

`apm-server.ilm.setup.overwrite`
:   Set to `true` to apply custom policies and to properly overwrite templates when switching between using ILM and not using ILM.

`apm-server.ilm.setup.require_policy`
:   Set to `false` when policies are set up outside of APM Server but referenced in this configuration.

`apm-server.ilm.setup.policies`
:   Array of ILM policies. Each entry has a `name` and a `policy`.

`apm-server.ilm.setup.mapping`
:   Array of mappings of ILM policies to event types. Each entry has a `policy_name` and an `event_type`, which can be one of `span`, `transaction`, `error`, or `metric`.

`apm-server.rum.source_mapping.enabled`
:   When events are monitored using the RUM agent, APM Server tries to apply source mapping by default. This configuration option allows you to disable source mapping on stack traces.

`apm-server.rum.source_mapping.cache.expiration`
:   Sets how long a source map should be cached before being refetched from Elasticsearch. Default value is 5m.

`output.elasticsearch.pipeline`
:   APM comes with a default pipeline definition. This allows overriding it. To disable, you can set `pipeline: _none`

`apm-server.agent.config.cache.expiration`
:   When using APM agent configuration, determines cache expiration from information fetched from Kibana. Defaults to `30s`.

`apm-server.ilm.enabled`
:   Enables index lifecycle management (ILM) for the indices created by the APM Server. Defaults to `false`. If you’re updating an existing APM Server, you must also set `setup.template.overwrite: true`. If you don’t, the index template will not be overridden and ILM changes will not take effect.

`apm-server.max_event_size`
:   Specifies the maximum allowed size of an event for processing by the server, in bytes. Defaults to `307200`.

`output.elasticsearch.pipelines`
:   Adds an array for pipeline selector configurations that support conditionals, format string-based field access, and name mappings used to [parse data using ingest node pipelines](/solutions/observability/apps/application-performance-monitoring-apm.md).

`apm-server.register.ingest.pipeline.enabled`
:   Loads the pipeline definitions to Elasticsearch when the APM Server starts up. Defaults to `false`.

`apm-server.register.ingest.pipeline.overwrite`
:   Overwrites the existing pipeline definitions in Elasticsearch. Defaults to `true`.

`apm-server.rum.event_rate.lru_size`
:   Defines the number of unique IP addresses that can be tracked in the LRU cache, which keeps a rate limit for each of the most recently seen IP addresses. Defaults to `1000`.

`apm-server.rum.event_rate.limit`
:   Sets the rate limit per second for each IP address for events sent to the APM Server v2 RUM endpoint. Defaults to `300`.

`apm-server.rum.enabled`
:   Enables/disables Real User Monitoring (RUM) support. Defaults to `true` (enabled).

`apm-server.rum.allow_origins`
:   Specifies a list of permitted origins from user agents. The default is `*`, which allows everything.

`apm-server.rum.library_pattern`
:   Differentiates library frames against specific attributes. Refer to "Configure Real User Monitoring (RUM)" in the [Observability Guide](https://www.elastic.co/guide/en/observability/current) to learn more. The default value is `"node_modules|bower_components|~"`.

`apm-server.rum.exclude_from_grouping`
:   Configures the RegExp to be matched against a stacktrace frame’s `file_name`.

`apm-server.rum.rate_limit`
:   Sets the rate limit per second for each IP address for requests sent to the RUM endpoint. Defaults to `10`.

`apm-server.capture_personal_data`
:   When set to `true`, the server captures the IP of the instrumented service and its User Agent. Enabled by default.

`setup.template.settings.index.number_of_shards`
:   Specifies the number of shards for the Elasticsearch template.

`setup.template.settings.index.number_of_replicas`
:   Specifies the number of replicas for the Elasticsearch template.

`apm-server.frontend.enabled`
:   Enables/disables frontend support.

`apm-server.frontend.allow_origins`
:   Specifies the comma-separated list of permitted origins from user agents. The default is `*`, which allows everything.

`apm-server.frontend.library_pattern`
:   Differentiates library frames against [specific attributes](https://www.elastic.co/guide/en/apm/server/6.3/configuration-frontend.html). The default value is `"node_modules|bower_components|~"`.

`apm-server.frontend.exclude_from_grouping`
:   Configures the RegExp to be matched against a stacktrace frame’s `file_name`.

`apm-server.frontend.rate_limit`
:   Sets the rate limit per second per IP address for requests sent to the frontend endpoint. Defaults to `10`.

`apm-server.capture_personal_data`
:   When set to `true`, the server captures the IP address of the instrumented service and its User Agent. Enabled by default.

`max_procs`
:   Max number of CPUs used simultaneously. Defaults to the number of logical CPUs available.

`setup.template.enabled`
:   Set to false to disable loading of Elasticsearch templates used for APM indices. If set to false, you must load the template manually.

`setup.template.name`
:   Name of the template. Defaults to `apm-server`.

`setup.template.pattern`
:   The template pattern to apply to the default index settings. Default is `apm-*`

`setup.template.settings.index.number_of_shards`
:   Specifies the number of shards for the Elasticsearch template.

`setup.template.settings.index.number_of_replicas`
:   Specifies the number of replicas for the Elasticsearch template.

`output.elasticsearch.bulk_max_size`
:   Maximum number of events to bulk together in a single Elasticsearch bulk API request. By default, this number changes based on the size of the instance:

    | Instance size | Default max events |
    | --- | --- |
    | 512MB | 267 |
    | 1GB | 381 |
    | 2GB | 533 |
    | 4GB | 762 |
    | 8GB | 1067 |


`output.elasticsearch.indices`
:   Array of index selector rules supporting conditionals and formatted string.

`output.elasticsearch.index`
:   The index to write the events to. If changed, `setup.template.name` and `setup.template.pattern` must be changed accordingly.

`output.elasticsearch.worker`
:   Maximum number of concurrent workers publishing events to Elasticsearch. By default, this number changes based on the size of the instance:

    | Instance size | Default max concurrent workers |
    | --- | --- |
    | 512MB | 5 |
    | 1GB | 7 |
    | 2GB | 10 |
    | 4GB | 14 |
    | 8GB | 20 |


`queue.mem.events`
:   Maximum number of events to concurrently store in the internal queue. By default, this number changes based on the size of the instance:

    | Instance size | Default max events |
    | --- | --- |
    | 512MB | 2000 |
    | 1GB | 4000 |
    | 2GB | 8000 |
    | 4GB | 16000 |
    | 8GB | 32000 |


`queue.mem.flush.min_events`
:   Minimum number of events to have before pushing them to Elasticsearch. By default, this number changes based on the size of the instance.

`queue.mem.flush.timeout`
:   Maximum duration before sending the events to the output if the `min_events` is not crossed.


### Logging settings [ec_logging_settings]

`logging.level`
:   Specifies the minimum log level. One of *debug*, *info*, *warning*, or *error*. Defaults to *info*.

`logging.selectors`
:   The list of debugging-only selector tags used by different APM Server components. Use *** to enable debug output for all components. For example, add *publish* to display all the debug messages related to event publishing.

`logging.metrics.enabled`
:   If enabled, APM Server periodically logs its internal metrics that have changed in the last period. Defaults to *true*.

`logging.metrics.period`
:   The period after which to log the internal metrics. Defaults to *30s*.

::::{note}
To change logging settings you must first [enable deployment logging](../../../deploy-manage/monitor/stack-monitoring/elastic-cloud-stack-monitoring.md).
::::




