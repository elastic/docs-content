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


To sign up:

1. Go to the [{{ecloud}} Sign Up](https://cloud.elastic.co/registration?page=docs&placement=docs-body) page.
2. Choose one of the available sign up methods. You can register with your email address and a password, use a Google or Microsoft account, or [subscribe from a Marketplace](../../../deploy-manage/deploy/elastic-cloud/subscribe-from-marketplace.md).

:::{note}
* You can only belong to one {{ecloud}} organization at a time. If you want to create or join another organization, you must [leave the previous one](/cloud-account/join-or-leave-an-organization.md#ec-leave-organization) or use a different email address.
* An email address can’t be used for more than one {{ecloud}} account. To make the email address available for a new account, you can [remove it from your existing account](/cloud-account/update-your-email-address.md#sign-up-existing).
:::

When you first sign up, you create an organization and start with a trial license.

This organization is the umbrella for all of your {{ecloud}} resources, users, and account settings. Every organization has a unique identifier. Bills are invoiced according to the billing contact and details that you set for your organization. For more details on how to manage your organization, refer to [](/deploy-manage/cloud-organization.md).


## Trial information [general-sign-up-trial-what-is-included-in-my-trial]

Your free 14-day trial includes:

**One hosted deployment**

A deployment lets you explore Elastic solutions for Search, Observability, and Security. Trial deployments run on the latest version of the {{stack}}. They includes 8 GB of RAM spread out over two availability zones, and enough storage space to get you started. If you’re looking to evaluate a smaller workload, you can scale down your trial deployment. Each deployment includes Elastic features such as Maps, SIEM, machine learning, advanced security, and much more. You have some sample data sets to play with and tutorials that describe how to add your own data.

For more information, check the [{{ech}} documentation](cloud-hosted.md).

**Three {{serverless-short}} project**

{{serverless-short}} projects package {{stack}} features by type of solution:

* [{{es}}](../../../solutions/search.md)
* [Observability](../../../solutions/observability.md)
* [Security](../../../solutions/security.md)

When you create a project, you select the project type applicable to your use case, so only the relevant and impactful applications and features are easily accessible to you.

For more information, check the [{{serverless-short}} documentation](serverless.md).

### Trial limitations [general-sign-up-trial-what-limits-are-in-place-during-a-trial]

:::{include} ../_snippets/trial-limitations.md
:::

### Get started with your trial [general-sign-up-trial-how-do-i-get-started-with-my-trial]

Start by checking out some common approaches for [moving data into {{ecloud}}](/manage-data/ingest.md).


### Maintain access to your trial projects and data [general-sign-up-trial-what-happens-at-the-end-of-the-trial]

When your trial expires, the deployment and projects that you created during the trial period are suspended until you subscribe to [{{ecloud}}](/deploy-manage/cloud-organization/billing/add-billing-details.md). When you subscribe, you are able to resume your deployment and {{serverless-short}} projects, and regain access to the ingested data. After your trial expires, you have 30 days to subscribe. After 30 days, your deployment, {{serverless-short}} projects, and ingested data are permanently deleted.

If you’re interested in learning more ways to subscribe to {{ecloud}}, don’t hesitate to [contact us](https://www.elastic.co/contact).


## How do I get help? [ec_how_do_i_get_help]

We’re here to help. If you have any questions feel free to reach out to [Support](https://cloud.elastic.co/support).
