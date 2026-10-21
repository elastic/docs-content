---
navigation_title: Not enough capacity during scale-up
description: Learn why a scale-up or new deployment in Elastic Cloud Hosted can show a not enough capacity message, and how to wait, mitigate, or contact support.
applies_to:
  deployment:
    ess: all
products:
  - id: cloud-hosted
---

# Understanding not enough capacity on scale-up [ec-not-enough-capacity]

A scale-up, or a new deployment, may temporarily show a capacity error message. It can also fail if {{ecloud}} or the underlying cloud service provider does not, in the end, have enough capacity for the desired size.

Specifically, while the plan is still trying, the [activity page](../../deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md) can show a message that follows this pattern. The text below is an example. The attempt number and the other values in angle brackets vary.

```sh
Retry [<attempt>] will happen in [60000 milliseconds]. Errors from previous attempt:
1. Could not ensure capacity allocation for [<deployment id>] result was [{"type":"capacity_by_zone","allocated_instances":0,"required_capacity":{"<zone>":{"<instance configuration>":<size>}},"failed_instances":[{"instance_name":"not-created-yet"}]}]
```

The plan retries this check up to 100 times. While the retry message is still showing, wait. If the scale-up succeeds within those retries, you do not need to contact support. If the plan fails after the retries, [contact support](/troubleshoot/index.md#contact-us).

This page explains why the change can fail, and what you can do.

## Possible causes [ec-not-enough-capacity-causes]

There are two situations:

### When {{ecloud}} has enough capacity

When {{ecloud}} and the underlying cloud service provider have enough capacity, but the allocator that holds the instance does not, it may take time for {{ecloud}} to orchestrate the following actions:

* Spin up new empty allocators.
* On the new allocator, spin up a new instance with the desired size, and copy the data from the current instance into the new instance.

While a new allocator is spun up, this `Could not ensure capacity allocation for...` message can be observed. In this situation, the message is temporary. The scale-up can succeed after a retry, within those 100 attempts.

### When {{ecloud}} or the underlying cloud service provider do not have enough capacity

When there is not enough capacity in {{ecloud}} or the underlying cloud service provider (CSP), the plan can fail after the maximum number of retries and show this message.

This usually happens when:

* A large scale-up on a current hardware profile, such as an increase of several hundred GiB in RAM.
* A normal scale-up using a [deprecated hardware profile](../../deploy-manage/deploy/elastic-cloud/change-hardware.md#ec-deprecated-icdt).

## Mitigation [ec-not-enough-capacity-mitigation]

The following sections describe how to mitigate this situation.

### Configure high availability

Configuring [high availability](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md#ec-ha) can avoid a performance outage and degradation while the deployment changes size. With high availability, search and indexing continue during the scale-up. You do not need to follow the retry time. The deployment keeps serving at its current size, and the new capacity is available when a later retry attempt succeeds.

### Avoid using a deprecated hardware profile

A current [hardware profile](../../deploy-manage/deploy/elastic-cloud/ec-change-hardware-profile.md#ec_upgrade_to_the_newest_version_of_your_current_hardware_profile) usually has more available capacity than a [deprecated one](../../deploy-manage/deploy/elastic-cloud/change-hardware.md#ec-deprecated-icdt). If you use a deprecated hardware profile and encounter the "not enough capacity" issue, consider migrating to a current one before the scale-up.

### Contact support for scale-up failure

In case the scale-up fails eventually, please [contact support](/troubleshoot/index.md#contact-us).

Additionally, for a large scale-up on a current hardware profile, such as an increase of several hundred GiB in RAM, there is a higher chance the underlying CSP does not have enough capacity. In this situation, we recommend you contact support beforehand, so that we can better help you plan for the desired capacity.
