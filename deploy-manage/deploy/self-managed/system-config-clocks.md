---
description: Keep system clocks synchronized and free from large discontinuities.
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Synchronize system clocks [system-config-clocks]

{{es}} relies on the system clock of each node for many time-dependent operations. This includes:

* Timestamps recorded during ingest
* Searches that use `now` (see [date math](elasticsearch://reference/elasticsearch/rest-apis/common-options.md#date-math))
* Scheduled activities
* Security features such as API key and token expiry, JWT and SAML time validation, and TLS certificate validity
* Timestamped log messages
* Certain cache invalidation events

Keep the clocks on all nodes in the cluster synchronized with real time, and avoid discontinuities in these clocks in which the clock time jumps forwards or backwards by a large amount. Run a time synchronization service such as [NTP](http://www.ntp.org/) or Chrony on every host.

A properly-configured time synchronization service typically keeps clocks synchronized to within at most a few milliseconds. A few seconds of clock skew between nodes can cause some confusing effects, but {{es}} otherwise operates normally under these conditions. A skew or discontinuity of over ten seconds can cause unexpected or inefficient behavior.

{{es}} does not rely on clock synchronization for any safety guarantees. For instance, if {{es}} acknowledges a write operation, then this operation is guaranteed to be durable regardless of any clock skew or discontinuity.

## Related pages

* [Schedule trigger](/explore-analyze/alerting/watcher/trigger-schedule.md): How {{watcher}} uses the system clock for schedules
* [{{kib}} task management](/deploy-manage/distributed-architecture/kibana-tasks-management.md): Clock synchronization for {{kib}} scheduled tasks
