---
applies_to:
  stack: ga 9.2
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
navigation_title: Built-in alerts and templates
---

# Built-in alerts and templates [built-in-alerts]

## {{agent}} out-of-the-box alert rules [ea-alert-rules]

When you install or upgrade {{agent}}, new alert rules are created automatically. You can configure and customize out-of-the-box alerts to get them up and running quickly. 

::::{note}
The built-in alerts feature for {{agent}} is available only for some subscription levels. The license (or a trial license) must be in place _before_ you install or upgrade {{agent}} for the alert rules to be available. 

Refer to [Elastic subscriptions](https://www.elastic.co/subscriptions) for more information. 
::::

In {{kib}}, you can enable out-of-the-box rules pre-configured with reasonable defaults to provide immediate value for managing agents.
You can use [{{esql}}](/explore-analyze/discover/try-esql.md) to author conditions for each rule.

You can find these rules in **Stack Management** > **Alerts and Insights** > **Rules**.

### Available alert rules [available-alert-rules]

| Alert | Description |
| -------- | -------- |
| [Elastic Agent] CPU usage spike|  Checks if {{agent}} or any of its processes were pegged at a high CPU for a specified window of time. This could signal a bug in an application and warrant further investigation.<br> - Condition: `system.process.cpu.total.time.ms` > 80% for 5 minutes<br>- Default: Enabled |
| [Elastic Agent] Dropped events | Checks if the percentage of dropped events to acked events from the pipeline is greater than or equal to 5%. Rows are distinguished by agent ID and component ID. |
| [Elastic Agent] Excessive memory usage|  Checks if {{agent}} or any of its processes have a high memory usage or memory usage that is trending higher. This could signal a memory leak in an application and warrant further investigation.<br>- Condition: Alert on `system.process.memory.rss.pct` > 50%<br>- Default: Enabled |
| [Elastic Agent] Excessive restarts| Checks for excessive restarts on a host which require further investigation. Some restarts can have a business impact and getting alerts for them can enable timely mitigation.<br>- Condition: Alert on restarts > 10 restarts in a 5 minute window<br>- Default: Enabled |
| [Elastic Agent] High pipeline queue | Checks if max of `beat.stats.libbeat.pipeline.queue.filled.pct` exceeds 90%. Rows are distinguished by agent ID and component ID. |
| [Elastic Agent] Output errors | Checks if errors per minute from an agent component is greater than 5. Rows are distinguished by agent ID and component ID. |
| [Elastic Agent] Unhealthy status | Checks logs for an agent status change to `error` using the new `elastic_agent.status_change` datastreams. |

**Connectors** are not added to rules automatically, but you can attach a connector to route alerts to your Slack, email, or other notification platforms.
In addition, you can add filters for policies, tags, or hostnames to scope alerts to specific sets of agents.  

## Alert template assets for integrations [alert-templates]

Some integration packages include alerting rule template assets that provide pre-made definitions of alerting rules. You can use the templates to create your own custom alerting rules that you can enable and fine-tune. 

When you click a template, you get a pre-filled rule creation form. You can define and adjust values, set up connectors, and define rule actions to create your custom alerting rule.

You can see available templates in the **integrations/detail/<package>/assets** view. 
