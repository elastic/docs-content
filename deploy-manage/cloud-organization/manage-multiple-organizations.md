---
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
  - id: cloud-serverless
navigation_title: Manage multiple organizations
---

# Manage multiple {{ecloud}} organizations

You can create or access multiple organizations from a single {{ecloud}} account. 

You might want to create multiple organizations for reasons such as the following:

* You want to separate management of your {{ecloud}} resources and settings for different use cases or teams.
* You want to create a [trial](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial) to evaluate additional {{ecloud}} features or solutions.

Although you can access multiple organizations from the same {{ecloud}} account, each organization is independent. Each organization has its own set of resources, users, settings, and billing and licensing. Because of this, you need to be logged in to the organization you want to manage to make changes to its resources and settings.

You can perform the following tasks to manage multiple organizations:

* [Create a new organization](#create-a-new-organization)
* [View the organizations you have access to](#view-organizations)
* [Switch to a different organization](#switch-to-a-different-organization)
* [Invite users to join additional organizations](#invite-users-to-join-additional-organizations)

:::{include} _snippets/view-orgs.md
:::

## Create a new organization

You can create a new organization at any time. Each organization starts with its own [14-day trial](/deploy-manage/deploy/elastic-cloud/create-an-organization.md#general-sign-up-trial-what-is-included-in-my-trial).

To create a new organization:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
2. From the top navigation menu, click on the user menu and select **Profile**.
3. Click the **My organizations** tab.
4. From the **Organizations** page, click {icon}`plus_in_circle` **Create organization**.
5. Enter an optional name for your organization, and then click **Create organization**.

After you create the organization, you can switch to it by clicking the organization name in the **Organizations** list.

:::{tip}
You can also create a new organization by clicking on your current organization name and selecting {icon}`plus_in_circle`  **Create**.
:::

:::{include} _snippets/switch-orgs.md
:::

## Invite users to join additional organizations [invite-additional-orgs]

:::{include} _snippets/invite-additional-orgs.md
:::

## Reconcile alternative email addresses

:::{include} /deploy-manage/users-roles/cloud-organization/_snippets/reconcile-email.md
:::

## View your users' organization memberships

:::{include} _snippets/view-users-org-memberships.md
:::