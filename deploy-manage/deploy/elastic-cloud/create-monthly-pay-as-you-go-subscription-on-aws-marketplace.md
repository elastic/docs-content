---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-aws-marketplace-conversion.html
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
---

# Create a monthly pay-as-you-go subscription on AWS Marketplace [ec-aws-marketplace-conversion]

When subscribing to an annual prepaid subscription to {{ecloud}} on AWS Marketplace, follow these instructions to obtain a separate pay-as-you-go subscription. This subscription will allow us to continue your {{ecloud}} service through the Marketplace once the contract is expired. You will not get charged twice for the usage under the annual contract.

1. Log in to AWS under the same Account ID that you will use to accept the Annual Private Offer.
2. Go to the [AWS Marketplace subscription page for {{ecloud}} pay-as-you-go](https://aws.amazon.com/marketplace/saas/ordering?productId=bb253a6c-e775-4634-bdf0-17bd56a69c36&offerId=b2uzdkwqj7177fqhm39o4snxy).
3. Click **Subscribe** to create an AWS Marketplace subscription under the selected AWS Account.

:::{image} /deploy-manage/images/cloud-aws-subscribe-button.png
:alt: Subscribe to {{ecloud}} on AWS Marketplace
:::

You should now see the monthly *Pay as you go* subscription for {{ecloud}} in your AWS **Manage subscriptions** page.

From the top-right corner, you can check that the Account ID is the same account that has your {{ecloud}} annual subscription.

:::{image} /deploy-manage/images/cloud-aws-mp-manage-subscriptions.png
:alt: Account ID on top-right menu
:::
