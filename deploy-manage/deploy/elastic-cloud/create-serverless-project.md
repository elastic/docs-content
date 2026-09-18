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

:::{include} /deploy-manage/deploy/_snippets/create-serverless-project-intro.md
:::

## Before you begin

* Decide which project type you might need before you create the project. You'll select one of the following types during setup:

    * {{es}}
    * {{vectordb}}
    * {{observability}}
    * Security

  To match a type to your use case, review this [project comparison table](/deploy-manage/deploy/elastic-cloud/serverless.md#choose-a-project-type).

* You can't convert a project to a different type later. If you choose the wrong type, create another project. When you no longer need a project, [delete it](/deploy-manage/uninstall/delete-a-cloud-deployment.md#serverless) so it doesn't continue to incur charges.

* You can have up to 500 {{serverless-short}} projects in your organization. This limit applies whether you create projects in the {{ecloud}} console or with the API. If you reach the limit, you'll get an error when you try to create another project. To request an increase, [contact Elastic Support](/troubleshoot/index.md#contact-us).

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

