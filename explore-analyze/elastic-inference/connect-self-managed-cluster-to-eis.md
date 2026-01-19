---
navigation_title: EIS for self-managed clusters
applies_to:
  stack: ga 9.3
  deployment:
    self: ga
    ece: ga
    eck: ga
---

# EIS for self-managed clusters

Elastic {{infer-cap}} Service (EIS) for self-managed clusters is available through [Cloud Connect](/deploy-manage/cloud-connect.md), which enables you to use {{ecloud}} services in your self-managed cluster without having to install and maintain their infrastructure yourself. This allows you to use AI-powered features like semantic search and text embeddings without deploying and managing {{ml}} nodes.

## Prerequisites

Before you can use EIS with your self-managed cluster, ensure you meet the following requirements:

* Your cluster is running {{es}} 9.3 or later
* Your self-managed cluster is on an [Enterprise self-managed license](https://www.elastic.co/subscriptions) or an [active self-managed trial](https://cloud.elastic.co/registration)
* You have an {{ecloud}} account with either an [active Cloud Trial](https://cloud.elastic.co/registration) or [billing information configured](/deploy-manage/cloud-organization/billing/add-billing-details.md)

## Set up EIS with Cloud Connect

To set up EIS for your self-managed cluster with Cloud Connect:

1. In your self-managed cluster, navigate to the **Cloud Connect** page using the [search bar](/explore-analyze/find-and-organize/find-apps-and-objects.md).

   :::{image} /explore-analyze/images/cloud-connect-eis.png
   :screenshot:
   :alt: Screenshot showing Cloud Connect page
   :::

2. Sign up or log in to {{ecloud}} and get the Cloud Connect API key:

   - If you already have an {{ecloud}} account, click **Log in**.
   - If you don’t have an account yet, click **Sign up** and follow the prompts to create your account and start a free trial.

3. Copy the Cloud Connect API key, paste it into your self-managed cluster's Cloud Connect page, then click **Connect**.

4. On the **Cloud connected services** page, click **Connect** for Elastic {{infer}} Service.


## Regions

For information about EIS regions and request routing, refer to the [Region and hosting](/explore-analyze/elastic-inference/eis.md#eis-regions).

## Token consumption and billing

EIS is billed per million tokens. For details on pricing and usage tracking, refer to [Pricing](/explore-analyze/elastic-inference/eis.md#pricing) and [Monitor your token usage](/explore-analyze/elastic-inference/eis.md#monitor-your-token-usage).

