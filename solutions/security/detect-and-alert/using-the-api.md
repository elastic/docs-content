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

## API endpoints

The detection APIs are part of the {{kib}} API. For a full operation list, refer to [`endpoint-security-detections-api`]({{kib-apis}}/group/endpoint-security-detections-api) for {{stack}} and [`endpoint-security-detections-api`]({{kib-serverless-apis}}/group/endpoint-security-detections-api) for {{serverless-short}}. Other {{elastic-sec}} endpoints are at [`solutions/security/apis`](/solutions/security/apis.md).

### Detection rules APIs

:::{table}
:widths: 4-4-4

| Function | {{stack}} | {{serverless-full}} |
| --- | --- | --- |
| Creates a new detection rule. | [`detection_engine/rules`]({{kib-apis}}/operation/operation-createrule) | [`detection_engine/rules`]({{kib-serverless-apis}}/operation/operation-createrule) |
| Returns a paginated list of detection rules. | [`detection_engine/rules/_find`]({{kib-apis}}/operation/operation-findrules) | [`detection_engine/rules/_find`]({{kib-serverless-apis}}/operation/operation-findrules) |
| Updates an existing detection rule. | [`detection_engine/rules`]({{kib-apis}}/operation/operation-updaterule) | [`detection_engine/rules`]({{kib-serverless-apis}}/operation/operation-updaterule) |
| Applies bulk edit, duplicate, or delete actions to multiple rules. | [`detection_engine/rules/_bulk_action`]({{kib-apis}}/operation/operation-performrulesbulkaction) | [`detection_engine/rules/_bulk_action`]({{kib-serverless-apis}}/operation/operation-performrulesbulkaction) |
| Imports detection rules from an NDJSON file. | [`detection_engine/rules/_import`]({{kib-apis}}/operation/operation-importrules) | [`detection_engine/rules/_import`]({{kib-serverless-apis}}/operation/operation-importrules) |
| Exports detection rules to NDJSON. | [`detection_engine/rules/_export`]({{kib-apis}}/operation/operation-exportrules) | [`detection_engine/rules/_export`]({{kib-serverless-apis}}/operation/operation-exportrules) |
| Installs and updates Elastic prebuilt detection rules and Timelines. | [`detection_engine/rules/prepackaged`]({{kib-apis}}/operation/operation-installprebuiltrulesandtimelines) | [`detection_engine/rules/prepackaged`]({{kib-serverless-apis}}/operation/operation-installprebuiltrulesandtimelines) |
:::

### Detection alerts APIs

:::{table}
:widths: 4-4-4

| Function | {{stack}} | {{serverless-full}} |
| --- | --- | --- |
| Sets the status of one or more detection alerts. | [`detection_engine/signals/status`]({{kib-apis}}/operation/operation-setalertsstatus) | [`detection_engine/signals/status`]({{kib-serverless-apis}}/operation/operation-setalertsstatus) |
:::

### Exceptions and lists APIs

:::{table}
:widths: 4-4-4

| Function | {{stack}} | {{serverless-full}} |
| --- | --- | --- |
| Manages exception lists and items for detection rules. | [`exception_lists`]({{kib-apis}}/group/endpoint-security-exceptions-api) | [`exception_lists`]({{kib-serverless-apis}}/group/endpoint-security-exceptions-api) |
| Manages Elastic Endpoint rule exception lists and items. | [`endpoint_list`]({{kib-apis}}/group/endpoint-security-endpoint-exceptions-api) | [`endpoint_list`]({{kib-serverless-apis}}/group/endpoint-security-endpoint-exceptions-api) |
| Manages value lists used with detection rule exceptions. | [`lists`]({{kib-apis}}/group/endpoint-security-lists-api) | [`lists`]({{kib-serverless-apis}}/group/endpoint-security-lists-api) |
:::
