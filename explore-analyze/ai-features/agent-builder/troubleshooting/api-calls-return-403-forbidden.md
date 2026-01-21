---
navigation_title: "403 Forbidden"
description: "Learn how to diagnose and resolve 403 Forbidden errors when using Agent Builder."
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless:
    elasticsearch: ga
    observability: preview
    security: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# API calls return `403 Forbidden` in {{agent-builder}}

A `403 Forbidden` error occurs when you don't have access to the required subscription or feature tier for {{agent-builder}}.

## Symptoms

API calls to {{agent-builder}} endpoints return a `403 Forbidden` HTTP status code.

## Cause

{{agent-builder}} requires specific subscription levels depending on your deployment type.

## Resolution

Upgrade to the required subscription or feature tier for your deployment type. To learn more, refer to [Manage your subscription](/deploy-manage/cloud-organization/billing/manage-subscription.md).


## Related pages

- [Get started](../get-started.md#enable-agent-builder)
- [Manage your subscription](/deploy-manage/cloud-organization/billing/manage-subscription.md)
