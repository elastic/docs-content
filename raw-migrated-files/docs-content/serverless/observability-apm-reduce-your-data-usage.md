# Reduce storage [observability-apm-reduce-your-data-usage]

The richness and volume of APM data provides unique insights into your applications, but it can also mean higher costs and more noise when analyzing data. There are a couple strategies you can use to reduce your data usage while continuing to get the full value of APM data.


## Reduce the sample rate [observability-apm-reduce-sample-rate] 

Distributed tracing can generate a substantial amount of data. More data can mean higher costs and more noise. Sampling aims to lower the amount of data ingested and the effort required to analyze that data.

See [Transaction sampling](../../../solutions/observability/apps/transaction-sampling.md) to learn more.


## Enable span compression [_enable_span_compression] 

In some cases, APM agents may collect large amounts of very similar or identical spans in a transaction. These repeated, similar spans often don’t provide added benefit, especially if they are of very short duration. Span compression takes these similar spans and compresses them into a single span-- retaining important information but reducing processing and storage overhead.

See [Span compression](../../../solutions/observability/apps/spans.md) to learn more.


## Reduce collected stack trace information [observability-apm-reduce-stacktrace] 

Elastic APM agents collect `stacktrace` information under certain circumstances. This can be very helpful in identifying issues in your code, but it also comes with an overhead at collection time and increases your storage usage.

Stack trace collection settings are managed in each APM agent. You can enable and disable this feature, or set specific configuration limits, like the maximum number of stacktrace frames to collect, or the minimum duration of a stacktrace to collect.

See the relevant [{{apm-agent}} documentation](https://www.elastic.co/guide/en/apm/agent/index.html) to learn how to customize stacktrace collection.

