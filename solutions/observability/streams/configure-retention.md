---
navigation_title: Configure data lifecycle
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
description: Learn how to configure data retention policies for your streams.
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Configure data lifecycle with Streams [streams-configure-retention]

Managing data lifecycles across multiple indexes typically requires configuring {{ilm}} ({{ilm-init}}), data stream lifecycle, index templates, and index settings, each in a different place. Streams replaces this with a single UI so you can control storage and meet regulatory or compliance requirements.

The **Data lifecycle** tab (**Retention** prior to Stack v9.5) provides a single place to manage lifecycle policies for your streams:

- **Set lifecycle periods per stream**: Configure how long each stream retains data without touching {{ilm-init}} policies, index templates, or index settings directly.
- **Parent lifecycle settings cascade to child streams**: For wired streams, parent stream lifecycle policies automatically apply to child streams. Override at the child level when a specific child stream needs different lifecycle settings.
- **Monitor storage in one view**: See storage size, ingestion averages, and phase distribution so you can align lifecycle periods with storage costs and compliance requirements.
- **Reduce storage with downsampling**: For time series data, replace high-resolution metrics with statistical summaries as data ages. This reduces storage costs and lets you retain data longer, with some loss of temporal precision.

## Before you get started [streams-configure-retention-permissions]

To edit data lifecycle in {{stack}}, you need the following data stream level privileges:

- `manage_data_stream_lifecycle`
- `manage_ilm`

For more information, refer to [Granting privileges for data streams and aliases](../../../deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md).

## Configure data lifecycle [streams-configure-retention-steps]

Follow these steps to review your stream's storage footprint, select a lifecycle method, and apply the policy.

### Step 1: Open the Data lifecycle tab

