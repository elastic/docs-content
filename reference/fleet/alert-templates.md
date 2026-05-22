---
applies_to:
  stack: ga 9.2
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
navigation_title: Elastic Agent built-in alerts
---

# Elastic Agent built-in alerts [built-in-alerts]

## {{agent}} out-of-the-box alert rules [ea-alert-rules]

When you install or upgrade {{agent}}, new alert rules are created automatically. You can configure and customize out-of-the-box alerts to get them up and running quickly. 

::::{note}
The built-in alerts feature for {{agent}} is available only for some subscription levels. The license (or a trial license) must be in place _before_ you install or upgrade {{agent}} for the alert rules to be available. 

Refer to [Elastic subscriptions](https://www.elastic.co/subscriptions) for more information. 
::::

In {{kib}}, you can enable out-of-the-box rules pre-configured with reasonable defaults to provide immediate value for managing agents.
You can use [{{esql}}](/explore-analyze/discover/try-esql.md) to author conditions for each rule.

Search for **Alerts and Insights** to find available **Rules**. 
If you don't see out-of-the-box alert rules, check your [Elastic subscriptions](https://www.elastic.co/subscription). 

### Available alert rules [available-alert-rules]

| Alert | Description |
| -------- | -------- |
| [Elastic Agent] CPU usage spike|  Checks if the agent or any of its processes were pegged at a high CPU for a specified window of time. This could signal a bug in an application and warrant further investigation.<br> - Condition: Alert on `system.process.cpu.total.norm.pct` of 80% or more<br>- Default: Disabled |
| [Elastic Agent] Dropped events | Checks ratio of dropped events to acknowledged events. Rows are distinguished by agent ID and component ID. <br> - Condition: Alert on ratio of dropped events to acknowledged events of 5% or more<br>- Default: Disabled|
| [Elastic Agent] Excessive memory usage|  Checks if the agent or any of its processes have a high memory usage or memory usage that is trending up. This could signal a memory leak in an application and warrant further investigation.<br>- Condition: Alert on `system.process.memory.rss.pct` exceeding 50%<br>- Default: Disabled |
| [Elastic Agent] Excessive restarts| Checks for excessive restarts on a host. Some restarts can have a business impact, and getting alerts for them can enable timely mitigation.<br>- Condition: Alert on 11 or more restarts in a 5-minute window<br>- Default: Disabled |
| [Elastic Agent] High pipeline queue | Checks percentage of pipeline queue. Rows are distinguished by agent ID and component ID. <br> - Condition: Alert on max of `beat.stats.libbeat.pipeline.queue.filled.pct` exceeding 90%  <br>- Default: Disabled|
| [Elastic Agent] Offline status | Checks for any agents that are offline. <br> - Condition: Alert when agent has been offline for longer than the time set in `inactivity timeout` <br>- Default: Disabled|
| [Elastic Agent] Output errors | Checks errors per minute from an agent component. Rows are distinguished by agent ID and component ID. <br> - Condition: Alert on 6 or more errors per minute  <br>- Default: Disabled|
| [Elastic Agent] Unenrolled status | Checks for agents that have been manually unenrolled. <br> - Condition: Alert on agent that has been removed from {{fleet}} and whose API keys have been revoked <br>- Default: Disabled|
| [Elastic Agent] Unhealthy status | Checks agent status. An `unhealthy` status can indicate errors or degraded functionality of the agent. <br> - Condition: Alert on `unhealthy` status <br>- Default: Disabled|
| [Elastic Agent] Uninstalled status | Checks for agents that have been uninstalled. <br> - Condition: Alert when agents have been uninstalled and removed from the host system <br>- Default: Disabled|

**Connectors** are not added to rules automatically, but you can attach a connector to route alerts to your Slack, email, or other notification platforms.
In addition, you can add filters for policies, tags, or hostnames to scope alerts to specific sets of agents.  
