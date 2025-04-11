---
applies_to:
    serverless: preview
---

# Manage data retention [streams-data-retention]

Use the **Data retention** page under the **Management** tab to set how long your stream retains data and to get insight into your streams data ingestion and storage size.

![alt text](<retention.png>)

The **Data retention** page is made up of the following components that can help you determine how long you want your stream to retain data:

% this list doesn't show all of the components in the screenshot. Should we add the other components, or is the screenshot out of date?

- **Ingestion**: Estimated ingestion per day and month calculated based on the size of all data in the stream and divided by the age of the stream. This is an estimate, and the actual ingestion may vary.
- **Size**: The total size of the data in the stream. This is all data currently in the stream.
- **Ingestion Rate**: Estimated ingestion rate per time bucket. The bucket interval is dynamic and adjusts based on the selected time range. The ingestion rate is calulated based on the average document size in a stream, multiplied by the number of documents in the bucket. This is an estimate, and the actual ingestion rate may vary.

## Edit the data retention period [streams-update-data-retention]
Select `Edit data retention` to change how long data for your stream is retained. The **Retention period** is the minimum number of days after which the data is deleted.

To define a global default retention policy, refer to [project settings](../../../../../deploy-manage/deploy/elastic-cloud/project-settings.md).