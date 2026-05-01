---
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Learn about action steps that perform tasks in your workflows.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Action steps

Action steps are the building blocks that perform tasks in your workflows. They are the operations that do the work, such as searching data, calling an API, managing cases, or interacting with external systems.

Action steps are organized into the following categories.

## {{es}}

{{es}} actions provide native integration with {{es}} APIs. These actions are automatically authenticated and offer a simplified interface for common operations. Use {{es}} actions to:

* Search and query data
* Index new documents
* Update or delete existing documents
* Manage indices and data streams

Refer to [](/explore-analyze/workflows/steps/elasticsearch.md) for more information.

## {{kib}}

{{kib}} actions provide native integration with {{kib}} APIs. Like {{es}} actions, they're automatically authenticated. Use {{kib}} actions to:

* Change detection alert status or tags (`kibana.SetAlertsStatus`, `kibana.SetAlertTags`)
* Call any {{kib}} API through the `kibana.request` step

Refer to [](/explore-analyze/workflows/steps/kibana.md) for more information.

## Cases

Cases actions provide 27 step types for creating, querying, updating, and managing the lifecycle of cases in {{elastic-sec}} and other Cases-enabled apps. Use Cases actions to:

* Create cases with a full schema or from a template
* Attach alerts, events, observables, and comments
* Assign, tag, categorize, and close cases
* Find cases by criteria or similarity

Refer to [](/explore-analyze/workflows/steps/cases.md) for the complete 27-step catalog.

## Streams

```{applies_to}
stack: preview 9.4+
serverless: preview
```

Streams actions let workflows operate on Observability Streams. Use Streams actions to:

* List available streams
* Fetch a specific stream
* Pull significant events from a stream's time window

Refer to [](/explore-analyze/workflows/steps/streams.md) for more information.

## External systems and apps

External actions let workflows communicate with third-party systems using [connectors](kibana:/reference/connectors-kibana.md). Use external actions to:

* Send notifications to Slack or email
* Create incidents in ServiceNow
* Create issues in Jira
* Call any external API using HTTP requests

Refer to [](/explore-analyze/workflows/steps/external-systems-apps.md) for more information.
