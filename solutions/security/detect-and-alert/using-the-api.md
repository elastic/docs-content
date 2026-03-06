---
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Create and manage detection rules programmatically using the Security detections API for CI/CD and bulk operations.
---

# Using the API

You can create and manage detection rules programmatically instead of using the {{kib}} UI. This is useful for CI/CD pipelines, bulk rule management, rule-as-code workflows, and integrating detection management with external tooling.

:::{admonition} Create rules using the UI
If you prefer to use the UI for creating rules, refer to [Using the UI](/solutions/security/detect-and-alert/using-the-rule-builder.md).
:::

::::{important}

Rules run in the background using the privileges of the user who last edited them. When you create or modify a rule, {{elastic-sec}} generates an [API key](/deploy-manage/api-keys/elasticsearch-api-keys.md) that captures a snapshot of your current privileges. If a user without the required privileges (such as index read access) updates a rule, the rule can stop functioning correctly and no longer generate alerts. To fix this, a user with the right privileges to either modify the rule or update the API key. To learn more, refer to [](/solutions/security/detect-and-alert/detection-rule-concepts.md#rule-authorization-concept).

::::

## API reference

The detection APIs are part of the {{kib}} API. Use the appropriate reference for your deployment type:

**{{stack}}**
:   [Security detections API]({{kib-apis}}/group/endpoint-security-detections-api): Create, read, update, delete, and bulk-manage detection rules. Also covers alert management (status, tags, assignees) and prebuilt rule installation. For a complete list of {{elastic-sec}} APIs, refer to [{{elastic-sec}} APIs](/solutions/security/apis.md).

**{{serverless-full}}**
:   [Security detections API (Serverless)]({{kib-serverless-apis}}/group/endpoint-security-detections-api): The same detection operations, scoped to {{serverless-short}} projects.

## Common operations

| Task | {{stack}} | {{serverless-full}} |
|---|---|---|
| Create a rule | [Stack]({{kib-apis}}/operation/operation-createrule) | [Serverless]({{kib-serverless-apis}}/operation/operation-createrule) |
| List all rules | [Stack]({{kib-apis}}/operation/operation-findrules) | [Serverless]({{kib-serverless-apis}}/operation/operation-findrules) |
| Update a rule | [Stack]({{kib-apis}}/operation/operation-updaterule) | [Serverless]({{kib-serverless-apis}}/operation/operation-updaterule) |
| Bulk actions | [Stack]({{kib-apis}}/operation/operation-performrulesbulkaction) | [Serverless]({{kib-serverless-apis}}/operation/operation-performrulesbulkaction) |
| Import rules | [Stack]({{kib-apis}}/operation/operation-importrules) | [Serverless]({{kib-serverless-apis}}/operation/operation-importrules) |
| Export rules | [Stack]({{kib-apis}}/operation/operation-exportrules) | [Serverless]({{kib-serverless-apis}}/operation/operation-exportrules) |
| Install prebuilt rules | [Stack]({{kib-apis}}/operation/operation-installprebuiltrulesandtimelines) | [Serverless]({{kib-serverless-apis}}/operation/operation-installprebuiltrulesandtimelines) |
| Set alert status | [Stack]({{kib-apis}}/operation/operation-setalertsstatus) | [Serverless]({{kib-serverless-apis}}/operation/operation-setalertsstatus) |
| Manage rule exceptions | [Stack]({{kib-apis}}/group/endpoint-security-exceptions-api) | [Serverless]({{kib-serverless-apis}}/group/endpoint-security-exceptions-api) |
| Manage endpoint exceptions | [Stack]({{kib-apis}}/group/endpoint-security-endpoint-exceptions-api) | [Serverless]({{kib-serverless-apis}}/group/endpoint-security-endpoint-exceptions-api) |
| Manage value lists | [Stack]({{kib-apis}}/group/endpoint-security-lists-api) | [Serverless]({{kib-serverless-apis}}/group/endpoint-security-lists-api) |