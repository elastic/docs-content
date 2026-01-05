---
navigation_title: View and manage SLOs
applies_to:
  stack: ga 9.1
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
---

# View and manage SLOs in {{product.observability}}

Manage your service level objectives (SLOs) from the **SLO Management** page. View SLO definitions, monitor the health of your SLOs, and perform actions such as purging data, checking SLO health, and deleting SLOs.

:::{image} /solutions/images/observability-slo-management.png
:alt: Screenshot of the SLO Management user interface
:screenshot:
:::

To open the **SLO management** page:

1. Navigate to the **SLOs** page in the main menu, or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select **Manage SLOs**.

## Permissions

Actions like deleting SLOs and purging SLO data require [a role with edit privileges for SLOs](./configure-service-level-objective-slo-access.md##slo-all-access). Users with [read-only privileges](./configure-service-level-objective-slo-access.md##slo-read-access) can use the SLO Management page to find unhealthy SLOs that need attention.


## Filter SLOs

From the **SLO Management** page, use the search bar to find SLOs by name. Use the **Filter tags** menu to include or exclude SLOs from the view based on the defined tags.

## Monitor SLO health
```{applies_to}
stack: ga 9.3
```

The **Health** column of the SLO management table shows the following:

* **Healthy**: the SLO transforms are operating as expected.
* **Needs attention**: the SLO transforms are not operating as expected and need attention.

Select **Needs attention** to inspect the transforms with issues.

For more on SLO transforms and troubleshooting SLO health, refer to [Understanding SLO internals](../../../troubleshoot/observability/troubleshoot-service-level-objectives-slos.md#slo-understanding-slos).

## Bulk delete SLOs
Use the **SLO Managment** page to delete multiple SLOs at once. To bulk delete SLOs:

1. From the **SLO Management** page, select the checkbox next to the SLOs you want to delete.
1. From the **Selected [number] SLO** menu, select **Delete**.
1. Select **Delete**.

## Purge stale SLO instances
```{applies_to}
stack: ga 9.3
```

A stale SLO instance hasn't received new data within the **Stale SLOs threshold** period, which you can set in the SLOs **Settings** page.

From the **Overview** on the **SLOs** page, you can see the number of **Stale** SLOs. Select the number to show your stale SLOs.

Occasionally, you might want to delete these stale instances. You can either purge all stale SLO instances at once or select SLOs from which to purge stale instances.

### Purge all stale SLO instances

To pure all stale SLO instances:

1. From the **SLO Management** page, select **Actions** → **Purge stale instances**.
1. If you don't want to delete stale instances according to the predefined **Stale SLOs threshold** setting, you can update the **Stale threshold**.
1. Select **Purge**.

### Purge stale instances from selected SLOs

To purge stale instances from individual or multiple SLOs:

1. From the **SLO Management** page, select the checkbox next to the SLOs from which you want to purge stale instances.
1. From the **Selected [number] SLOs** menu, select **Purge stale instances**.
1. If you don't want to delete stale instances according to the predefined **Stale SLOs threshold** setting, you can update the **Stale threshold**.
1. Select **Purge**.

## Purge SLO {{rollup}} data
```{applies_to}
stack: ga 9.1
```

Rollup functionality summarizes old, high-granularity data into a reduced granularity format for long-term storage. Occasionally, you might want to delete this {{rollup}} data.

### Bulk purge SLO {{rollup}} data

To bulk purge SLO {{rollup}} data:

1. From the **SLO Management** page, select the checkbox next to the SLOs from which you want to purge {{rollup}} data.
1. From the **Selected [number] SLOs** menu, select **Purge {{rollup}} data**.
1. Define which data to purge.
1. Select **Purge**.

### Purge {{rollup}} data from a single SLO

To purge {{rollup}} data from a specific SLO:

1. Open the **Actions** menu ({icon}`boxes_vertical`) for the SLO from which you want to purge {{rollup}} data.
1. Select **Purge {{rollup}} data**.
1. Define which data to purge.
1. Select **Purge**.