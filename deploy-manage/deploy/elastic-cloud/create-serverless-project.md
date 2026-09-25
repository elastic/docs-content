---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/serverless-get-started.html
applies_to:
  serverless:
products:
  - id: cloud-serverless
navigation_title: Create a serverless project
type: how-to
---

# Create an {{serverless-full}} project [serverless-get-started]

There are a few options to create a serverless project:

* If you are a new user, [sign up for a free 14-day trial](https://cloud.elastic.co/serverless-registration) to create a serverless project. For more information about the {{ecloud}} trials, refer to [Trial features](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial).
* If you are an existing customer, [log in to {{ecloud}}](https://cloud.elastic.co/login) and [create a project in the {{ecloud}} console](#create-project-console). The `admin` predefined role or an equivalent custom role is required to create projects. Refer to [](/deploy-manage/users-roles/cloud-organization/user-roles.md).

    :::{note}
    Existing customers can also [create and manage projects](/deploy-manage/deploy/elastic-cloud/manage-serverless-projects-using-api.md) using the [{{serverless-full}} API]({{cloud-serverless-apis}}) or the {applies_to}`serverless: preview` [Elastic CLI](cli://index.md).
    :::

## Before you begin

Decide which project type you might need before you create the project. You'll select one of the following types during setup:

* {{es}}
* {{vectordb}}
* {{observability}}
* Security

To match a type to your use case, review this [project comparison table](/deploy-manage/deploy/elastic-cloud/serverless.md#choose-a-project-type).
  
You can't convert a project to a different type later. If you choose the wrong type, create another project. When you no longer need a project, [delete it](/deploy-manage/uninstall/delete-a-cloud-deployment.md#serverless) so it doesn't continue to incur charges.

You can have up to 500 {{serverless-short}} projects in your organization. This limit applies whether you create projects in the {{ecloud}} console or with the API. If you reach the limit, you'll get an error when you try to create another project. To request an increase, [contact Elastic Support](/troubleshoot/index.md#contact-us).

## Create a project in the {{ecloud}} console [create-project-console]

The steps to create a {{serverless-short}} project are the same regardless of which project type you select.

1. On the {{ecloud}} home page, find the **Serverless projects** panel and select **Create project**.
2. Select a project type that matches your use case, then select **Next**. If you're not sure which type to choose, refer to our [project type comparison](serverless.md#get-started).
3. Enter a name for your project.
4. Select a cloud provider and region. For available regions, refer to [](/deploy-manage/deploy/elastic-cloud/regions.md).

    For {{sec-serverless}} and {{obs-serverless}} projects, you can also select a feature tier. For more information, review the [project features and add-ons](/deploy-manage/deploy/elastic-cloud/project-settings.md#project-features-add-ons) included in each feature tier.
5. Select **Create project**. It takes a few minutes to create your project.
6. When the project is ready, select **Continue** to open it. You might need to log in to {{ecloud}} again.

:::{tip}
If {{kib}} loads as a blank page, check that your firewall, proxy, or secure web gateway allows access to `kibana.estccdn.com` and `cloud.elastic.co`. For the full list of required domains, refer to [Browser access requirements](/deploy-manage/deploy/elastic-cloud.md#browser-access).
:::

