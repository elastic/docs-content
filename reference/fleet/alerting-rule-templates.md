---
applies_to:
  stack: ga 9.2.1
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
navigation_title: Alerting rule templates
---

# Alerting Rule Templates [alerting-rule-templates]

Alerting rule templates are out-of-the-box alert definitions that come bundled with Elastic integrations, enabling users to quickly set up monitoring without writing queries from scratch. 

Templates help you start monitoring in minutes by providing curated {{esql}} queries and recommended thresholds tailored to each integration. 

Once the integration is installed, these templates are automatically available in Kibana's alerting interface with a prefilled rule creation form that you can tailor to your needs.

:::{important}
Although the alerts can be used as provided, threshold values should always be evaluated in the context of your specific environment. Applying the predefined thresholds without adjustment may result in an excessive number of alerts.
:::

## Prerequisites
	
- Install or upgrade to the latest version of the integration that includes alerting rule templates.
- Ensure the relevant data stream is enabled and ingesting data for the template you plan to use.
- {{stack}} 9.2.1 or later.
- Appropriate {{kib}} role privileges to create and manage rules.

## How to use the Alerting rule templates

Alerting rule templates come with recommended, pre-populated values. To use them:

1. In {{kib}}, go to **{{manage-app}}** > **{{integrations}}**.
1. Find and open the integration.
1. On the integration page, open the **Assets** tab and expand **Alerting rule templates** to view all available templates for that integration.

    :::{note}
    You can find the Alerting rule template option only when the integration adds template support for alerting rules.
    :::

1. Select a template to open a prefilled **Create rule** form.

    You can use the template to create your own custom alerting rule by adjusting values, setting up connectors, and defining rule actions.

1. Review and (optionally) customize the prefilled settings, then save and enable the rule.

   The rule created from the template gets listed in the **Observability** → **Alerts** → **Manage Rules** page.

To update the rule you have created from the template, go to **Observability** → **Alerts** → **Manage Rules**, select the rule and click **Actions**.

The preconfigured defaults include:

- **{{esql}} query**
:   A curated, text-based query that evaluates your data and triggers when matches are found during the latest run.
- **Recommended threshold**
:   A suggested threshold embedded in the {{esql}} `WHERE` clause. You can tune the threshold to fit your environment.
- **Time window (look-back)**
:   The length of time the rule analyzes for data (for example, the last 5 minutes).
- **Rule schedule**
:   How frequently the rule checks alert conditions (for example, every minute).
- **Alert delay (alert suppression)**
:   The number of consecutive runs for which conditions must be met before an alert is created.

For details about fields in the Create rule form and how the rule evaluates data, refer to the [{{es}} query rule type](/explore-analyze/alerts-cases/alerts/rule-type-es-query.md).


