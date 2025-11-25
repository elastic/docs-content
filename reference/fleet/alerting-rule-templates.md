---
applies_to:
  stack: ga 9.3
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
navigation_title: Alerting rule templates
---

# Alerting Rule Templates [alerting-rule-templates]

Alerting rule templates are out-of-the-box, preconfigured rule definitions maintained by Elastic integration authors. They help you start monitoring in minutes—no queries to write, no thresholds to figure out—by providing curated {{esql}} queries, sensible defaults, and recommended thresholds tailored to each integration. Templates are available from an integration’s Assets and open a prefilled rule creation form you can adjust and enable.

## Prerequisites
	
- Install or upgrade to the latest version of the integration that includes alerting rule templates.
- Ensure the relevant data stream is enabled and ingesting data for the template you plan to use.
- {{stack}} 9.2.1 or later.
- Appropriate {{kib}} role privileges to create and manage rules in the current space.

## How to use the Alerting Rule Templates

Alerting rule templates come with recommended, pre-populated values. To use them:

1. In {{kib}}, go to **{{manage-app}}** > **{{integrations}}**.
1. Find and open the integration.
1. On the integration page, open the **Assets** tab and expand **Alerting rule templates** to view all available templates for that integration.
1. Select a template to open a prefilled Create rule form.
1. Review and (optionally) customize the prefilled settings, then save and enable the rule.

When you click a template, you get a prefilled **Create Rules** form. You can use the template to create your own custom alerting rule by adjusting values, setting up connectors, and defining rule actions.

The preconfigured defaults typically include:

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


