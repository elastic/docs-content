An {{obs-serverless}} project allows you to run {{obs-serverless}} in an autoscaled, fully managed environment where you don’t have to manage the underlying {{es}} cluster or {{kib}} instances.

::::{dropdown} Steps for creating a project
:::{note}
You need permission to create {{obs-serverless}} projects. Refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/manage-users.md#general-assign-user-roles).
:::

1. Navigate to [cloud.elastic.co](https://cloud.elastic.co/) and log in to your account, or create one.
2. Select **Create serverless project**.
3. Select the Observability solution:

    * If the selector shows **Observe your applications & infrastructure**, select it and click **Continue**.
    * If the selector shows **Elastic for Observability**, select it and click **Next**.

4. Enter a project name and select **Observability Complete**.
5. Under **Settings**, select a **Cloud provider** and [**Region**](/deploy-manage/deploy/elastic-cloud/regions.md). Available providers include Amazon Web Services (AWS), Microsoft Azure, and Google Cloud. Availability varies by region and organization.
6. Click **Create serverless project**. It takes a few minutes to create your project.
7. When the project is ready, click **Open project**.
