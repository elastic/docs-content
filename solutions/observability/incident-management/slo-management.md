---
navigation_title: View and manage SLOs
applies_to:
  stack: ga
  serverless:
    observability: ga
products:
  - id: observability
  - id: cloud-serverless
---

# View and manage SLOs in {{product.observability}}

Manage your service level objectives (SLOs) from the **SLO Management** page. View SLO definitions, monitor the health of your SLOs, and perform actions such as editing, cloning, purging data, and deleting SLOs.

To open the **SLO management** page:

1. Navigate to the **SLOs** page in the main menu, or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select **Manage SLOs**.

## Filter SLOs

From the SLO Management page, use the search bar to find SLOs by name. Use the **Filter tags** menu to include or exclude SLOs from the view based on the defined tags.

## Monitor SLO health
```{applies_to}
stack: ga 9.3
```

The **Health** column of the SLO management table shows the following:

* **Healthy**: the SLO transforms are operating as expected.
* **Needs attention**: the SLO transforms are not operating as expected and needs attention.

For more on SLO transforms and troubleshooting SLO health, refer to [Understanding SLO internals](../../../troubleshoot/observability/troubleshoot-service-level-objectives-slos.md#slo-understanding-slos).

## Purge stale SLO instances

A stale SLO instance hasn't received new data within the **Stale SLOs threshold**, which you can set in the **SLOs Settings**.

From the **Overview** on the **SLOs** page, you can see the number of **Stale** SLOs. Select the number to show your stale SLOs.

Occasionally, you might want to delete these stale instances. To purge your stale SLO instances:

### Purge all stale SLO instances
```{applies_to}
stack: ga 9.3
```

1. From the **SLO management** page, select **Actions** → **Purge stale instances**.
1. If you don't want to delete stale instances according to the predefined **Stale SLOs threshold** setting, you can update the **Stale threshold**.
1. Select **Purge**.

### Purge stale instances from selected SLOs

1. From the **SLO management** page, select the checkbox next to the SLOs from which you want to purge stale instances.
1. From the **Selected [number] SLO** menu, select **Purge stale instances**.
1. If you don't want to delete stale instances according to the predefined **Stale SLOs threshold** setting, you can update the **Stale threshold**.
1. Select **Purge**.

## Purge SLO {{rollup}} data

Rollup functionality summarizes old, high-granularity data into a reduced granularity format for long-term storage. Occasionally, you might want to delete this {{rollup}} data. To purge your {{rollup}} data:

**Bulk purge SLO {{rollup}} data**
```{applies_to}
stack: ga 9.3
```

1. From the **SLO management** page, select the checkbox next to the SLOs from which you want to purge {{rollup}} data.
1. From the **Selected [number] SLO** menu, select **Purge {{rollup}} data**.
1. Select the options to define which data to purge.
1. Select **Purge**.

**Purge {{rollup}} data from a single SLO**

1. Open the **Actions** menu ({icon}`boxes_vertical`) for the SLO.
1. Select **Purge rollup data**.
1. Select the options to define which data to purge.
1. Select **Purge**.