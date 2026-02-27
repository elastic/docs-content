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

# Sign up

To get started with {{ecloud}}, sign up for an account:

1. Go to the [{{ecloud}} Sign Up](https://cloud.elastic.co/registration?page=docs&placement=docs-body) page.
2. Choose one of the available sign up methods. You can register with your email address and a password, use a Google or Microsoft account, or [subscribe from a Marketplace](../../../deploy-manage/deploy/elastic-cloud/subscribe-from-marketplace.md).

When you first sign up, you create an organization and start with a trial license.

An organization is the umbrella for all of your {{ecloud}} resources, users, and account settings. Every organization has a unique identifier. Bills are invoiced according to the billing contact and details that you set for your organization. A user can belong to multiple organizations, or be the owner of multiple organizations. For more details on how to manage your organizations, refer to [](/deploy-manage/cloud-organization.md).

## Trial information [general-sign-up-trial-what-is-included-in-my-trial]

When you create an organization, you start with a free 14-day trial. During this trial, you have access to the following:

% do we want to tell them that they have unlimited trials by creating multiple organizations?

**One hosted deployment**

A deployment lets you explore Elastic solutions for Search, Observability, and Security. Trial deployments run on the latest version of the {{stack}}. They includes 8 GB of RAM spread out over two availability zones, and enough storage space to get you started. If you’re looking to evaluate a smaller workload, you can scale down your trial deployment. Each deployment includes Elastic features such as Maps, SIEM, machine learning, advanced security, and much more. You have some sample data sets to play with and tutorials that describe how to add your own data.

For more information, check the [{{ech}} documentation](cloud-hosted.md).

**Three {{serverless-short}} projects**

{{serverless-short}} projects package {{stack}} features by type of solution:

* [{{es}}](../../../solutions/search.md)
* [Observability](../../../solutions/observability.md)
* [Security](../../../solutions/security.md)

When you create a project, you select the project type applicable to your use case, so the most relevant applications and features are surfaced for you from the start.

For more information, check the [{{serverless-short}} documentation](serverless.md).

### Trial limitations [general-sign-up-trial-what-limits-are-in-place-during-a-trial]

:::{include} ../_snippets/trial-limitations.md
:::

### Get started with your trial [general-sign-up-trial-how-do-i-get-started-with-my-trial]

Start by checking out some common approaches for [moving data into {{ecloud}}](/manage-data/ingest.md).

### Remove trial limitations

Subscribe to [{{ecloud}}](/deploy-manage/cloud-organization/billing/add-billing-details.md) for the following benefits:

* Increased memory or storage for deployment components, such as {{es}} clusters, machine learning nodes, and APM server.
* As many deployments and projects as you need.
* Third availability zone for your deployments.
* Access to additional features, such as {{ccs}} and {{ccr}}.

You can subscribe to {{ecloud}} at any time during your trial.
[Billing](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md) starts when you subscribe.
To maximize the benefits of your trial, subscribe at the end of the free period.
To monitor charges, anticipate future costs, and adjust your usage, check your [account usage](/deploy-manage/cloud-organization/billing/monitor-analyze-usage.md) and [billing history](/deploy-manage/cloud-organization/billing/view-billing-history.md).

### Maintain access to your trial projects and data [general-sign-up-trial-what-happens-at-the-end-of-the-trial]

When your trial expires, the deployment and projects that you created during the trial period are suspended until you subscribe to [{{ecloud}}](/deploy-manage/cloud-organization/billing/add-billing-details.md). When you subscribe, you are able to resume your deployment and {{serverless-short}} projects, and regain access to the ingested data. After your trial expires, you have 30 days to subscribe. After 30 days, your deployment, {{serverless-short}} projects, and ingested data are permanently deleted.

If you’re interested in learning more ways to subscribe to {{ecloud}}, don’t hesitate to [contact us](https://www.elastic.co/contact).

## How do I get help? [ec_how_do_i_get_help]

We’re here to help. If you have any questions feel free to reach out to [Support](https://cloud.elastic.co/support).
