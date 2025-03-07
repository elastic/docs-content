---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/query-alert-indices.html
  - https://www.elastic.co/guide/en/serverless/current/security-query-alert-indices.html
---

# Query alert indices

% What needs to be done: Align serverless/stateful

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/security-docs/security/query-alert-indices.md
% - [ ] ./raw-migrated-files/docs-content/serverless/security-query-alert-indices.md

This page explains how you should query alert indices, for example, when building rule queries, custom dashboards, or visualizations. For more information about alert event field definitions, review the [Alert schema](/reference/security/fields-and-object-schemas/alert-schema.md).


## Alert index aliases [_alert_index_aliases]

We recommend querying the following index aliases:

* If you’re using version 8.0.0 or later: `.alerts-security.alerts-<space-id>` This alias includes the legacy (before 8.0.0) and the new alert indices.
* If you’re using a version before 8.0.0: `.siem-signals-<space-id>` Queries on this alias will function regardless of your {{stack}} version but will not follow the newer `.alerts` naming convention and may be deprecated in future releases.

Regardless of which alias you query, you should not include a dash or wildcard after the space ID. To query all spaces, use the following syntax: `.alerts-security.alerts-*` or `.siem-signals-*`.


## Alert indices [_alert_indices]

For additional context, alert events are stored in hidden {{es}} indices. We do not recommend querying them directly. The naming conventions for these indices and their aliases differ depending on which version of {{stack}} you’re running:

* **8.0.0 or later:** `.internal.alerts-security.alerts-<space-id>-NNNNNN`, where `NNNNNN` is a number that increases over time, starting from 000001.
* **Before 8.0.0:** `.siem-signals-<space-id>-NNNNNN`, where `NNNNNN` is a number that increases over time, starting from 000001.

