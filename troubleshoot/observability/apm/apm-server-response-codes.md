---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-common-response-codes.html
applies_to:
  stack: all
  serverless:
    observability: all
products:
  - id: observability
---

# APM Server response codes [apm-common-response-codes]


## HTTP 400: Data decoding error / Data validation error [apm-bad-request]

::::{applies-switch}

:::{applies-item} stack:
The most likely cause for this error is using incompatible versions of {{apm-agent}} and APM Server. See the [agent/server compatibility matrix](/solutions/observability/apm/apm-agent-compatibility.md) to verify compatibility.
:::

:::{applies-item} serverless:
The most likely cause for this error is using an incompatible version of an {{apm-agent}}. See [minimum supported APM agent versions](/solutions/observability/apm/apm-agents/index.md#observability-apm-agents-elastic-apm-agents-minimum-supported-versions) to verify compatibility.
:::

::::


## HTTP 400: Event too large [apm-event-too-large]

::::{applies-switch}

:::{applies-item} stack:
APM agents communicate with the APM server by sending events in an HTTP request. Each event is sent as its own line in the HTTP request body. If events are too large, you should consider increasing the [Max event size](/solutions/observability/apm/apm-server/general-configuration-options.md#apm-max_event_size) setting in the APM integration, and adjusting relevant settings in the agent.
:::

:::{applies-item} serverless:
APM agents communicate with the Managed intake service by sending events in an HTTP request. Each event is sent as its own line in the HTTP request body. If events are too large, you can reduce the size of the events that your APM agents send by: [enabling span compression](/solutions/observability/apm/spans.md) or [reducing collected stack trace information](/solutions/observability/apm/reduce-storage.md#observability-apm-reduce-stacktrace).
:::

::::


## HTTP 401: Invalid token [apm-unauthorized]

::::{applies-switch}

:::{applies-item} stack:
Either the [Secret token](/solutions/observability/apm/secret-token.md) in the request header doesn’t match the secret token configured in the APM integration, or the [API keys](/solutions/observability/apm/api-keys.md) is invalid.
:::

:::{applies-item} serverless:
The API key is invalid.
:::

::::


## HTTP 403: Forbidden request [apm-forbidden]

Either you are sending requests to a [RUM](/solutions/observability/apm/apm-agents/real-user-monitoring-rum.md) endpoint without RUM enabled, or a request is coming from an origin not specified in the APM integration settings. See the [Allowed origins](/solutions/observability/apm/apm-server/configure-real-user-monitoring-rum.md#apm-rum-allow-origins) setting for more information.


## HTTP 503: Request timed out waiting to be processed [apm-request-timed-out]

This happens when APM Server exceeds the maximum number of requests that it can process concurrently. To alleviate this problem, you can try to: reduce the sample rate and/or reduce the collected stack trace information. See [Reduce storage](/solutions/observability/apm/reduce-storage.md) for more information.

Another option is to increase processing power. This can be done by either migrating your {{agent}} to a more powerful machine or adding more APM Server instances.

