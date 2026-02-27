---
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
---

# Manage multiple {{ecloud}} organizations

You can create or access multiple organizations from a single {{ecloud}} account. 

You might want to create multiple organizations for reasons such as the following:

* You want to separate management of your {{ecloud}} resources and settings for different use cases or teams.
* You want to create a [trial](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#trial-information) to evaluate additional {{ecloud}} features or solutions.

Although you can access multiple organizations from the same {{ecloud}} account, each organization is independent. Each organization has its own set of resources, users, settings, and billing and licensing. Because of this, you need to be logged in to the organization you want to manage to make changes to its resources and settings.

You can perform the following tasks to manage multiple organizations:

* [Create a new organization](#create-a-new-organization)
* [View the organizations you have access to](#view-organizations)
* [Switch to a different organization](#switch-to-a-different-organization)
% * [Delete an organization](#delete-an-organization)

## View the organizations you have access to

You can view the organizations you have access to from the **Overview** page.

To view the organizations:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the top navigation menu, click on the user menu and select **Profile**.
3. Click the **My organizations** tab.

The organizations you have access to appear in the **My organizations** list. In the list, you can view the organization's name, its status, your roles in the organization, and when you were added to the organization.

% confirm list name, confirm that "added" is when you were added to the organization

:::{note}
Role information is refreshed only when you log in to the organization, and might be out of date if you haven't logged in recently.
:::

:::{tip}
You can also access your organizations list by clicking the **My organizations** button on the **Organization** page.
:::

## Create a new organization

You can create a new organization at any time. Each organization starts with its own [14-day trial](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#trial-information).

To create a new organization:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the top navigation menu, click on the user menu and select **Profile**.
3. Click the **My organizations** tab.
4. From the **Organizations** page, click {icon}`plus` **Create organization**.
5. Enter an optional name for your organization, and then click **Create organization**.

After you create the organization, you can switch to it by clicking the organization name in the **Organizations** list.

:::{tip}
You can also create a new organization by clicking on your current organization name and selecting {icon}`plus`  **Create**.
:::

## Switch to a different organization

You can switch between organizations at any time. Depending on the authentication requirements for the organization, you might be required to re-authenticate.

### From your user profile

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the top navigation menu, click on the user menu and select **Profile**.
3. Click the **My organizations** tab.
4. Click the name of the organization you want to switch to. If it doesn't appear in the list, click **Manage organizations** to view all of the organizations you have access to.

### From the My organizations menu

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the top navigation menu, in the breadcrumb list, click the name of your current organization.
3. Click on the organization that you want to log into, or 
4. Click the **My organizations** tab.
5. Click the name of the organization you want to switch to.

% ## Delete an organization

% Can it be done?