---
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

# Configure retention [streams-configure-retention]

Managing data retention across multiple indexes typically requires configuring several different settings—{{ilm}} ({{ilm-init}}), data stream lifecycle, index templates, and index settings—each in a different place. Streams replaces this with a single UI so you can efficiently control storage costs and meet regulatory or compliance requirements.

The Streams **Retention** tab provides a single place to manage lifecycle policies for your streams:

- **Set retention periods per stream**: Configure how long each stream retains data without touching {{ilm-init}} policies, index templates, or index settings directly.
- **Cascade retention to child streams**: For wired streams, parent retention policies automatically apply to child streams. Override at the child level when a specific stream needs different settings.
- **Monitor storage in one view**: See storage size, ingestion averages, and tier distribution so you can align retention periods with storage costs and compliance requirements.

## Required permissions [streams-configure-retention-permissions]

To edit data retention in {{stack}}, you need the following data stream level privileges:

- `manage_data_stream_lifecycle`
- `manage_ilm`

For more information, refer to [Granting privileges for data streams and aliases](../../../deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md).

## Configure retention [streams-configure-retention-steps]

Use the following steps to review your stream's storage footprint, choose a retention method, and apply it.

:::::::{stepper}

::::::{step} Review storage and ingestion data

Select a stream and open its **Retention** tab. Before setting a retention policy, review the following panels to understand your data's footprint:

- **Storage size**: Total data volume and document count for the stream.
- **Ingestion averages**: Estimated ingestion per day and per month, based on total stream size divided by stream age.
- **Data lifecycle** or **{{ilm-init}} policy data tiers**: The amount of data in each phase (Hot, Warm, Cold, Frozen) so you can see where data is accumulating.
- **Ingestion over time**: A chart of estimated ingestion volume over time to help spot trends or spikes.

Use this information to decide how long you need to retain data and which retention method best fits your cost and compliance requirements.

For more information on data retention, refer to [Data stream lifecycle](../../../manage-data/lifecycle/data-stream.md).
::::::

::::::{step} Choose and configure a retention method

Select **Edit retention method** to open the configuration options, then choose one of the following methods:

:::::{tab-set}

::::{tab-item} Inherit retention

The stream uses retention settings from its index template (classic streams) or parent stream (wired streams). No custom period or policy is needed.

**Classic streams** default to the data stream's existing index template's data retention configuration. When a stream inherits retention settings from an index template, Streams doesn't manage retention. This is useful when onboarding existing data streams and preserving their lifecycle behavior while still benefiting from Streams' visibility and {{monitor-features}}.

**Wired streams** {applies_to}`serverless: preview` {applies_to}`stack: preview 9.2+` follow a hierarchical structure that supports inheritance. A child stream can inherit the lifecycle of its nearest ancestor that has a set {{ilm-init}} or retention period policy. When the ancestor's lifecycle is updated, Streams cascades the change to all child streams that inherit it.

To enable inheritance, turn on **Inherit from index template** or **parent stream** in the **Edit retention method** options.
::::

::::{tab-item} Set a retention period

Set the minimum number of days after which data is deleted. Data stays in the hot phase for best indexing and search performance.

To set a specific retention period:

1. Select **Edit retention method**.
1. Turn off **Inherit from index template** or **parent stream**, if enabled.
1. Select **Custom period**.
1. Set the number of days you want to retain data.

To define a global default retention policy for serverless projects, refer to [project settings](../../../deploy-manage/deploy/elastic-cloud/project-settings.md).
::::

::::{tab-item} Follow an {{ilm-init}} policy

```{applies_to}
serverless: unavailable
stack: preview =9.1, ga 9.2+
```

Select an existing {{ilm-init}} policy to automate how data moves through phases (hot, warm, cold) as it ages. {{ilm-init}} policies let you standardize data retention across Streams and other data streams.

To follow an existing policy:

1. Select **Edit retention method**.
1. Turn off **Inherit from index template** or **parent stream**, if enabled.
1. Select **{{ilm-init}} policy**, then choose a pre-defined policy from the list.

If the policy you need doesn't exist, refer to [Configure a lifecycle policy](../../../manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) to create one.
::::

:::::

::::::

::::::{step} Configure data lifecycle phases

```{applies_to}
stack: ga 9.4+
```

When a stream follows an {{ilm-init}} policy, the **Data lifecycle** panel shows the phases defined in that policy as a visual bar. You can edit existing phases or add new ones directly from the **Retention** tab:

- To edit an existing phase, select the phase in the **Data lifecycle** panel and click {icon}`pencil`.
- To add a phase, click **Add data phase** and select a phase.

This opens the **Edit data phases** window where you can configure or update your phases. The following phases are available:

**Hot**
: The index is actively updated and queried. This is the default phase for all data. Options include enabling read-only access and [downsampling](#streams-configure-retention-downsampling).

**Warm**
: The index is updated infrequently but still queried. Set the minimum age for data to move into this phase. Options include enabling read-only access and [downsampling](#streams-configure-retention-downsampling).

**Cold**
: The index is rarely updated or queried, and slower query performance is acceptable. Set the minimum age for data to move into this phase. Options include enabling read-only access, [downsampling](#streams-configure-retention-downsampling), and [{{search-snaps}}](#streams-configure-retention-searchable-snapshots).

**Frozen**
: The index is no longer updated and is queried rarely. Optimized for long-term retention at the lowest possible cost. Set the minimum age for data to move into this phase and configure a snapshot repository. The frozen phase requires a snapshot repository.

**Delete**
: Remove the index after a specified period of time. Set how long data is stored before deletion and optionally delete any associated [{{search-snaps}}](#streams-configure-retention-searchable-snapshots).

For more information on {{ilm-init}} phases and available actions, refer to [Index lifecycle](../../../manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md).

### Downsampling [streams-configure-retention-downsampling]

Downsampling reduces storage for time series data by replacing original metrics with statistical summaries at a higher sampling interval. For example, metrics sampled every 10 seconds can be consolidated into hourly data points as the data ages, significantly reducing storage while keeping the data queryable.

Downsampling is available in the Hot, Warm, and Cold phases and only applies to time series data streams.

For more information, refer to [Downsampling concepts](../../../manage-data/data-store/data-streams/downsampling-concepts.md).

### {{search-snaps-cap}} [streams-configure-retention-searchable-snapshots]

{{search-snaps-cap}} let you search infrequently accessed, read-only data directly from a snapshot repository without needing replica shards, significantly reducing storage costs. They are best suited for archival or historical data that requires infrequent access.

{{search-snaps-cap}} are available in the Cold and Frozen phases.

For more information, refer to [Searchable snapshots](../../../deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md).
::::::

::::::{step} Apply retention to child streams

```{applies_to}
serverless: preview
stack: preview 9.2+
```

For wired streams, retention policies cascade automatically from parent to child streams. When you update a parent stream's retention policy, Streams propagates the change to all child streams that inherit from it.

To override retention for a specific child stream, open that stream's **Retention** tab and configure a different method. The child stream uses its own policy instead of inheriting from the parent.
::::::

:::::::

## Set failure store retention [streams-configure-failure-store-retention]

A [failure store](../../../manage-data/data-store/data-streams/failure-store.md) is a secondary set of indices inside a data stream, dedicated to storing failed documents.

You can enable and configure failure store retention directly from the **Retention** tab. Select **Enable failure store** to turn it on and set the retention period for failed documents.
