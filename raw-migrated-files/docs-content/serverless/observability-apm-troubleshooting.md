# Troubleshooting [observability-apm-troubleshooting]

This section provides solutions to common questions and problems.


## Common problems [observability-apm-troubleshooting-common-problems]


### Field limit exceeded [field-limit-exceeded-legacy]

When adding too many distinct tag keys on a transaction or span, you risk creating a [mapping explosion](../../../manage-data/data-store/mapping.md#mapping-limit-settings).

For example, you should avoid that user-specified data, like URL parameters, is used as a tag key. Likewise, using the current timestamp or a user ID as a tag key is not a good idea. However, tag **values** with a high cardinality are not a problem. Just try to keep the number of distinct tag keys at a minimum.

The symptom of a mapping explosion is that transactions and spans are not indexed anymore after a certain time. Usually, on the next day, the spans and transactions will be indexed again because a new index is created each day. But as soon as the field limit is reached, indexing stops again.


## Common response codes [observability-apm-troubleshooting-common-response-codes]


### HTTP 400: Data decoding error / Data validation error [bad-request]

The most likely cause for this error is using an incompatible version of an {{apm-agent}}. See [minimum supported APM agent versions](../../../solutions/observability/apps/elastic-apm-agents.md#observability-apm-agents-elastic-apm-agents-minimum-supported-versions) to verify compatibility.


### HTTP 400: Event too large [event-too-large]

APM agents communicate with the Managed intake service by sending events in an HTTP request. Each event is sent as its own line in the HTTP request body. If events are too large, you can reduce the size of the events that your APM agents send by: [enabling span compression](../../../solutions/observability/apps/spans.md) or [reducing collected stack trace information](../../../solutions/observability/apps/reduce-storage.md).


### HTTP 401: Invalid token [unauthorized]

The API key is invalid.


## Related troubleshooting resources [observability-apm-troubleshooting-related-troubleshooting-resources]

For additional help with other APM components, see the links below. {{agent}} and each {{apm-agent}} has its own troubleshooting guide:

* [{{fleet}} and {{agent}} troubleshooting](../../../troubleshoot/ingest/fleet/fleet-elastic-agent.md)
* [.NET agent troubleshooting](../../../troubleshoot/observability/apm-agent-dotnet/apm-net-agent.md)
* [Go agent troubleshooting](../../../troubleshoot/observability/apm-agent-go/apm-go-agent.md)
* [Java agent troubleshooting](../../../troubleshoot/observability/apm-agent-java/apm-java-agent.md)
* [Node.js agent troubleshooting](../../../troubleshoot/observability/apm-agent-nodejs/apm-nodejs-agent.md)
* [PHP agent troubleshooting](../../../troubleshoot/observability/apm-agent-php/apm-php-agent.md)
* [Python agent troubleshooting](../../../troubleshoot/observability/apm-agent-python/apm-python-agent.md)
* [Ruby agent troubleshooting](../../../troubleshoot/observability/apm-agent-ruby/apm-ruby-agent.md)


## Elastic Support [observability-apm-troubleshooting-elastic-support]

We offer a support experience unlike any other. Our team of professionals *speak human and code* and love making your day. [Learn more about subscriptions](https://www.elastic.co/subscriptions).
