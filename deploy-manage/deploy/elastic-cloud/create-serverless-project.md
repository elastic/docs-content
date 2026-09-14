---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/serverless-get-started.html
applies_to:
  serverless:
products:
  - id: cloud-serverless
navigation_title: Create a serverless project
---

# Create an {{serverless-full}} project [serverless-get-started]

There are a few options to create a serverless project:

* If you are a new user, [sign up for a free 14-day trial](https://cloud.elastic.co/serverless-registration) to create a serverless project. For more information about the {{ecloud}} trials, refer to [Trial features](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial).
* If you are an existing customer, [log in to {{ecloud}}](https://cloud.elastic.co/login) and [create a project in the {{ecloud}} console](#create-project-console). The `admin` predefined role or an equivalent custom role is required to create projects. Refer to [](/deploy-manage/users-roles/cloud-organization/user-roles.md).
* You can also [create and manage projects](/deploy-manage/deploy/elastic-cloud/manage-serverless-projects-using-api.md) using the [{{serverless-full}} API]({{cloud-serverless-apis}}).

Each of these options counts toward the same organization limit: you can have up to 500 {{serverless-short}} projects. If you reach this limit, you'll get an error when you try to create another project. To request an increase, [contact Elastic Support](/troubleshoot/index.md#contact-us).

## Create a project in the {{ecloud}} console [create-project-console]

The steps to create a {{serverless-short}} project are the same regardless of which project type you select.

1. On the {{ecloud}} home page, find the **Serverless projects** panel and select **Create project** .
2. Select a project type that matches your use case, then select **Next**. If you're not sure which type to choose, refer to [{{serverless-full}}](serverless.md#get-started).
3. Enter a name for your project.
4. Select a cloud provider and region. For available regions, refer to [](/deploy-manage/deploy/elastic-cloud/regions.md).

    Depending on the project type, you can also configure additional settings, such as a feature tier. For details, refer to [](/deploy-manage/deploy/elastic-cloud/project-settings.md).
5. Select **Create project**. It takes a few minutes to create your project.
6. When the project is ready, select **Continue** to open it. You might need to log in to {{ecloud}} again.

:::{tip} 
If {{kib}} loads as a blank page, check that your firewall, proxy, or secure web gateway allows access to `kibana.estccdn.com` and `cloud.elastic.co`. For the full list of required domains, refer to [Browser access requirements](/deploy-manage/deploy/elastic-cloud.md#browser-access).
:::

