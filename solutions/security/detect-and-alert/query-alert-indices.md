---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/query-alert-indices.html
  - https://www.elastic.co/guide/en/serverless/current/security-query-alert-indices.html
applies_to:
  stack: all
  serverless:
    security: all
---

# Query alert indices [security-query-alert-indices]

This page explains how you should query alert indices, for example, when building rule queries, custom dashboards, or visualizations. For more information about alert event field definitions, review the [Alert schema](/reference/security/fields-and-object-schemas/alert-schema.md).


## Alert index aliases [_alert_index_aliases]

We recommend querying the following index aliases:

We recommend querying the `.alerts-security.alerts-<space-id>` index alias. You should not include a dash or wildcard after the space ID. To query all spaces, use the following syntax: `.alerts-security.alerts-*`.


## Alert indices [_alert_indices]

For additional context, alert events are stored in hidden {{es}} indices. We do not recommend querying them directly. The naming convention for these indices and their aliases is `.internal.alerts-security.alerts-<space-id>-NNNNNN`, where `NNNNNN` is a number that increases over time, starting from 000001.

