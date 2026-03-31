---
navigation_title: Set rule data sources
applies_to:
  serverless: preview
products:
  - id: kibana
description: "Configure Kibana alerting v2 rule data sources using ES|QL FROM commands, including index patterns, cross-cluster search, and alert indices."
---

# Set Kibana alerting v2 rule data sources [set-rule-data-sources-v2]

Every Kibana alerting v2 rule evaluates data from one or more {{es}} indices. The data source is defined by the `FROM` command in the rule's ES|QL query.
