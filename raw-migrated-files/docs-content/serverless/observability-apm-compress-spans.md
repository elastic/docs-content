# Span compression [observability-apm-compress-spans]

In some cases, APM agents may collect large amounts of very similar or identical spans in a transaction. For example, this can happen if spans are captured inside a loop or in unoptimized SQL queries that use multiple queries instead of joins to fetch related data.

In such cases, the upper limit of spans per transaction (by default, 500 spans) can be reached quickly, causing the agent to stop capturing potentially more relevant spans for a given transaction.

Capturing similar or identical spans often isn’t helpful, especially if they are of very short duration. They can also clutter the UI, and cause processing and storage overhead.

To address this problem, APM agents can compress similar spans into a single span. The compressed span retains most of the original span information, including the overall duration and number of spans it represents.

Regardless of the compression strategy, a span is eligible for compression if:

* It has not propagated its trace context.
* It is an *exit* span (such as database query spans).
* Its outcome is not `"failure"`.


## Compression strategies [observability-apm-compress-spans-compression-strategies]

The {{apm-agent}} selects between two strategies to decide if adjacent spans can be compressed. In both strategies, only one previous span needs to be kept in memory. This ensures that the agent doesn’t require large amounts of memory to enable span compression.


### Same-Kind strategy [observability-apm-compress-spans-same-kind-strategy]

The agent uses the same-kind strategy if two adjacent spans have the same:

* span type
* span subtype
* `destination.service.resource` (e.g. database name)


### Exact-Match strategy [observability-apm-compress-spans-exact-match-strategy]

The agent uses the exact-match strategy if two adjacent spans have the same:

* span name
* span type
* span subtype
* `destination.service.resource` (e.g. database name)


## Settings [observability-apm-compress-spans-settings]

You can specify the maximum span duration in the agent’s configuration settings. Spans with a duration longer than the specified value will not be compressed.

For the "Same-Kind" strategy, the default maximum span duration is 0 milliseconds, which means that the "Same-Kind" strategy is disabled by default. For the "Exact-Match" strategy, the default limit is 50 milliseconds.


### Agent support [observability-apm-compress-spans-agent-support]

Support for span compression is available in the following agents and can be configured using the options listed below:

| Agent | Same-kind config | Exact-match config |
| --- | --- | --- |
| **Go agent** | [`ELASTIC_APM_SPAN_COMPRESSION_SAME_KIND_MAX_DURATION`](https://www.elastic.co/guide/en/apm/agent/go/{{apm-go-branch}}/configuration.html#config-span-compression-same-kind-duration) | [`ELASTIC_APM_SPAN_COMPRESSION_EXACT_MATCH_MAX_DURATION`](https://www.elastic.co/guide/en/apm/agent/go/{{apm-go-branch}}/configuration.html#config-span-compression-exact-match-duration) |
| **Java agent** | [`span_compression_same_kind_max_duration`](https://www.elastic.co/guide/en/apm/agent/java/{{apm-java-branch}}/config-huge-traces.html#config-span-compression-same-kind-max-duration) | [`span_compression_exact_match_max_duration`](https://www.elastic.co/guide/en/apm/agent/java/{{apm-java-branch}}/config-huge-traces.html#config-span-compression-exact-match-max-duration) |
| **.NET agent** | [`SpanCompressionSameKindMaxDuration`](https://www.elastic.co/guide/en/apm/agent/dotnet/{{apm-dotnet-branch}}/config-core.html#config-span-compression-same-kind-max-duration) | [`SpanCompressionExactMatchMaxDuration`](https://www.elastic.co/guide/en/apm/agent/dotnet/{{apm-dotnet-branch}}/config-core.html#config-span-compression-exact-match-max-duration) |
| **Node.js agent** | [`spanCompressionSameKindMaxDuration`](https://www.elastic.co/guide/en/apm/agent/nodejs/{{apm-node-branch}}/configuration.html#span-compression-same-kind-max-duration) | [`spanCompressionExactMatchMaxDuration`](https://www.elastic.co/guide/en/apm/agent/nodejs/{{apm-node-branch}}/configuration.html#span-compression-exact-match-max-duration) |
| **Python agent** | [`span_compression_same_kind_max_duration`](https://www.elastic.co/guide/en/apm/agent/python/{{apm-py-branch}}/configuration.html#config-span-compression-same-kind-max-duration) | [`span_compression_exact_match_max_duration`](https://www.elastic.co/guide/en/apm/agent/python/{{apm-py-branch}}/configuration.html#config-span-compression-exact-match-max_duration) |
