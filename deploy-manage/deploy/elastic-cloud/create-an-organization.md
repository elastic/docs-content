---
navigation_title: Sign up
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-getting-started-trial.html
  - https://www.elastic.co/guide/en/serverless/current/general-sign-up-trial.html
  - https://www.elastic.co/guide/en/cloud/current/ec-getting-started-existing-email.html
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Sign up and create an organization

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/336

% Scope notes: merge

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/cloud/cloud/ec-getting-started-trial.md
% - [ ] ./raw-migrated-files/docs-content/serverless/general-sign-up-trial.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-getting-started-existing-email.md

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$general-sign-up-trial-what-is-included-in-my-trial$$$

To sign up:

1. Go to the [{{ecloud}} Sign Up](https://cloud.elastic.co/registration?page=docs&placement=docs-body) page.
2. Choose one of the available sign up methods. You can register with your email address and a password, use a Google or Microsoft account, or [subscribe from a Marketplace](../../../deploy-manage/deploy/elastic-cloud/subscribe-from-marketplace.md).

:::{note}
You can only belong to one {{ecloud}} organization at a time. If you want to create or join another organization, you must leave the previous one or use a different email address.
:::

When your first sign up, you create an organization and start with a trial license.

This organization is the umbrella for all of your {{ecloud}} resources, users, and account settings. Every organization has a unique identifier. Bills are invoiced according to the billing contact and details that you set for your organization. For more details on how to manage your organization, refer to [](/deploy-manage/cloud-organization.md).


## Trial information [general-sign-up-trial-what-is-included-in-my-trial]

Your free 14-day trial includes:

**One hosted deployment**

A deployment lets you explore Elastic solutions for Search, Observability, and Security. Trial deployments run on the latest version of the {{stack}}. They includes 8 GB of RAM spread out over two availability zones, and enough storage space to get you started. If you’re looking to evaluate a smaller workload, you can scale down your trial deployment. Each deployment includes Elastic features such as Maps, SIEM, machine learning, advanced security, and much more. You have some sample data sets to play with and tutorials that describe how to add your own data.

For more information, check the [{{ech}} documentation](cloud-hosted.md).

**One serverless project**

Serverless projects package {{stack}} features by type of solution:

* [{{es}}](../../../solutions/search.md)
* [Observability](../../../solutions/observability.md)
* [Security](../../../solutions/security/elastic-security-serverless.md)

When you create a project, you select the project type applicable to your use case, so only the relevant and impactful applications and features are easily accessible to you.

For more information, check the [{{serverless-short}} documentation](serverless.md).


### Trial limitations [general-sign-up-trial-what-limits-are-in-place-during-a-trial]

During the free 14 day trial, Elastic provides access to one hosted deployment and one serverless project. If all you want to do is try out Elastic, the trial includes more than enough to get you started. During the trial period, some limitations apply.

**Hosted deployments**

* You can have one active deployment at a time
* The deployment size is limited to 8GB RAM and approximately 360GB of storage, depending on the specified hardware profile
* Machine learning nodes are available up to 4GB RAM
* Custom {{es}} plugins are not enabled

For more information, check the [{{ech}} documentation](cloud-hosted.md).

**Serverless projects**

* You can have one active serverless project at a time.
* Search Power is limited to 100. This setting only exists in {{es-serverless}} projects
* Search Boost Window is limited to 7 days. This setting only exists in {{es-serverless}} projects
* Scaling is limited for serverless projects in trials. Failures might occur if the workload requires memory or compute beyond what the above search power and search boost window setting limits can provide.

**Remove limitations**

Subscribe to [{{ecloud}}](/deploy-manage/cloud-organization/billing/add-billing-details.md) for the following benefits:

* Increased memory or storage for deployment components, such as {{es}} clusters, machine learning nodes, and APM server.
* As many deployments and projects as you need.
* Third availability zone for your deployments.
* Access to additional features, such as cross-cluster search and cross-cluster replication.

You can subscribe to {{ecloud}} at any time during your trial. [Billing](../../../deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md) starts when you subscribe. To maximize the benefits of your trial, subscribe at the end of the free period. To monitor charges, anticipate future costs, and adjust your usage, check your [account usage](/deploy-manage/cloud-organization/billing/monitor-analyze-usage.md) and [billing history](/deploy-manage/cloud-organization/billing/view-billing-history.md).


### Get started with your trial [general-sign-up-trial-how-do-i-get-started-with-my-trial]

Start by checking out some common approaches for [moving data into {{ecloud}}](/manage-data/ingest.md).


### Maintain access to your trial projects and data [general-sign-up-trial-what-happens-at-the-end-of-the-trial]

When your trial expires, the deployment and project that you created during the trial period are suspended until you subscribe to [{{ecloud}}](/deploy-manage/cloud-organization/billing/add-billing-details.md). When you subscribe, you are able to resume your deployment and serverless project, and regain access to the ingested data. After your trial expires, you have 30 days to subscribe. After 30 days, your deployment, serverless project, and ingested data are permanently deleted.

If you’re interested in learning more ways to subscribe to {{ecloud}}, don’t hesitate to [contact us](https://www.elastic.co/contact).


## How do I get help? [ec_how_do_i_get_help]

We’re here to help. If you have any questions feel free to reach out to [Support](https://cloud.elastic.co/support).
