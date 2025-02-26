---
navigation_title: "Anonymous authentication"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configuration-anonymous.html
applies_to:
  stack: all
---



# Configure anonymous authentication [apm-configuration-anonymous]


::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-yes.svg "")

Most options on this page are supported by all APM Server deployment methods.

::::


Elastic APM agents can send unauthenticated (anonymous) events to the APM Server. An event is considered to be anonymous if no authentication token can be extracted from the incoming request. This is useful for agents that run on clients, like the Real User Monitoring (RUM) agent running in a browser, or the Android or iOS/Swift agent running in a user application.

Enable anonymous authentication in the APM Server to allow the ingestion of unauthenticated client-side APM data while still requiring authentication for server-side services.

:::::::{tab-set}

::::::{tab-item} APM Server binary
Example configuration:

```yaml
apm-server.auth.anonymous.enabled: true
apm-server.auth.anonymous.allow_agent: [rum-js]
apm-server.auth.anonymous.allow_service: [my_service_name]
apm-server.auth.anonymous.rate_limit.event_limit: 300
apm-server.auth.anonymous.rate_limit.ip_limit: 1000
```
::::::

::::::{tab-item} Fleet-managed
Configure and customize Fleet-managed APM settings directly in {{kib}}:

1. In {{kib}}, find **Fleet** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Under the **Agent policies** tab, select the policy you would like to configure.
3. Find the Elastic APM integration and select **Actions** > **Edit integration**.
4. Look for these settings under **Agent authorization**.
::::::

:::::::
::::{important}
All anonymous access configuration is ignored if [authenticated communication](secure-communication-with-apm-agents.md) is disabled.
::::



## Real User Monitoring (RUM) [apm-config-auth-anon-rum]

If an [API key](api-keys.md) or [secret token](secret-token.md) is configured, then anonymous authentication must be enabled to collect RUM data. For this reason, anonymous auth will be enabled automatically if [Enable RUM](configure-real-user-monitoring-rum.md#apm-rum-enable) is set to `true`, and [Anonymous Agent access](#apm-config-auth-anon-enabled) is not explicitly defined.

See [Real User Monitoring (RUM)](configure-real-user-monitoring-rum.md) for additional RUM configuration options.


### Mitigating malicious requests [apm-config-auth-anon-mitigating]

There are a few configuration variables that can mitigate the impact of malicious requests to an unauthenticated APM Server endpoint.

Use the [Allowed anonymous agents](#apm-config-auth-anon-allow-agent) and [Allowed services](#apm-config-auth-anon-allow-service) configs to ensure that the `agent.name` and `service.name` of each incoming request match a specified list.

Additionally, the APM Server can rate-limit unauthenticated requests based on the client IP address (`client.ip`) of the request with [Event limit](#apm-config-auth-anon-event-limit). This allows you to specify the maximum number of requests allowed per unique IP address, per second.


### Deriving an incoming request’s `client.ip` address [apm-config-auth-anon-client-ip]

The remote IP address of an incoming request might be different from the end-user’s actual IP address, for example, because of a proxy. For this reason, the APM Server attempts to derive the IP address of an incoming request from HTTP headers. The supported headers are parsed in the following order:

1. `Forwarded`
2. `X-Real-Ip`
3. `X-Forwarded-For`

If none of these headers are present, the remote address for the incoming request is used.


### Using a reverse proxy or load balancer [apm-config-auth-anon-client-ip-concerns]

HTTP headers are easily modified; it’s possible for anyone to spoof the derived `client.ip` value by changing or setting, for example, the value of the `X-Forwarded-For` header. For this reason, if any of your clients are not trusted, we recommend setting up a reverse proxy or load balancer in front of the APM Server.

Using a proxy allows you to clear any existing IP-forwarding HTTP headers, and replace them with one set by the proxy. This prevents malicious users from cycling spoofed IP addresses to bypass the APM Server’s rate limiting feature.


## Configuration reference [apm-config-auth-anon]


### Anonymous Agent access [apm-config-auth-anon-enabled]

Enable or disable anonymous authentication. Default: `false` (disabled). (bool)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.auth.anonymous.enabled` |
| Fleet-managed | `Anonymous Agent access` |


### Allowed anonymous agents [apm-config-auth-anon-allow-agent]

A list of permitted {{apm-agent}} names for anonymous authentication. Names in this list must match the agent’s `agent.name`. Default: `[rum-js, js-base]` (only RUM agent events are accepted). (array)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.auth.anonymous.allow_agent` |
| Fleet-managed | `Allowed Anonymous agents` |


## Allowed services [apm-config-auth-anon-allow-service]

A list of permitted service names for anonymous authentication. Names in this list must match the agent’s `service.name`. This can be used to limit the number of service-specific indices or data streams created. Default: Not set (any service name is accepted). (array)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.auth.anonymous.allow_service` |
| Fleet-managed | `Allowed Anonymous services` |


### IP limit [apm-config-auth-anon-ip-limit]

The number of unique IP addresses to track in an LRU cache. IP addresses in the cache will be rate limited according to the [Event limit](#apm-config-auth-anon-event-limit) setting. Consider increasing this default if your application has many concurrent clients. Default: `1000`. (int)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.auth.anonymous.rate_limit.ip_limit` |
| Fleet-managed | `Anonymous Rate limit (IP limit)` |


### Event limit [apm-config-auth-anon-event-limit]

The maximum number of events allowed per second, per agent IP address. Default: `300`. (int)

|     |     |
| --- | --- |
| APM Server binary | `apm-server.auth.anonymous.rate_limit.event_limit` |
| Fleet-managed | `Anonymous Event rate limit (event limit)` |
