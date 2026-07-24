---
navigation_title: Create a composite SLO
applies_to:
  stack: preview 9.5+
  serverless: preview
products:
  - id: observability
  - id: cloud-serverless
---

# Composite service level objectives (SLOs) [observability-create-a-composite-slo]

A composite SLO aggregates multiple individual SLOs into a single health indicator using a weighted average. Use composite SLOs to:

* Track reliability at the system or platform level instead of per service
* Define service importance using weights so the composite score reflects your priorities
* Detect platform-wide reliability degradation early through burn-rate alerts across all member SLOs

For example, you could create a "Checkout Flow Health" composite SLO that combines SLOs for your payment service, cart service, and inventory service.

::::{important}
**For Observability serverless projects**, the [**SLO Editor** custom role](/solutions/observability/incident-management/configure-service-level-objective-slo-access.md#slo-all-access) is required to create SLOs.

**For {{product.elastic-stack}}**, to create and manage SLOs, you need an [appropriate license](https://www.elastic.co/subscriptions), an {{es}} cluster with both `transform` and `ingest` [node roles](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles) present, and [SLO access](/solutions/observability/incident-management/configure-service-level-objective-slo-access.md) must be configured.
::::

::::{note}
Composite SLOs are enabled automatically for {{product.serverless-observability}} and {{ech}} deployments. For self-managed deployments, add the following to your `kibana.yml` to enable the feature:

```yaml
feature_flags.overrides:
  slo.compositeSloEnabled: true
```
::::

## Create and configure a composite SLO [create-configure-composite-slo]

Follow these steps to create and configure a composite SLO:

::::::{stepper}

:::::{step} Create a new composite SLO

Create a new composite SLO from the **SLOs** page:

1. Find **SLOs** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select **Create SLO**, then select **Create composite SLO**.

:::::

:::::{step} Select member SLOs

Add the individual SLOs that make up the composite SLO. A composite SLO can include up to 25 member SLOs.

For each member SLO, set the following:

* **SLO**: Select an existing SLO. When the selected SLO has multiple instances (created using the **Group by** field), you can optionally filter to specific **Instances**. By default, the composite SLO includes all instances of the selected SLO.
* **Weight**: A numeric weight that controls how much this SLO contributes to the composite **SLI value**. Weights are relative. For example, a weight of 2 counts twice as much as a weight of 1. The default weight is 1.

:::::

:::::{step} Set objectives
Set the following objectives for your composite SLO:

**Time window**
:   Select a rolling time window duration for your composite SLO. Rolling windows use data from a fixed lookback period that moves forward as time passes. For example, the last 30 days.

    From the **Time window** menu, select your duration.

**Budgeting method**
:   The **Occurrences** budgeting method, which computes the SLI using the number of good events and the number of total events across all member SLOs.

**Target**
:   Set the composite SLO's target as a percentage. This target is independent of the targets set on individual member SLOs.

:::::

:::::{step} Name, description, and tags

Give your composite SLO a **Name**, an optional **Description** to provide context for what system or platform it represents, and any relevant **Tags** that you can use for filtering.

:::::

::::::


## View composite SLOs [composite-slo-viewing]

Your composite SLO appears on the **Composite SLOs** tab of the **SLOs** page. Each row displays:

* **Status**: Whether the composite SLO is currently meeting its target.
* **Name**: The name of the composite SLO.
* **Tags**: Labels associated with the composite SLO that you can use for filtering.
* **Healthy members**: The number of member SLOs currently meeting their targets. For example, 3 of 25.
* **Objective**: The composite SLO's target percentage, set independently from the targets of individual member SLOs.
* **SLI value**: The weighted average of all member SLI values.
* **Historical status**: A graphical representation of the the composite SLOs history.
* **Budget remaining**: How much error budget remains until the composite SLO violates its target.
* **Active alerts**: The number of active alerts across the underlying member SLOs.
* **Burn rate**: The rate at which the composite SLO is consuming its error budget, shown over 5-minute, 1-hour, and 1-day windows.
* **Time window**: The rolling time window over which the composite SLO is evaluated.

Expand a row to see the individual member SLOs and their data.