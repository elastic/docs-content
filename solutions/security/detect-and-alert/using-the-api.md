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

## API reference

The detection APIs are part of the {{kib}} API. Use the appropriate reference for your deployment type:

**{{stack}}**
:   [Security detections API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-security-detections-api): Create, read, update, delete, and bulk-manage detection rules. Also covers alert management (status, tags, assignees) and prebuilt rule installation.

**{{serverless-full}}**
:   [Security detections API (Serverless)](https://www.elastic.co/docs/api/doc/kibana-serverless/group/endpoint-security-detections-api): The same detection operations, scoped to {{serverless-short}} projects.

For rule exceptions and value lists, use these additional APIs:

- [Exceptions API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-security-exceptions-api): Create and manage rule exceptions and shared exception lists.
- [Endpoint exceptions API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-security-endpoint-exceptions-api): Manage endpoint-specific exceptions.
- [Lists API](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-security-lists-api): Create source event value lists for use with rule exceptions.

For a complete list of {{elastic-sec}} APIs, refer to [{{elastic-sec}} APIs](/solutions/security/apis.md).

## Common operations

| Task | Endpoint |
|---|---|
| Create a rule | [`POST /api/detection_engine/rules`](https://www.elastic.co/docs/api/doc/kibana/operation/operation-createrule) |
| List all rules | [`GET /api/detection_engine/rules/_find`](https://www.elastic.co/docs/api/doc/kibana/operation/operation-findrules) |
| Update a rule | [`PUT /api/detection_engine/rules`](https://www.elastic.co/docs/api/doc/kibana/operation/operation-updaterule) |
| Bulk actions (enable, export, duplicate, delete) | [`POST /api/detection_engine/rules/_bulk_action`](https://www.elastic.co/docs/api/doc/kibana/operation/operation-performrulesbulkaction) |
| Import rules | [`POST /api/detection_engine/rules/_import`](https://www.elastic.co/docs/api/doc/kibana/operation/operation-importrules) |
| Export rules | [`POST /api/detection_engine/rules/_export`](https://www.elastic.co/docs/api/doc/kibana/operation/operation-exportrules) |
| Install prebuilt rules | [`PUT /api/detection_engine/rules/prepackaged`](https://www.elastic.co/docs/api/doc/kibana/operation/operation-installprebuiltrulesandtimelines) |
| Set alert status | [`POST /api/detection_engine/signals/status`](https://www.elastic.co/docs/api/doc/kibana/operation/operation-setalertsstatus) |
