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

:::{include} /deploy-manage/deploy/_snippets/create-serverless-project-intro.md
:::

## Create a project in the {{ecloud}} console [create-project-console]

The steps to create a {{serverless-short}} project are the same regardless of which project type you select.

1. On the {{ecloud}} home page, find the **Serverless projects** panel and select **Create project** .
2. Select a project type that matches your use case, then select **Next**. If you're not sure which type to choose, refer to [{{serverless-full}}](serverless.md#get-started).
3. Enter a name for your project.
4. Select a cloud provider and region. For available regions, refer to [](/deploy-manage/deploy/elastic-cloud/regions.md).

    Depending on the project type, you can also configure additional settings, such as a feature tier. For details, refer to [](/deploy-manage/deploy/elastic-cloud/project-settings.md).
5. Select **Create project**. It takes a few minutes to create your project.
6. When the project is ready, select **Continue** to open it. You might need to log in to {{ecloud}} again.

:::{include} /deploy-manage/deploy/_snippets/serverless-kibana-blank-page.md
:::

