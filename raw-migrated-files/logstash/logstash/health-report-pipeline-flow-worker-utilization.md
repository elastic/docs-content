# Health Report Pipeline Flow: Worker Utilization [health-report-pipeline-flow-worker-utilization]

The Pipeline indicator has a `flow:worker_utilization` probe that is capable of producing one of several diagnoses about blockages in the pipeline.

A pipeline is considered "blocked" when its workers are fully-utilized, because if they are consistently spending 100% of their time processing events, they are unable to pick up new events from the queue. This can cause back-pressure to cascade to upstream services, which can result in data loss or duplicate processing depending on upstream configuration.

The issue typically stems from one or more causes:

* a downstream resource being blocked,
* a plugin consuming more resources than expected, and/or
* insufficient resources being allocated to the pipeline.

To address the issue, observe the [Plugin flow rates](https://www.elastic.co/guide/en/logstash/current/node-stats-api.html#plugin-flow-rates) from the [Node Stats API](https://www.elastic.co/guide/en/logstash/current/node-stats-api.html), and identify which plugins have the highest `worker_utilization`. This will tell you which plugins are spending the most of the pipeline’s worker resources.

* If the offending plugin connects to a downstream service or another pipeline that is exerting back-pressure, the issue needs to be addressed in the downstream service or pipeline.
* If the offending plugin connects to a downstream service with high network latency, throughput for the pipeline may be improved by [allocating more worker resources to the pipeline](asciidocalypse://docs/logstash/docs/reference/ingestion-tools/logstash/tuning-logstash.md#tuning-logstash-settings).
* If the offending plugin is a computation-heavy filter such as `grok` or `kv`, its configuration may need to be tuned to eliminate wasted computation.

## $$$blocked-5m$$$Blocked Pipeline (5 minutes) [health-report-pipeline-flow-worker-utilization-diagnosis-blocked-5m]

A pipeline that has been completely blocked for five minutes or more represents a critical blockage to the flow of events through your pipeline that needs to be addressed immediately to avoid or limit data loss. See above for troubleshooting steps.


## $$$nearly-blocked-5m$$$Nearly Blocked Pipeline (5 minutes) [health-report-pipeline-flow-worker-utilization-diagnosis-nearly-blocked-5m]

A pipeline that has been nearly blocked for five minutes or more may be creating intermittent blockage to the flow of events through your pipeline, which can result in the risk of data loss. See above for troubleshooting steps.


## $$$blocked-1m$$$Blocked Pipeline (1 minute) [health-report-pipeline-flow-worker-utilization-diagnosis-blocked-1m]

A pipeline that has been completely blocked for one minute or more represents a high-risk or upcoming blockage to the flow of events through your pipeline that likely needs to be addressed soon to avoid or limit data loss. See above for troubleshooting steps.


## $$$nearly-blocked-1m$$$Nearly Blocked Pipeline (1 minute) [health-report-pipeline-flow-worker-utilization-diagnosis-nearly-blocked-1m]

A pipeline that has been nearly blocked for one minute or more may be creating intermittent blockage to the flow of events through your pipeline, which can result in the risk of data loss. See above for troubleshooting steps.


