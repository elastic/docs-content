---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-common-response-codes.html
---

# APM Server response codes [apm-common-response-codes]


## HTTP 400: Data decoding error / Data validation error [apm-bad-request] 

The most likely cause for this error is using incompatible versions of {{apm-agent}} and APM Server. See the [agent/server compatibility matrix](apm-agent-compatibility.md) to verify compatibility.


## HTTP 400: Event too large [apm-event-too-large] 

APM agents communicate with the APM server by sending events in an HTTP request. Each event is sent as its own line in the HTTP request body. If events are too large, you should consider increasing the [Max event size](general-configuration-options.md#apm-max_event_size) setting in the APM integration, and adjusting relevant settings in the agent.


## HTTP 401: Invalid token [apm-unauthorized] 

Either the [Secret token](secret-token.md) in the request header doesn’t match the secret token configured in the APM integration, or the [API keys](api-keys.md) is invalid.


## HTTP 403: Forbidden request [apm-forbidden] 

Either you are sending requests to a [RUM](real-user-monitoring-rum.md) endpoint without RUM enabled, or a request is coming from an origin not specified in the APM integration settings. See the [Allowed origins](configure-real-user-monitoring-rum.md#apm-rum-allow-origins) setting for more information.


## HTTP 503: Request timed out waiting to be processed [apm-request-timed-out] 

This happens when APM Server exceeds the maximum number of requests that it can process concurrently. To alleviate this problem, you can try to: reduce the sample rate and/or reduce the collected stack trace information. See [Reduce storage](reduce-storage.md) for more information.

Another option is to increase processing power. This can be done by either migrating your {{agent}} to a more powerful machine or adding more APM Server instances.

