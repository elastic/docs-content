---
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Start with pre-configured rule templates for common monitoring patterns and install pre-built detection rules."
---

% Content will be updated when template UI is implemented.

# Kibana alerting v2 rule templates [rule-templates-v2]

Rule templates provide pre-configured starting points for common monitoring patterns. Instead of writing a rule from scratch, you can start with a template that includes opinionated defaults for the ES|QL query, schedule, grouping, and thresholds, then customize it for your environment.

## How templates work

1. Navigate to the rule creation form and select **Create from template**.
2. Browse available templates, filtered by category, data source, or tag.
3. Select a template to pre-populate the rule form with its defaults.
4. Customize the query, schedule, grouping, and other settings as needed.
5. Save the rule.

Templates are a starting point, not a constraint. After you create a rule from a template, it becomes an independent rule that you can edit freely.

## Template categories

Templates are organized by use case:

- **Infrastructure monitoring** — CPU, memory, disk, and network thresholds per host or container.
- **Application performance** — latency percentiles, error rates, and throughput by service.
- **Log analysis** — error pattern detection, log volume anomalies, and specific error string matching.
- **Availability** — no-data detection for hosts, services, and data sources.
- **SLO** — burn rate calculations for service-level objectives.

## Pre-built rule library

In addition to templates, the pre-built rule library offers fully configured detection rules that you can install and enable with a single action. Pre-built rules are maintained by Elastic and updated through rule packages.

To install pre-built rules:

1. Click **Install pre-built rules** from the rules list.
2. Browse available rules with tags, severity, data source, and installation status, sorted by relevance to your stack.
3. Filter by rule attributes.
4. Select a rule and review its details in a flyout.
5. Click **Install and enable**.

The rule starts generating alert events immediately. Review results in Discover or the alerts table.
