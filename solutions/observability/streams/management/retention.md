---
navigation_title: Manage data retention
applies_to:
  serverless: ga
  stack: preview 9.1, ga 9.2
---

# Manage data retention for streams [streams-data-retention]

Use the **Retention** tab to set how long your stream retains data and to get insight into your stream's data ingestion and storage size.

The **Retention** tab contains the following components to help you determine how long you want your stream to retain data:

- **Retention**: The current retention policy, including the source of the policy.
- **Storage size**: The total size and number of documents in the stream.
- **Ingestion averages**: Estimated ingestion per day and month, calculated based on the total size of all data in the stream  divided by the stream's age.
- **ILM policy data tiers**: {applies_to}`stack: preview 9.1, ga 9.2` The amount of data in each data tier (**Hot**, **Warm**, **Cold**).
- **Ingestion over time**: Estimated ingestion rate per time bucket. The bucket interval is dynamic and adjusts based on the selected time range. The ingestion rate is calculated using the average document size in the stream multiplied by the number of documents in each bucket. This is an estimate, and the actual ingestion rate may vary.

For more information on data retention, refer to [Data stream lifecycle](../../../../manage-data/lifecycle/data-stream.md).

## Edit the data retention [streams-update-data-retention]
From the **Retention** tab, select **Edit data retention** to change how long your data stream retains data.

### Inherit from index template
When enabled, your stream uses the retention configuration from its index template.

### Set a specific retention period
The **Retention period** is the minimum number of days after which the data is deleted. To set data retention to a specific time period:

1. From the **Retention** tab, select **Edit data retention**.
1. Turn off **Inherit from index template** if enabled.
1. Select **Custom period**.
1. Set the period of time you want to retain data for this stream.

To define a global default retention policy, refer to [project settings](../../../../deploy-manage/deploy/elastic-cloud/project-settings.md).

### Follow an ILM policy
```{applies_to}
stack: preview 9.1, ga 9.2
```
[ILM policies](../../../../manage-data/lifecycle/index-lifecycle-management.md) let you automate and standardize data retention across streams and other data streams. To have your streams follow an existing policy:

1. From the **Retention** tab, select **Edit data retention**.
1. Select a pre-defined ILM policy from the list.

You can also create a new ILM policy. Refer to [Configure a lifecycle policy](../../../../manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) for more information.