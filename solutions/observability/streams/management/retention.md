---
navigation_title: Manage data retention
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
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

# Manage data retention for Streams [streams-data-retention]

After selecting a stream, use the **Retention** tab to set how long your stream retains data and to get insight into your stream's data ingestion and storage size. The following components help you determine how long you want your stream to retain data:

- **Retention**: The current retention policy, including the source of the policy.
- **Storage size**: The total data volume and number of documents in the stream.
- **Ingestion averages**: Estimated ingestion per day and month, calculated based on the total size of all data in the stream divided by the stream's age.
- **Data lifecycle**: {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` The amount of data in each data phase (**Hot**, **Warm**, **Cold**, **Frozen**, **Delete**).
- **{{ilm-init}} policy data tiers**: {applies_to}`stack: preview =9.1, ga 9.2-9.3` The amount of data in each data tier (**Hot**, **Warm**, **Cold**).
- **Ingestion over time**: Estimated ingestion volume over time based on the number of documents over that time, multiplied by the average document size in the backing index.

For more information on data retention, refer to [Data stream lifecycle](../../../../manage-data/lifecycle/data-stream.md).

## Required permissions

To edit data retention in {{stack}}, you need the following data stream level privileges:
- `manage_data_stream_lifecycle`
- `manage_ilm`

For more information, refer to [Granting privileges for data streams and aliases](../../../../deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md).

## Configure data retention [streams-update-data-retention]

Under the **Retention** tab, select **Edit retention method** to open the configuration options.

You have the following options when setting your data retention:

- [**Inherit from index template or parent stream**](#streams-retention-inherit-from-template): Use the data retention configuration that is set in a classic stream's index template or a wired stream's parent stream.
- [**Set a specific retention period**](#streams-retention-dsl): You can set your stream to retain data for a specific number of days. Setting a specific or indefinite retention period stores data in the hot phase for best indexing and search performance.
- [**Follow an ILM policy**](#streams-retention-ilm): {applies_to}`stack: preview =9.1, ga 9.2+` Select an existing ILM policy that uses phases for your data (hot, warm, cold) to allow more control when managing storage, performance, and cost as your data ages.


### Inherit from index template or parent stream [streams-retention-inherit-from-template]
If you enable **Inherit from index template** or **parent stream**, the stream uses the retention settings from its index template (for classic streams) or parent stream (for wired streams). When this option is enabled, you don’t need to specify a custom retention period or policy.

#### Inherit from index template
Classic streams let you default to the data stream's existing index template’s data retention configuration. When a stream inherits retention settings from an index template, Streams doesn't manage retention.

This is useful when onboarding existing data streams and preserving their lifecycle behavior while still benefiting from Streams' visibility and monitoring features.

#### Inherit from parent stream
```{applies_to}
stack: preview 9.2
serverless: preview
```

Wired streams follow a hierarchical structure that supports inheritance. A child stream can inherit the lifecycle of its nearest ancestor that has a set {{ilm-init}} or retention period policy. This lets you define a single lifecycle policy higher in the hierarchy, and Streams automatically applies it to all relevant descendants.

When the ancestor’s lifecycle is updated, Streams cascades the change to all child streams that inherit it, keeping everything in sync.

### Set a specific retention period [streams-retention-dsl]
The **Retention period** is the minimum number of days after which the data is deleted. To set data retention to a specific time period:

1. Under **Retention**, select **Edit data retention**.
1. Turn off **Inherit from index template** or **parent stream**, if on.
1. Select **Custom period**.
1. Set the period of time that you want to retain data.

To define a global default retention policy, refer to [project settings](../../../../deploy-manage/deploy/elastic-cloud/project-settings.md).

### Follow an {{ilm-init}} policy [streams-retention-ilm]
```{applies_to}
serverless: unavailable
stack: preview =9.1, ga 9.2+
```
[{{ilm-init}} policies](../../../../manage-data/lifecycle/index-lifecycle-management.md) let you automate and standardize data retention across Streams and other data streams.

To have your streams follow an existing policy:

1. Under **Retention**, select **Edit data retention**.
1. Turn off **Inherit from index template** or **parent stream**, if on.
1. Select **{{ilm-init}} policy**, then select a pre-defined {{ilm-init}} policy from the list.

If the policy you want doesn't exist, create a new {{ilm-init}} policy. Refer to [Configure a lifecycle policy](../../../../manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) for more information.

## Modify data lifecycle
```{applies_to}
stack: ga 9.4+
serverless: unavailable
```

When a stream follows an {{ilm-init}} policy, the **Data lifecycle** panel on the **Retention** tab displays the phases defined in that policy as a visual bar. Each phase represents a stage in the data lifecycle, from active indexing to eventual deletion. Data moves between phases based on the minimum age you configure for each phase.

To edit or add a phase:

- To edit an existing phase, select the phase (**Hot**, **Warm**, **Cold**, **Frozen**, or **Delete**) in the **Data lifecycle** panel, and click {icon}`pencil`.
- To add a new phase, click **Add data phase** and select the phase you want to add.

This opens the **Edit data phases** window, where you can configure or update your phases.

The following phases and options are available:

**Hot**
: The index is actively updated and queried. This is the default phase for all data. Options include enabling read-only access and [downsampling](#streams-retention-downsampling).

**Warm**
: The index is updated infrequently but still queried. Set the minimum age for data to move into this phase. Options include enabling read-only access and [downsampling](#streams-retention-downsampling).

**Cold**
: The index is rarely updated or queried, and slower query performance is acceptable. Set the minimum age for data to move into this phase. Options include enabling read-only access, [downsampling](#streams-retention-downsampling), and [searchable snapshots](#streams-retention-searchable-snapshots).

**Frozen**
: The index is no longer updated and is queried rarely. Optimized for long-term retention at the lowest possible cost. Set the minimum age for data to move into this phase and configure a [snapshot repository](#streams-retention-searchable-snapshots). The frozen phase requires a snapshot repository.

**Delete**
: Remove the index after a specified period of time. Set how long data is stored before deletion and optionally delete any associated [searchable snapshots](#streams-retention-searchable-snapshots).

For more information on {{ilm-init}} phases and available actions, refer to [Index lifecycle](../../../../manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md).

### Downsampling [streams-retention-downsampling]

Downsampling reduces storage for time series data by replacing original metrics with statistical summaries at a higher sampling interval. For example, metrics sampled every 10 seconds can be consolidated into hourly data points as the data ages, significantly reducing storage while keeping the data queryable.

Downsampling is available in the Hot, Warm, and Cold phases and only applies to time series data streams.

For more information, refer to [Downsampling concepts](../../../../manage-data/data-store/data-streams/downsampling-concepts.md).

### Searchable snapshots [streams-retention-searchable-snapshots]

Searchable snapshots let you search infrequently accessed, read-only data directly from a snapshot repository without needing replica shards, significantly reducing storage costs. They are best suited for archival or historical data that requires infrequent access.

Searchable snapshots are available in the Cold and Frozen phases.

For more information, refer to [Searchable snapshots](../../../../deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md).

## Set failure store data retention

A [failure store](../../../../manage-data/data-store/data-streams/failure-store.md) is a secondary set of indices inside a data stream, dedicated to storing failed documents.

You can enable failure stores from the **Retention** tab by selecting **Enable failure store**. This opens the failure store configuration for your stream. From here, you can set the retention period.