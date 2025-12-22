---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-vcpu-boost-instance.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-vcpu-boost-instance.html
applies_to:
  deployment:
    ess: all
products:
  - id: cloud-hosted
---

# vCPU boosting and credits [ec-vcpu-boost-instance]

{{ecloud}} allows smaller instance sizes to get temporarily boosted vCPU when under heavy load. vCPU boosting is governed by vCPU credits that instances can earn over time when vCPU usage is less than the assigned amount.

::::{important}
vCPU credits temporarily assigns extra CPU resources beyond the default. These credits are not always guaranteed, and might be reset during essential maintenance.
::::

## How does vCPU boosting work? [ec_how_does_vcpu_boosting_work]

Based on the instance size, the vCPU resources assigned to your instance can be boosted to improve performance temporarily, by using vCPU credits. If credits are available, {{ecloud}} will automatically boost your instance when under heavy load. Boosting is available depending on the instance size:

* Instance sizes up to and including 12 GB of RAM get boosted. The boosted vCPU value is `16 * vCPU ratio`, the vCPU ratios are dependent on the [hardware profile](cloud://reference/cloud-hosted/hardware.md#ec-getting-started-configurations) selected. If an instance is eligible for boosting, the {{ecloud}} console will display **Up to 2.5 vCPU**, depending on the hardware profile selected. The baseline, or unboosted, vCPU value is calculated as: `RAM size * vCPU ratio`.
* Instance sizes bigger than 12 GB of RAM do not get boosted. The vCPU value is displayed in the {{ecloud}} console and calculated as follows: `RAM size * vCPU ratio`.


## What are vCPU credits? [ec_what_are_vcpu_credits]

[vCPU](/reference/glossary/index.md#glossary-vcpu) credits enable a smaller instance to perform as if it were assigned the vCPU resources of a larger instance, but only for a limited time. vCPU credits are available only on smaller instances up to and including 12 GB of RAM.

vCPU credits persist through cluster restarts, but they are tied to your existing instance nodes. Operations that create new instance nodes will lose existing vCPU credits. This happens when you resize your instance, or if Elastic performs system maintenance on your nodes.


## How to earn vCPU credits? [ec_how_to_earn_vcpu_credits]

When you initially create an instance, you receive a credit of 60 seconds worth of vCPU time. You can accumulate additional credits when your vCPU usage is less than what your instance is assigned. At most, you can accumulate one hour worth of additional vCPU time per GB of RAM for your instance.

For example: An instance with 4 GB of RAM, can at most accumulate four hours worth of additional vCPU time and can consume all of these vCPU credits within four hours when loaded heavily with requests.

If you observe declining performance on a smaller instance over time, you might have depleted your vCPU credits. In this case, increase the size of your cluster to handle the workload with consistent performance.

For more information, check [{{ech}} default provider instance configurations](cloud://reference/cloud-hosted/hardware.md#ec-getting-started-configurations).


## Where to check vCPU credits status? [ec_where_to_check_vcpu_credits_status]

You can check the **Monitoring > Performance > CPU Credits** section of the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), and find the related metrics:

:::{image} /deploy-manage/images/cloud-metrics-credits.png
:alt: CPU usage versus CPU credits over time
:::


## What to do if my vCPU credits get depleted constantly? [ec_what_to_do_if_my_vcpu_credits_get_depleted_constantly]

If you need your cluster to be able to sustain a certain level of performance, you cannot rely on CPU boosting to handle the workload except temporarily. To ensure that performance can be sustained, consider increasing the size of your cluster. Refer to [](/troubleshoot/monitoring/performance.md) for more guidance.

