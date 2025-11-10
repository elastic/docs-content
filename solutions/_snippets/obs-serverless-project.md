An {{obs-serverless}} project allows you to run {{obs-serverless}} in an autoscaled and fully-managed environment, where you don’t have to manage the underlying {{es}} cluster or {{kib}} instances.

::::{dropdown} Steps for creating a project
:::{note}
The **Admin** role or higher is required to create projects. Refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/manage-users.md#general-assign-user-roles).
:::

1. Navigate to [cloud.elastic.co](https://cloud.elastic.co/) and log in to your account, or create one.
2. Select **Create serverless project**.
3. Under **Elastic for Observability**, select **Next**.
4. Enter a name for your project and select **Observability Complete**. 
6. (Optional) Select **Edit settings** to change your project settings:

    * **Cloud provider**: The cloud platform where you’ll deploy your project. We currently support Amazon Web Services (AWS).
    * **Region**: The [region](/deploy-manage/deploy/elastic-cloud/regions.md) where your project will live.

7. Select **Create project**. It takes a few minutes to create your project.
8. When the project is ready, click **Continue**.
