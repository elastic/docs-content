---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/security-create-project.html
applies_to:
  serverless:
    security: all
---

# Create a Security project [security-create-project]

A serverless project allows you to run {{elastic-sec}} in an autoscaled and fully managed environment, where you don’t have to manage the underlying {{es}} cluster and {{kib}} instances.


## Create project [security-create-project-create-project]

Use your {{ecloud}} account to create a fully managed {{sec-serverless}} project:

1. Navigate to [cloud.elastic.co](https://cloud.elastic.co/).
2. Log in to your {{ecloud}} account and select **Create project** from the **Serverless projects** panel.
3. Select **Next** from the **Security** panel.
4. Edit your project settings (click **Edit settings** to access all settings).

    * **Name**: A unique name for your project.
    * **Cloud provider**: The cloud platform where you’ll deploy your project. We currently support Amazon Web Services (AWS).
    * **Region**: The cloud platform’s [region](../../../deploy-manage/deploy/elastic-cloud/regions.md) where your project will live.

        You can also check [the pricing details](https://www.elastic.co/pricing/serverless-security) to see how you consume {{sec-serverless}}.

5. Select **Create project**. It takes a few minutes before your project gets created.
6. Once the project is ready, select **Continue** to open the **Get started** page (you might need to log in to {{ecloud}} again).

    From here, you can learn more about {{elastic-sec}} features and start setting up your workspace.
