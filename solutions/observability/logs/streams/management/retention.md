---
applies_to:
  serverless: preview
  stack: preview 9.1
---

# Manage data retention [streams-data-retention]

Use the **Data retention** tab on the **Manage stream** page to set how long your stream retains data and to get insight into your stream's data ingestion and storage size.

![Screenshot of the data retention UI](<../../../../images/logs-streams-retention.png>)

The **Data retention** page is made up of the following components that can help you determine how long you want your stream to retain data:

- **Retention period**: The minimum number of days after which the data is deleted
- **Source**: The origin of the data retention policy.
- **Last updated**: When data retention was last updated for the selected stream.
- **Ingestion**: Estimated ingestion per day and month, calculated based on the total size of all data in the stream  divided by the stream's age. This is an estimate, and the actual ingestion may vary.
- **Total doc count**: The total number of documents in the stream.
- **Ingestion Rate**: Estimated ingestion rate per time bucket. The bucket interval is dynamic and adjusts based on the selected time range. The ingestion rate is calculated using the average document size in the stream multiplied by the number of documents in each bucket. This is an estimate, and the actual ingestion rate may vary.
- **Policy summary**: {applies_to}`stack: preview 9.1` The amount of data ingested per phase (hot, warm, cold).

## Edit the data retention [streams-update-data-retention]
From any stream page, select **Edit data retention** to change how long your data stream retains data.

### Set a specific retention period
The **Retention period** is the minimum number of days after which the data is deleted. To set data retention to a specific time period:

1. Select **Edit data retention** → **Set specific retention days**.
1. From here, set the period of time you want to retain data for this stream.

To define a global default retention policy, refer to [project settings](../../../../../deploy-manage/deploy/elastic-cloud/project-settings.md).

### Follow an ILM policy
```{applies_to}
stack: ga 9.1
```
[ILM policies](../../../../../manage-data/lifecycle/index-lifecycle-management.md) let you automate and standardize data retention across streams and other data streams. To have your streams follow an existing policy:

1. Select **Edit data retention** → **Use a lifecycle policy**.
1. Select a pre-defined ILM policy from the list.

You can also create a new ILM policy. Refer to [Configure a lifecycle policy](../../../../../manage-data/lifecycle/index-lifecycle-management/configure-lifecycle-policy.md) for more information.