---
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Configure the DNS histogram

The DNS histogram (**Top domains by dns.question.registered_domain**) on the **Network** page helps you visualize domain activity in your environment. If you're using {{elastic-defend}}, you may need to add the `dns.question.registered_domain` field so that DNS data appears correctly.

If the DNS histogram is empty, follow these steps to populate the data.

## Add the `dns.question.name` field

Add the `dns.question.name` field to the Events table to confirm that DNS data is available.

1. Go to the **Network** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). 
2. Select the **Events** tab.
3. In the Events table, click **Fields**, then add the `dns.question.name` field.

## Create a custom ingest pipeline

Create an ingest pipeline that extracts registered domains (for example, `example.com`) from full DNS query names (for example, `www.example.com`).

1. Go to the **Ingest Pipelines** page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and select **Create pipeline → New pipeline**.
2. On the **Create pipeline** page, set the pipeline name to `logs-endpoint.events.network@custom`.
3. Click **Add a processor**. In the **Add processor** flyout, configure the following:
   1. From the **Processor** dropdown, select **Registered domain**.
   2. Under **Field**, enter `dns.question.name`.
   3. Under **Target field (optional)**, enter `dns.question.registered_domain`.
   4. Turn **Ignore missing** on.
   5. Under **Condition (optional)**, enter `ctx?.dns?.question?.name != null`.
   6. Turn **Ignore failures for this processor** on.
   7. Select **Add processor**.
4. Select **Create pipeline**. This custom pipeline is automatically picked up by the existing `logs-endpoint.events.network-<version>` pipeline.

## Add the `dns.question.registered_domain` field

Add the `dns.question.registered_domain` field to the Events table to verify that the ingest pipeline processes DNS queries correctly.

1. Go back to the Events table on the **Network** page.
2. Click **Fields**, then add the `dns.question.registered_domain` field.

After you configure the DNS histogram, it will show domain activity grouped by registered domain, allowing you to identify the top domains queried in your environment.
