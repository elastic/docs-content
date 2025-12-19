---
navigation_title: Manage data retention
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
---

# Manage data retention for Streams [streams-data-retention]

After selecting a stream, use the **Retention** tab to set how long your stream retains data and to get insight into your stream's data ingestion and storage size. The following components help you determine how long you want your stream to retain data:

- **Retention**: The current retention policy, including the source of the policy.
- **Storage size**: The total data volume and number of documents in the stream.
- **Ingestion averages**: Estimated ingestion per day and month, calculated based on the total size of all data in the stream divided by the stream's age.
- **ILM policy data tiers**: {applies_to}`stack: preview =9.1, ga 9.2+` The amount of data in each data tier (**Hot**, **Warm**, **Cold**).
- **Ingestion over time**: Estimated ingestion volume over time based on the number of documents over that time, multiplied by the average document size in the backing index.

For more information on data retention, refer to [Data stream lifecycle](../../../../manage-data/lifecycle/data-stream.md).

## Required permissions

To edit data retention in {{stack}}, you need the following data stream level privileges:
- `manage_data_stream_lifecycle`
- `manage_ilm`

For more information, refer to [Granting privileges for data streams and aliases](../../../../deploy-manage/users-roles/cluster-or-deployment-auth/granting-privileges-for-data-streams-aliases.md).

## Retention configuration options [streams-update-data-retention]
Under **Retention**, select **Edit data retention** to open the configuration options. You have the following options when setting your data retention:

- [**Inherit from index template or parent stream**](#streams-retention-inherit-from-template): Use the data retention configuration that's set in a classic stream's index template or a wired stream's parent stream.
- [**Set a specific retention period**](#streams-retention-dsl): For simplicity, you can set your stream to retain data for a specific number of days. Setting a specific or indefinite retention period stores data in the hot phase for best indexing and search performance.
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

Wired streams follow a hierarchical structure that supports inheritance. A child stream can inherit the lifecycle of its nearest ancestor that has a set ILM or retention period policy. This lets you define a single lifecycle policy higher in the hierarchy, and Streams automatically applies it to all relevant descendants.

When the ancestor’s lifecycle is updated, Streams cascades the change to all child streams that inherit it, keeping everything in sync.

### Set a specific retention period [streams-retention-dsl]
The **Retention period** is the minimum number of days after which the data is deleted. To set data retention to a specific time period:

1. Under **Retention**, select **Edit data retention**.
1. Turn off **Inherit from index template** or **parent stream**, if on.
1. Select **Custom period**.
1. Set the period of time that you want to retain data for this stream.

To define a global default retention policy, refer to [project settings](../../../../deploy-manage/deploy/elastic-cloud/project-settings.md).

### Follow an ILM policy [streams-retention-ilm]
```{applies_to}
serverless: unavailable
stack: preview 9.1, ga 9.2
```
[ILM policies](../../../../manage-data/lifecycle/index-lifecycle-management.md) let you automate and standardize data retention across Streams and other data streams.

To have your streams follow an existing policy:

1. Under **Retention**, select **Edit data retention**.
1. Turn off **Inherit from index template** or **parent stream**, if on.
1. Select **ILM policy**, then select a pre-defined ILM policy from the list.

If the policy you want doesn't exist, create a new ILM policy. Refer to [Configure a lifecycle policy](../../../../manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) for more information.

## Set failure store data retention

A [failure store](../../../../manage-data/data-store/data-streams/failure-store.md) is a secondary set of indices inside a data stream, dedicated to storing failed documents.

You can enable failure stores from the **Retention** tab by selecting **Enable failure store**. This opens the failure store configuration for your stream. From here, you can set the retention period