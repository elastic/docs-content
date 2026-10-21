---
navigation_title: Not enough capacity during scale-up
description: Learn why a scale-up or new deployment in Elastic Cloud Hosted can show a not enough capacity message, and how to mitigate, or contact support.
applies_to:
  deployment:
    ech: ga
products:
  - id: cloud-hosted
---

# Not enough capacity on scale-up [ec-not-enough-capacity]

A scale-up, or a new deployment, may temporarily show a capacity error message. It can also fail if {{ecloud}} or the underlying cloud service provider (CSP) does not, in the end, have enough capacity for the desired size.

This page explains the scale-up configuration change workflow, and what you can do when you encounter the failure.

## Scale-up workflow

When you initialize a scale-up configuration change, 
* If the underlying hosts that hold your deployment instances, such as {{es}} and {{kib}}, have enough room for the size change, the configuration change will perform an inline size up straightforward. 
* If the underlying hosts do not have enough room, as a normal process, {{ecloud}} will request the new host (virtual machines) from the cloud provider. 

During the requesting period, you may observe the message that follows below pattern in the [activity page](../../deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md). 

```bash
Retry [<attempt>] will happen in [60000 milliseconds]. Errors from previous attempt:
1. Could not ensure capacity allocation for [<deployment id>] result was [{"type":"capacity_by_zone","allocated_instances":0,"required_capacity":{"<zone>":{"<instance configuration>":<size>}},"failed_instances":[{"instance_name":"not-created-yet"}]}]
```

While those hosts are starting, the message is temporary, and the scale-up can still succeed. In this situation, you can safely disregard this message.

### Possible failure causes

The configuration change can fail when:

* CSP does not have enough desired resources. A large scale-up on a current hardware profile, such as an increase of several hundred GiB in RAM, has a higher chance of this.
* The deployment uses a [deprecated hardware profile](../../deploy-manage/deploy/elastic-cloud/change-hardware.md#ec-deprecated-icdt).

In case of failure, you may observe below message in the [activity page](../../deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md).

```bash
Plan change failed: Not enough capacity to allocate instance(s)
```

### Potential performance degradation

During the scale-up, after {{ecloud}} required and started the new hosts, the new {{stack}} instances will be created and started, and the index/shard data will be migrated from old {{es}} instances to new ones. 

In this migration step, a part of the resources from existing instance is consumed, and the deployment without configuring [high availability](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md#ec-ha) may experience temporary service degradation.


## Mitigation [ec-not-enough-capacity-mitigation]

The following sections describe how to mitigate this situation.

### Avoid using a deprecated hardware profile

Current [hardware profiles](../../deploy-manage/deploy/elastic-cloud/ec-change-hardware-profile.md#ec_upgrade_to_the_newest_version_of_your_current_hardware_profile) generally offer more available capacity than [deprecated profiles](../../deploy-manage/deploy/elastic-cloud/change-hardware.md#ec-deprecated-icdt). If you're using a deprecated profile and encounter a "not enough capacity" error when scaling up, consider migrating to a current profile first.

::::{note}
For a large scale-up on a current hardware profile, such as increasing RAM by several hundred GiB, there is a higher chance the underlying CSP does not have enough capacity. In this situation, we recommend you contact support beforehand, so that we can better help you plan for the desired capacity.
::::


### Configure high availability

Configuring [high availability](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md#ec-ha) can avoid a performance outage and degradation while the deployment changes size. With high availability, search and indexing continue smoothly during the scale-up, so you can leave the configuration change to retry. The deployment keeps serving at its current size, and the new capacity is available when a later retry attempt succeeds.

### Contact support for scale-up failure

In case the scale-up fails eventually, [contact support](/troubleshoot/index.md#contact-us) for assistance.
