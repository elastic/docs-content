---
navigation_title: Not enough capacity during scale-up or scale-out
description: Learn why a scale-up, a scale-out, or a new deployment in Elastic Cloud Hosted can show a not enough capacity message, and how to mitigate, or contact support.
applies_to:
  deployment:
    ech: ga
products:
  - id: cloud-hosted
---

# Not enough capacity on scale-up or scale-out [ec-not-enough-capacity]

When scaling up, scaling out, or creating a new deployment, you might encounter a temporary capacity error message if {{ecloud}} or the underlying cloud service provider (CSP) does not have enough capacity for the desired size. If sufficient capacity cannot be allocated, the operation might eventually fail.

This page explains the scale configuration change workflow, and what you can do when you encounter the failure.

:::{note}
In the rest of this page, we describe scale-up for simplicity. The content also applies to a scale-out.
:::

## Workflow

When you initialize a scale-up configuration change, 
* If the underlying hosts running deployment instances, such as {{es}} and {{kib}}, have enough available capacity, the scale-up operation proceeds normally, either on the existing hosts or by creating new instances on other available hosts.
* If the underlying hosts do not have enough capacity, {{ecloud}} might request additional hosts (virtual machines) from the cloud service provider (CSP) to accommodate the scale-up operation.

While {{ecloud}} requests additional hosts, the configuration change stays on `Validating plan prerequisites` step and it may take a long time. After those hosts are provisioned, the scale-up can still succeed.

### Possible failure causes

The configuration change can fail when:

* The CSP does not have enough resources. A large scale-up on a current hardware profile, such as an increase of several hundred GiB in RAM, has a higher chance of this.
* The deployment uses a [deprecated hardware profile](../../deploy-manage/deploy/elastic-cloud/change-hardware.md#ec-deprecated-icdt).

If the configuration change fails, you might see the following message on the [Activity page](../../deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md):

```
Not enough capacity to allocate instance(s)
Unable to get capacity from ...
```

:::{note}
If the plan fails, no change is made to the deployment. The previous size and billing still apply.
:::

### Potential performance degradation

During the scale-up, after {{ecloud}} has requested and provisioned the new hosts, the new {{stack}} instances are created and started, and the index/shard data is migrated from the old {{es}} instances to the new ones.

This migration consumes additional resources on the existing instances, and deployments without [high availability](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md#ec-ha) might experience temporary service degradation.


## Mitigation [ec-not-enough-capacity-mitigation]

The following sections describe how to mitigate this situation.

### Avoid using a deprecated hardware profile

Current [hardware profiles](../../deploy-manage/deploy/elastic-cloud/ec-change-hardware-profile.md#ec_upgrade_to_the_newest_version_of_your_current_hardware_profile) generally offer more available capacity than [deprecated profiles](../../deploy-manage/deploy/elastic-cloud/change-hardware.md#ec-deprecated-icdt). If you're using a deprecated profile and encounter a "not enough capacity" error when scaling up, consider migrating to a current profile first.

::::{note}
For large scale-ups, such as adding several hundred GiB of RAM, or large hardware profile migrations, notify support several weeks before your target date with your expected capacity needs and timeline. Advance notice allows Elastic to work on securing the necessary capacity or help you plan alternative options. Requests made without sufficient lead time are subject to CSP availability and may fail due to capacity limits.
::::

### Try a smaller increase

If a scale-up fails, try a smaller increase and then gradually work up to the size you need. For example, if you want 10 nodes in each availability zone, try 5 first.

### Configure high availability

Configuring [high availability](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md#ec-ha) can avoid a performance outage and degradation while the deployment changes size. With high availability, search and indexing continue smoothly during the scale-up while {{ecloud}} retries the configuration change. The deployment keeps serving at its current size, and the new capacity is available when a later retry attempt succeeds.

### Contact support for scale-up failure

In case the scale-up fails eventually, [contact support](/troubleshoot/index.md#contact-us) for assistance.
