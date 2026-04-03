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
If you prefer to use the UI for creating rules, refer to [Using the UI](/solutions/security/detect-and-alert/using-the-rule-ui.md).
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
| Create a rule | [`POST /api/detection_engine/rules`]({{kib-apis}}/operation/operation-createrule) | [`POST /api/detection_engine/rules`]({{kib-serverless-apis}}/operation/operation-createrule) |
| List all rules | [`GET /api/detection_engine/rules/_find`]({{kib-apis}}/operation/operation-findrules) | [`GET /api/detection_engine/rules/_find`]({{kib-serverless-apis}}/operation/operation-findrules) |
| Update a rule | [`PUT /api/detection_engine/rules`]({{kib-apis}}/operation/operation-updaterule) | [`PUT /api/detection_engine/rules`]({{kib-serverless-apis}}/operation/operation-updaterule) |
| Bulk actions | [`POST /api/detection_engine/rules/_bulk_action`]({{kib-apis}}/operation/operation-performrulesbulkaction) | [`POST /api/detection_engine/rules/_bulk_action`]({{kib-serverless-apis}}/operation/operation-performrulesbulkaction) |
| Import rules | [`POST /api/detection_engine/rules/_import`]({{kib-apis}}/operation/operation-importrules) | [`POST /api/detection_engine/rules/_import`]({{kib-serverless-apis}}/operation/operation-importrules) |
| Export rules | [`POST /api/detection_engine/rules/_export`]({{kib-apis}}/operation/operation-exportrules) | [`POST /api/detection_engine/rules/_export`]({{kib-serverless-apis}}/operation/operation-exportrules) |
| Install prebuilt rules | [`PUT /api/detection_engine/rules/prepackaged`]({{kib-apis}}/operation/operation-installprebuiltrulesandtimelines) | [`PUT /api/detection_engine/rules/prepackaged`]({{kib-serverless-apis}}/operation/operation-installprebuiltrulesandtimelines) |
| Set alert status | [`POST /api/detection_engine/signals/status`]({{kib-apis}}/operation/operation-setalertsstatus) | [`POST /api/detection_engine/signals/status`]({{kib-serverless-apis}}/operation/operation-setalertsstatus) |
| Manage rule exceptions | [`POST /api/exception_lists`]({{kib-apis}}/group/endpoint-security-exceptions-api) | [`POST /api/exception_lists`]({{kib-serverless-apis}}/group/endpoint-security-exceptions-api) |
| Manage endpoint exceptions | [`POST /api/endpoint_list`]({{kib-apis}}/group/endpoint-security-endpoint-exceptions-api) | [`POST /api/endpoint_list`]({{kib-serverless-apis}}/group/endpoint-security-endpoint-exceptions-api) |
| Manage value lists | [`POST /api/lists`]({{kib-apis}}/group/endpoint-security-lists-api) | [`POST /api/lists`]({{kib-serverless-apis}}/group/endpoint-security-lists-api) |