---
navigation_title: "Create an Observability project"
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-create-an-observability-project.html
---

% Serverless only

# Create an observability project [observability-create-an-observability-project]


::::{admonition} Required role
:class: note

The **Admin** role or higher is required to create projects. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/manage-users.md#general-assign-user-roles).

::::


An {{obs-serverless}} project allows you to run {{obs-serverless}} in an autoscaled and fully-managed environment, where you don’t have to manage the underlying {{es}} cluster or {{kib}} instances.

1. Navigate to [cloud.elastic.co](https://cloud.elastic.co/) and log in to your account.
2. Within **Serverless projects**, click **Create project**.
3. Under **Observability**, click **Next**.
4. Enter a name for your project.
5. (Optional) Click **Edit settings** to change your project settings:

    * **Cloud provider**: The cloud platform where you’ll deploy your project. We currently support Amazon Web Services (AWS).
    * **Region**: The [region](../../../deploy-manage/deploy/elastic-cloud/regions.md) where your project will live.

6. Click **Create project**. It takes a few minutes to create your project.
7. When the project is ready, click **Continue**.

From here, you can start adding logs and other observability data.

::::{tip}
To return to the onboarding page later, select **Add data** from the main menu.

::::



## Next steps [observability-create-an-observability-project-next-steps]

Learn how to add data to your project and start using {{obs-serverless}} features:

* [Get started with system logs](../logs/get-started-with-system-logs.md)
* [Get started with traces and APM](../apps/get-started-with-apm.md)
* [Get started with system metrics](../infra-and-hosts/get-started-with-system-metrics.md)
