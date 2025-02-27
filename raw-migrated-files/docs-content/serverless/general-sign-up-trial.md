# Sign up for Elastic Cloud [general-sign-up-trial]

The following page provides information on how to sign up for an Elastic Cloud Serverless account, for information on how to sign up for hosted deployments, see [{{ech}} - How do i sign up?](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md).


## Trial features [general-sign-up-trial-what-is-included-in-my-trial]

Your free 14-day trial includes:

**One hosted deployment**

A deployment lets you explore Elastic solutions for Search, Observability, and Security. Trial deployments run on the latest version of the Elastic Stack. They includes 8 GB of RAM spread out over two availability zones, and enough storage space to get you started. If you’re looking to evaluate a smaller workload, you can scale down your trial deployment. Each deployment includes Elastic features such as Maps, SIEM, machine learning, advanced security, and much more. You have some sample data sets to play with and tutorials that describe how to add your own data.

To learn more about Elastic Cloud Hosted, check our [{{ech}} documentation](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md).

**One serverless project**

Serverless projects package Elastic Stack features by type of solution:

* [{{es}}](../../../solutions/search.md)
* [Observability](../../../solutions/observability.md)
* [Security](../../../solutions/security/elastic-security-serverless.md)

When you create a project, you select the project type applicable to your use case, so only the relevant and impactful applications and features are easily accessible to you.

::::{note}
During the trial period, you are limited to one active hosted deployment and one active serverless project at a time. When you subscribe, you can create additional deployments and projects.

::::



## Trial limitations [general-sign-up-trial-what-limits-are-in-place-during-a-trial]

During the free 14 day trial, Elastic provides access to one hosted deployment and one serverless project. If all you want to do is try out Elastic, the trial includes more than enough to get you started. During the trial period, some limitations apply.

**Hosted deployments**

* You can have one active deployment at a time
* The deployment size is limited to 8GB RAM and approximately 360GB of storage, depending on the specified hardware profile
* Machine learning nodes are available up to 4GB RAM
* Custom {{es}} plugins are not enabled

To learn more about Elastic Cloud Hosted, check our [{{ech}} documentation](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md).

**Serverless projects**

* You can have one active serverless project at a time.
* Search Power is limited to 100. This setting only exists in {{es-serverless}} projects
* Search Boost Window is limited to 7 days. This setting only exists in {{es-serverless}} projects
* Scaling is limited for serverless projects in trials. Failures might occur if the workload requires memory or compute beyond what the above search power and search boost window setting limits can provide.

**Remove limitations**

Subscribe to [Elastic Cloud](/deploy-manage/cloud-organization/billing/add-billing-details.md) for the following benefits:

* Increased memory or storage for deployment components, such as {{es}} clusters, machine learning nodes, and APM server.
* As many deployments and projects as you need.
* Third availability zone for your deployments.
* Access to additional features, such as cross-cluster search and cross-cluster replication.

You can subscribe to Elastic Cloud at any time during your trial. [Billing](../../../deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md) starts when you subscribe. To maximize the benefits of your trial, subscribe at the end of the free period. To monitor charges, anticipate future costs, and adjust your usage, check your [account usage](/deploy-manage/cloud-organization/billing/monitor-analyze-usage.md) and [billing history](/deploy-manage/cloud-organization/billing/view-billing-history.md).


## Get started with your trial [general-sign-up-trial-how-do-i-get-started-with-my-trial]

Start by checking out some common approaches for [moving data into Elastic Cloud](/manage-data/ingest.md).


## Maintain access to your trial projects and data [general-sign-up-trial-what-happens-at-the-end-of-the-trial]

When your trial expires, the deployment and project that you created during the trial period are suspended until you subscribe to [Elastic Cloud](/deploy-manage/cloud-organization/billing/add-billing-details.md). When you subscribe, you are able to resume your deployment and serverless project, and regain access to the ingested data. After your trial expires, you have 30 days to subscribe. After 30 days, your deployment, serverless project, and ingested data are permanently deleted.

If you’re interested in learning more ways to subscribe to Elastic Cloud, don’t hesitate to [contact us](https://www.elastic.co/contact).


## Sign up through a marketplace [general-sign-up-trial-how-do-i-sign-up-through-a-marketplace]

If you’re interested in consolidated billing, subscribe from the AWS Marketplace, which allows you to skip the trial period and connect your AWS Marketplace email to your unique Elastic account. For a list of regions supported, see [Regions](../../../deploy-manage/deploy/elastic-cloud/regions.md).

::::{note}
Serverless projects are only available for AWS Marketplace. Support for GCP Marketplace and Azure Marketplace will be added in the near future.

::::
