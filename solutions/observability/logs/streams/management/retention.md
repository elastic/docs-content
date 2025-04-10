---
applies_to:
    serverless: tp
---

# Data retention

Use the **Data retention** tab to manage the retention of your stream and get insight into the ingestion and size of your data.

![alt text](<retention.png>)

**Ingestion**: Estimated ingestion per day and month calculated based on the size of all data in the stream and divided by the age of the stream. This is an estimate, and the actual ingestion may vary.

**Size**: The total size of the data in the stream. This is all data currently in the stream.

**Ingestion Rate**: Estimated ingestion rate per time bucket. The bucket interval is dynamic and adjusts based on the selected time range. The ingestion rate is calulated based on the average document size in a stream, multiplied by the number of documents in the bucket. This is an estimate, and the actual ingestion rate may vary.

## Change retention
Click the `Edit data retention` button to change the retention of your Stream. The retention is set in days. The retention is the minimum number of days after which the data is deleted. You can define a global default retention in your [project settings](../../../../../deploy-manage/deploy/elastic-cloud/project-settings.md).