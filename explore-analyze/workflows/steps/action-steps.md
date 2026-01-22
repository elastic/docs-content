---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about action steps that perform tasks in your workflows.
---

# Action steps

Action steps are the building blocks that perform tasks in your workflows. They are the operations that do the work, such as searching data, calling an API, sending a notification, or interacting with external systems.

Action steps are organized into the following categories.

## {{es}}

{{es}} actions provide native integration with {{es}} APIs. These actions are automatically authenticated and offer a simplified interface for common operations. Use {{es}} actions to:

* Search and query data
* Index new documents
* Update or delete existing documents
* Manage indices and data streams

Refer to [](/explore-analyze/workflows/steps/elasticsearch.md) for more information.

## {{kib}}

{{kib}} actions provide native integration with {{kib}} APIs. Like {{es}} actions, they are automatically authenticated and simplify common operations. Use {{kib}} actions to:

* Create or update cases
* Manage alerts
* Interact with saved objects
* Work with other {{kib}} features

Refer to [](/explore-analyze/workflows/steps/kibana.md) for more information.

## External systems and apps

External actions allow your workflows to communicate with third-party systems using connectors. Use external actions to:

* Send notifications to Slack or email
* Create incidents in ServiceNow
* Create issues in Jira
* Call any external API using HTTP

Refer to [](/explore-analyze/workflows/steps/external-systems-apps.md) for more information.
