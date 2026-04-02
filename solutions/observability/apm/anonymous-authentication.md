---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-anonymous-auth.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Anonymous authentication [apm-anonymous-auth]

Elastic APM agents can send unauthenticated (anonymous) events to the APM Server. An event is considered to be anonymous if no authentication token can be extracted from the incoming request. The APM Server’s default response to these these requests depends on its configuration:

| Configuration | Default |
| --- | --- |
| An [API key](/solutions/observability/apm/api-keys.md) or [secret token](/solutions/observability/apm/secret-token.md) is configured | Anonymous requests are rejected and an authentication error is returned. |
| No API key or secret token is configured | Anonymous requests are accepted by the APM Server. |

In some cases, however, it makes sense to allow both authenticated and anonymous requests. For example, it isn’t possible to authenticate requests from front-end services as the secret token or API key can’t be protected. This is the case with the Real User Monitoring (RUM) agent running in a browser, or the Android or iOS/Swift agent running in a user application. However, you still likely want to authenticate requests from back-end services. To solve this problem, you can enable anonymous authentication in the APM Server to allow the ingestion of unauthenticated client-side APM data while still requiring authentication for server-side services.

## Configuring anonymous auth for client-side services [apm-anonymous-auth-config]

::::{note}
You can only enable and configure anonymous authentication if an [API key](/solutions/observability/apm/api-keys.md) or [secret token](/solutions/observability/apm/secret-token.md) is configured. If neither are configured, these settings will be ignored.

::::

:::::::{tab-set}

::::::{tab-item} Fleet-managed
When an [API key](/solutions/observability/apm/api-keys.md) or [secret token](/solutions/observability/apm/secret-token.md) is configured, anonymous authentication must be enabled to collect RUM data. Set **Anonymous Agent access** to true to enable anonymous authentication.

When configuring anonymous authentication for client-side services, there are a few configuration variables that can mitigate the impact of malicious requests to an unauthenticated APM Server endpoint.

Use the **Allowed anonymous agents** and **Allowed anonymous services** configs to ensure that the `agent.name` and `service.name` of each incoming request match a specified list.

Additionally, the APM Server can rate-limit unauthenticated requests based on the client IP address (`client.ip`) of the request. This allows you to specify the maximum number of requests allowed per unique IP address, per second.
::::::

::::::{tab-item} APM Server binary
When an [API key](/solutions/observability/apm/api-keys.md) or [secret token](/solutions/observability/apm/secret-token.md) is configured, anonymous authentication must be enabled to collect RUM data. To enable anonymous access, set either [`apm-server.rum.enabled`](/solutions/observability/apm/apm-server/configure-real-user-monitoring-rum.md#apm-rum-enable) or [`apm-server.auth.anonymous.enabled`](/solutions/observability/apm/apm-server/configure-anonymous-authentication.md#apm-config-auth-anon-enabled) to `true`.

Because anyone can send anonymous events to the APM Server, additional configuration variables are available to rate limit the number anonymous events the APM Server processes; throughput is equal to the `rate_limit.ip_limit` times the `rate_limit.event_limit`.

See [Anonymous authentication](/solutions/observability/apm/apm-server/configure-anonymous-authentication.md) for a complete list of options and a sample configuration file.
::::::

:::::::

## Deriving an incoming request’s `client.ip` address [apm-derive-client-ip]

The remote IP address of an incoming request might be different from the end-user’s actual IP address, for example, because of a proxy. For this reason, the APM Server attempts to derive the IP address of an incoming request from HTTP headers. The supported headers are parsed in the following order:

1. `Forwarded`
2. `X-Real-Ip`
3. `X-Forwarded-For`

If none of these headers are present, the remote address for the incoming request is used.

### Using a reverse proxy or load balancer [apm-derive-client-ip-concerns]

HTTP headers are easily modified; it’s possible for anyone to spoof the derived `client.ip` value by changing or setting, for example, the value of the `X-Forwarded-For` header. For this reason, if any of your clients are not trusted, we recommend setting up a reverse proxy or load balancer in front of the APM Server.

Using a proxy allows you to clear any existing IP-forwarding HTTP headers, and replace them with one set by the proxy. This prevents malicious users from cycling spoofed IP addresses to bypass the APM Server’s rate limiting feature.
