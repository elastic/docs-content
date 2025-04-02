---
navigation_title: "Health report pipelines"
mapped_pages:
  - https://www.elastic.co/guide/en/logstash/current/health-report-pipeline-status.html
  - https://www.elastic.co/guide/en/logstash/current/health-report-pipeline-flow-worker-utilization.html
applies_to:
  stack: ga
  serverless: ga
---

# Troubleshoot health report pipelines

This page helps you troubleshoot Logstash health report pipelines.

* [Check health report pipeline status](#health-report-pipeline-status)
* [Check health report pipeline worker utilization](#health-report-pipeline-flow-worker-utilization)

## Check health report pipeline status [health-report-pipeline-status]

The Pipeline indicator has a `status` probe that is capable of producing one of several diagnoses about the pipeline’s lifecycle, indicating whether the pipeline is currently running.

### Loading pipeline [health-report-pipeline-status-diagnosis-loading]

A pipeline that is loading is not yet processing data, and is considered a temporarily-degraded pipeline state. Some plugins perform actions or pre-validation that can delay the starting of the pipeline, such as when a plugin pre-establishes a connection to an external service before allowing the pipeline to start. When these plugins take significant time to start up, the whole pipeline can remain in a loading state for an extended time.

If your pipeline does not come up in a reasonable amount of time, consider checking the Logstash logs to see if the plugin shows evidence of being caught in a retry loop.


### Finished pipeline [health-report-pipeline-status-diagnosis-finished]

A Logstash pipeline whose input plugins have all completed will be shut down once events have finished processing.

Many plugins can be configured to run indefinitely, either by listening for new inbound events or by polling for events on a schedule. A finished pipeline will not produce or process any more events until it is restarted, which will occur if the pipeline’s definition is changed and pipeline reloads are enabled. If you wish to keep your pipeline running, consider configuring its input to run on a schedule or otherwise listen for new events.


### Terminated pipeline [health-report-pipeline-status-diagnosis-terminated]

When a Logstash pipeline’s filter or output plugins crash, the entire pipeline is terminated and intervention is required.

A terminated pipeline will not produce or process any more events until it is restarted, which will occur if the pipeline’s definition is changed and pipeline reloads are enabled. Check the logs to determine the cause of the crash, and report the issue to the plugin maintainers.


### Unknown pipeline [health-report-pipeline-status-diagnosis-unknown]

When a Logstash pipeline either cannot be created or has recently been deleted the health report doesn’t know enough to produce a meaningful status.

Check the logs to determine if the pipeline crashed during creation, and report the issue to the plugin maintainers.


## Check health report pipeline worker utilization [health-report-pipeline-flow-worker-utilization]

The Pipeline indicator has a `flow:worker_utilization` probe that is capable of producing one of several diagnoses about blockages in the pipeline.

A pipeline is considered "blocked" when its workers are fully-utilized, because if they are consistently spending 100% of their time processing events, they are unable to pick up new events from the queue. This can cause back-pressure to cascade to upstream services, which can result in data loss or duplicate processing depending on upstream configuration.

The issue typically stems from one or more causes:

* a downstream resource being blocked,
* a plugin consuming more resources than expected, and/or
* insufficient resources being allocated to the pipeline.

To address the issue, observe the [Plugin flow rates](https://www.elastic.co/guide/en/logstash/current/node-stats-api.html#plugin-flow-rates) from the [Node Stats API](https://www.elastic.co/guide/en/logstash/current/node-stats-api.html), and identify which plugins have the highest `worker_utilization`. This will tell you which plugins are spending the most of the pipeline’s worker resources.

* If the offending plugin connects to a downstream service or another pipeline that is exerting back-pressure, the issue needs to be addressed in the downstream service or pipeline.
* If the offending plugin connects to a downstream service with high network latency, throughput for the pipeline may be improved by [allocating more worker resources to the pipeline](logstash://reference/tuning-logstash.md#tuning-logstash-settings).
* If the offending plugin is a computation-heavy filter such as `grok` or `kv`, its configuration may need to be tuned to eliminate wasted computation.

### Blocked pipeline (5 minutes) [health-report-pipeline-flow-worker-utilization-diagnosis-blocked-5m]

A pipeline that has been completely blocked for five minutes or more represents a critical blockage to the flow of events through your pipeline that needs to be addressed immediately to avoid or limit data loss. See above for troubleshooting steps.


### Nearly blocked pipeline (5 minutes) [health-report-pipeline-flow-worker-utilization-diagnosis-nearly-blocked-5m]

A pipeline that has been nearly blocked for five minutes or more may be creating intermittent blockage to the flow of events through your pipeline, which can result in the risk of data loss. See above for troubleshooting steps.


### Blocked pipeline (1 minute) [health-report-pipeline-flow-worker-utilization-diagnosis-blocked-1m]

A pipeline that has been completely blocked for one minute or more represents a high-risk or upcoming blockage to the flow of events through your pipeline that likely needs to be addressed soon to avoid or limit data loss. See above for troubleshooting steps.


### Nearly blocked pipeline (1 minute) [health-report-pipeline-flow-worker-utilization-diagnosis-nearly-blocked-1m]

A pipeline that has been nearly blocked for one minute or more may be creating intermittent blockage to the flow of events through your pipeline, which can result in the risk of data loss. See above for troubleshooting steps.
