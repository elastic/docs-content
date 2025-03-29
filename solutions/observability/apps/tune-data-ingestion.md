---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-tune-data-ingestion.html
applies_to:
  stack: all
---

# Tune data ingestion [apm-tune-data-ingestion]

This section explains how to adapt data ingestion according to your needs.


## Tune APM Server [apm-tune-apm-server]

* [Add APM Server or {{agent}} instances](#apm-add-apm-server-instances)
* [Reduce the payload size](#apm-reduce-payload-size)
* [Adjust anonymous auth rate limit](#apm-adjust-event-rate)


### Add APM Server or {{agent}} instances [apm-add-apm-server-instances]

If the APM Server cannot process data quickly enough, you will see request timeouts. One way to solve this problem is to increase processing power.

Increase processing power by either migrating to a more powerful machine or adding more APM Server/Elastic Agent instances. Having several instances will also increase [availability](high-availability.md).


### Reduce the payload size [apm-reduce-payload-size]

Large payloads may result in request timeouts. You can reduce the payload size by decreasing the flush interval in the agents. This will cause agents to send smaller and more frequent requests.

Optionally you can also [reduce the sample rate](reduce-storage.md#apm-reduce-sample-rate) or [reduce the amount of stack traces](reduce-storage.md#observability-apm-reduce-stacktrace).

Read more in the [agents documentation](https://www.elastic.co/guide/en/apm/agent/index.html).


### Adjust anonymous auth rate limit [apm-adjust-event-rate]

Agents make use of long running requests and flush as many events over a single request as possible. Thus, the rate limiter for anonymous authentication is bound to the number of *events* sent per second, per IP.

If the event rate limit is hit while events on an established request are sent, the request is not immediately terminated. The intake of events is only throttled to anonymous event rate limit, which means that events are queued and processed slower. Only when the allowed buffer queue is also full, does the request get terminated with a `429 - rate limit exceeded` HTTP response. If an agent tries to establish a new request, but the rate limit is already hit, a `429` will be sent immediately.

Increasing the default value for the following configuration variable will help avoid `rate limit exceeded` errors:

|     |     |
| --- | --- |
| APM Server binary | [`rate_limit.event_limit`](configure-anonymous-authentication.md#apm-config-auth-anon-event-limit) |
| Fleet-managed | `Anonymous Event rate limit (event limit)` |


## Tune {{es}} [apm-tune-elasticsearch]

The {{es}} Reference provides insight on tuning {{es}}.

[Tune for indexing speed](../../../deploy-manage/production-guidance/optimize-performance/indexing-speed.md) provides information on:

* Refresh interval
* Disabling swapping
* Optimizing file system cache
* Considerations regarding faster hardware
* Setting the indexing buffer size

[Tune for disk usage](../../../deploy-manage/production-guidance/optimize-performance/disk-usage.md) provides information on:

* Disabling unneeded features
* Shard size
* Shrink index

