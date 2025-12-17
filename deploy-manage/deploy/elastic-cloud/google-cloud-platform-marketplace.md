---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-billing-gcp.html
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Google Cloud Platform Marketplace [ec-billing-gcp]

Subscribe to {{ecloud}} directly from the Google Cloud Platform (GCP). You then have the convenience of viewing your {{ecloud}} subscription as part of your GCP bill, and you do not have to supply any additional credit card information to Elastic. Your investment in Elastic draws against your cloud purchase commitment.

Some differences exist when you subscribe to {{ecloud}} through the GCP Marketplace:

* New {{ecloud}} customers obtain a 7-day trial period. During this period, you can use a single deployment and three projects of {{ecloud}}. After this period, usage-based billing starts, unless you delete your cloud resources. Note that once customers unsubscribe from the GCP offer, their trial will end immediately. Even if they resubscribe, they will not be able to resume the trial.
* Pricing for an {{ecloud}} subscription through the GCP Marketplace follows the pricing outlined on the [{{ecloud}}](https://console.cloud.google.com/marketplace/product/elastic-prod/elastic-cloud) page in the GCP Marketplace. Pricing is based the {{ecloud}} [billing dimensions](../../cloud-organization/billing.md#pricing-model).
* To access your billing information at any time go to **Account & Billing**. You can also go to **Account & Billing** and then **Usage** to view your usage hours and units per hour.

::::{important} 
Only one {{ecloud}} organization can be subscribed through GCP Marketplace per GCP billing account.
::::


To subscribe to {{ecloud}} through the GCP Marketplace:

1. Log in to your Google Cloud Platform account.
2. Go to the [{{ecloud}}](https://console.cloud.google.com/marketplace/product/elastic-prod/elastic-cloud) page in the GCP Marketplace.
3. On the {{ecloud}} page select **Subscribe**, where you will be directed to another page. There is only one plan—the Elastic plan—and it’s pre-selected. The billing account you are logged into will be pre-selected for this purchase, though you can change it at this time.
4. Accept the terms of service (TOS) and select **Subscribe**.
5. When you are presented with a pop-up that specifies that "Your order request has been sent to Elastic" choose **Sign up with Elastic** to continue.
6. After choosing to sign up, a new window will appear. Do one of the following:

    * Create a new, unique user account for an {{ecloud}} {{ecloud}} organization.
    * Log in with an existing user account that’s associated with an {{ecloud}} trial. This links the billing account used for the purchase on GCP Marketplace to the existing Elastic organization.

7. After signing up, check your inbox to verify the email address you signed up with. Upon verification, you will be asked to create a password, and once created your organization will be set up and you will be logged into it.

    ::::{note} 
    Immediately after your first login to {{ecloud}} you may briefly see a banner on the {{ecloud}} user console saying that your account is disconnected. There is sometimes a short delay in activation, but refreshing the page is generally enough time to allow its completion. If this issue persists, contact support.
    ::::


    You are ready to [create your first deployment](create-an-elastic-cloud-hosted-deployment.md).


If you plan to use {{ech}} and have existing deployments that you want to migrate to your new marketplace account, we recommend using a custom repository to take a snapshot. Then restore that snapshot to a new deployment in your new marketplace account. Check [Snapshot and restore with custom repositories](../../tools/snapshot-and-restore/elastic-cloud-hosted.md) for details.

::::{tip} 
Your new account is automatically subscribed to the Enterprise subscription level. You can [change your subscription level](../../cloud-organization/billing/manage-subscription.md).
::::



## Changes to your billing account [ec-billing-gcp-account-change] 

::::{important} 
To prevent downtime, do not remove the currently used billing account before the switch to the new billing account has been confirmed by Elastic.
::::


{{ecloud}} subscriptions through GCP Marketplace are associated with a GCP billing account.  In order to change the billing account associated with an {{ecloud}} organization:

* for customers under a Private Offer contract: reach out to Elastic support and provide the GCP Billing Account, as well as the contact of any reseller information for approval.
* for pay-as-you-go customers: you need to have purchased and subscribed to {{ecloud}} on the new billing account using the details above—but do not create a new Elastic user or organization (that is, you can skip Steps 5 and 6 in the subscription instructions, above). Once you successfully subscribed with the new billing account, you can contact Elastic support and provide the new billing account ID you wish to move to, which you can find from [GCP’s billing page](https://console.cloud.google.com/billing). The ID is in the format `000000-000000-000000`.

If you cancel your {{ecloud}} order on GCP through the [marketplace orders page](https://console.cloud.google.com/marketplace/orders) before the switch to the new billing account has been done, any running deployments will immediately enter a degraded state known as maintenance mode and they will be scheduled for termination in five days.

If you already unsubscribed before the new billing account has been set up, you can subscribe again from the previously used billing account, which will cancel the termination and restore the deployments to a functional state.


## Native GCP integrations [ec-gcp-marketplace-native] 

You can ingest data from Google Pub/Sub to the {{stack}} very easily from the Google Cloud Console. You can use the [Metricbeat Google Cloud Platform module](../../../solutions/observability/cloud/monitor-google-cloud-platform-gcp.md) or the [GCP Dataflow Templates](../../../solutions/observability/cloud/gcp-dataflow-templates.md).

