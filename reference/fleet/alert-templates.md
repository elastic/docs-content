---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/data-streams.html
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
The built-in alerts feature for {{agent}} is available only for some subscription levels. The license (or a trial license) must be in place before you install or upgrade {{agent}} before this feature is available. 

Refer [Elastic subscriptions](https://www.elastic.co/subscriptions) for more information. 
::::

In {{kib}}, you can enable out-of-the-box rules pre-configured with reasonable defaults to provide immediate value for managing agents.
You can use [ES|QL](/explore-analyze/discover/try-esql.md) to author conditions for each rule.

Connectors are not added to rules automatically, but you can attach a connector to route alerts to your platform of choice -- Slack or email, for example.
In addition, you can add filters for policies, tags, or hostnames to scope alerts to specific sets of agents  

You can find these rules in **Stack Management** > **Alerts and Insights** > **Rules**.


## Alert templates assets for integrations [alert-templates]

Some integration packages include alerting rule template assets that provide pre-made definitions of alerting rules. You can use the templates to create your own custom alerting rules that you can enable and fine tune. 

When you click a template, you get a pre-filled rule creation form. You can define and adjust values, set up connectors, and define rule actions to create your custom alerting rule.

You can see available templates in the **integrations/detail/<package>/assets** view. 