1. Open **Streams** from the navigation menu or use the [global search field](../../../explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select your stream from the list.
1. Go to the **Data lifecycle** tab (**Retention** in earlier versions).

### Step 2: Review storage and ingestion data

Before setting a lifecycle policy, review the following panels to understand your data's footprint:

- **Storage size**: Total data volume and document count for the stream, including data across all phases.
- **Ingestion averages**: Estimated ingestion per day and per month, based on total stream size divided by stream age.
- **Data lifecycle** or **{{ilm-init}} policy data tiers**: The amount of data in each phase (Hot, Warm, Cold, Frozen) so you can see where data is accumulating.
- **Ingestion over time**: A chart of estimated ingestion volume over time to help spot trends or spikes. For streams with an active frozen phase, volume is split by phase.

Use this information to decide how long you need to retain data and which lifecycle method best fits your cost and compliance requirements.

For more information on data lifecycle, refer to [Data stream lifecycle](../../../manage-data/lifecycle/data-stream.md).

### Step 3: Choose and configure a lifecycle method

Select {icon}`controls` **Edit lifecycle method** to open the configuration options, then select one of the following methods:

- [**Inherit lifecycle**](#streams-configure-retention-inherit): Use lifecycle settings from the stream's index template (classic streams) or parent stream (wired streams).
    - **Classic streams**: This preserves existing data streams' behavior while still benefiting from Streams' other features.
    - **Wired streams**: Child streams automatically inherit lifecycle settings and updates from their parent stream.
- [**Set a lifecycle period**](#streams-configure-retention-period): Define a minimum number of days before data is deleted. Data stays in the hot phase for best performance. Recommended when a lifecycle period is specific to a single stream.
- [**Follow an {{ilm-init}} policy**](#streams-configure-retention-ilm): Apply an existing {{ilm-init}} policy to automate how data moves through lifecycle phases as it ages. Recommended when you want to share an {{ilm-init}} policy across multiple streams.

#### Inherit lifecycle [streams-configure-retention-inherit]

To use the lifecycle settings from the stream's index template (classic streams) or parent stream (wired streams) without setting a custom period or policy:

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.5+", "serverless": "ga" }

1. Select {icon}`controls` **Edit lifecycle method**.
1. Turn on **Inherit lifecycle from index template** or **parent stream**.

For wired streams, you can override lifecycle settings for a specific child stream by opening that stream's **Data lifecycle** tab and configuring a different method. The child stream will then use its own policy instead of inheriting from the parent.

:::

:::{applies-item} { "stack": "ga 9.1-9.4" }

1. Select **Edit retention method**.
1. Turn on **Inherit from index template** or **parent stream**.

For wired streams, you can override retention for a specific child stream by opening that stream's **Retention** tab and configuring a different method. The child stream will then use its own policy instead of inheriting from the parent.
:::

::::

#### Set a lifecycle period [streams-configure-retention-period]

To set a specific lifecycle period:

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.5+", "serverless": "ga" }

1. Select {icon}`controls` **Edit lifecycle method**.
1. Turn off **Inherit lifecycle from index template** or **parent stream** if enabled.
1. Select **Data stream lifecycle**.
1. From the **Data stream lifecycle** panel, select **Add data phase** → **Delete phase**.
1. Set the delete phase to the number of days you want to retain data and select **Apply**.

To define a global default lifecycle policy for serverless projects, refer to [project settings](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).
:::

:::{applies-item} { "stack": "ga 9.1-9.4" }

1. Select **Edit retention method**.
1. Turn off **Inherit from index template** or **parent stream**, if enabled.
1. Select **Custom period**.
1. Set the number of days you want to retain data.
:::

::::

#### Follow an {{ilm-init}} policy [streams-configure-retention-ilm]

```{applies_to}
serverless: unavailable
stack: preview =9.1, ga 9.2+
```

Select an existing {{ilm-init}} policy to automate how data moves through phases (Hot, Warm, Cold, Frozen) as it ages. {{ilm-init}} policies let you standardize data lifecycle across Streams and other data streams.

To follow an existing policy:

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.5+" }

1. Select {icon}`controls` **Edit lifecycle method**.
1. Turn off **Inherit from index template** or **parent stream**, if enabled.
1. Select **{{ilm-init}} policy**, then select a predefined policy from the list.

After selecting a policy, you can [configure data lifecycle phases](#streams-configure-data-lifecycle-phases) directly from the **Data lifecycle** tab.

:::

:::{applies-item} { "stack": "ga 9.1-9.4" }

1. Select **Edit retention method**.
1. Turn off **Inherit from index template** or **parent stream**, if enabled.
1. Select **{{ilm-init}} policy**, then choose a predefined policy from the list.

After selecting a policy, you can [configure data lifecycle phases](#streams-configure-data-lifecycle-phases) directly from the **Retention** tab.

:::

::::

If the policy you need doesn't exist, refer to [Configure a lifecycle policy](../../../manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) to create one.

## Configure data lifecycle phases [streams-configure-data-lifecycle-phases]

```{applies_to}
stack: ga 9.4+
```

The **Data lifecycle** tab (**Retention** in earlier versions) shows your stream's phases as a visual timeline. From here, you can edit existing phases or add new ones:

- To edit an existing phase, select the phase from the **Data phases** timeline and select **Edit**.
- To add a phase, select **Add data phase**, then choose a phase.

This opens **Edit data phases**, where you can configure or update your phases. {applies_to}`stack: ga 9.5+` For streams using a data stream lifecycle, you can add **Frozen** and **Delete** phases. For streams using an {{ilm-init}}, you can add any of the following phases:

**Hot**
:   The index is actively updated and queried. This is the default phase for all data. Options include enabling read-only access and [downsampling](#streams-configure-retention-downsampling).

**Warm**
:   The index is updated infrequently but still queried. Set the minimum age for data to move into this phase. Options include enabling read-only access and [downsampling](#streams-configure-retention-downsampling).

**Cold**
:   The index is rarely updated or queried, and slower query performance is acceptable. Set the minimum age for data to move into this phase. Options include enabling read-only access, [downsampling](#streams-configure-retention-downsampling), and [{{search-snaps}}](#streams-configure-retention-searchable-snapshots).

**Frozen**
:   The index is no longer updated and is queried rarely. Optimized for long-term retention at the lowest possible cost. Set the minimum age for data to move into this phase and configure a snapshot repository.

    {applies_to}`stack: ga 9.5+` For streams using a data stream lifecycle, you need to set a default snapshot repository and the [appropriate subscription]({{subscriptions}}) before adding a frozen phase. If no default repository is set, you'll be prompted to set one. After setting it, select {icon}`refresh` to resume.

**Delete**
:   Remove the index after a specified period of time. Set how long data is stored before deletion and optionally delete any associated [{{search-snaps}}](#streams-configure-retention-searchable-snapshots).

For more information, refer to [{{ilm}} phases and actions](../../../manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md).

### {{search-snaps-cap}} [streams-configure-retention-searchable-snapshots]

{{search-snaps-cap}} let you search infrequently accessed, read-only data directly from a snapshot repository without needing replica shards, significantly reducing storage costs. A local data cache speeds up repeat access. They are best suited for historical data that requires infrequent access or archival.

{{search-snaps-cap}} are available in the Cold and Frozen phases.

For more information, refer to [{{search-snaps-cap}}](../../../deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md).

### Downsampling [streams-configure-retention-downsampling]

Downsampling reduces storage for time series data by replacing original metrics with statistical summaries at a higher sampling interval. For example, metrics sampled every 10 seconds can be consolidated into hourly data points as the data ages, significantly reducing storage while keeping the data queryable.

Downsampling is available in the Hot, Warm, and Cold phases and only applies to time series data streams.

For more information, refer to [Downsampling concepts](../../../manage-data/data-store/data-streams/downsampling-concepts.md).

## Set failed data lifecycle [streams-configure-failure-store-retention]

When a document fails to be ingested because of a processor error or a mapping conflict, Streams writes it to the [failure store](../../../manage-data/data-store/data-streams/failure-store.md) instead of dropping it. This lets you inspect what went wrong and fix issues using the actual failing documents, rather than losing data silently.

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.5+", "serverless": "ga" }

1. Under **Failed data**, select {icon}`controls` **Edit failed data lifecycle**.
1. Turn off **Inherit lifecycle from index template** or **parent stream** if enabled.
1. From the **Data stream lifecycle** panel, select **Add **Add delete phase**.
1. Set the delete phase to the number of days you want to retain data and select **Apply**.

:::

:::{applies-item} { "stack": "ga 9.1-9.4" }

You can enable and configure failure store lifecycle directly from the **Retention** tab. Select **Enable failure store** to turn it on and set the lifecycle period for failed documents.

:::

::::

To review and resolve ingestion failures, refer to [Manage data quality](./manage-data-quality.md).