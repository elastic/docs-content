---
applies_to:
  deployment:
    ess: ga
  serverless: ga
products:
  - id: cloud-hosted
navigation_title: View and switch between organizations
---

# View and switch between {{ecloud}} organizations

From a single {{ecloud}} account, you can access multiple organizations.

You might be a member of multiple organizations in cases such as the following:

* You use different organizations for different use cases or teams.
* You're a consultant working with multiple clients who have different {{ecloud}} organizations.

You can switch between organizations at any time. Depending on the organization that you're switching to, you might be required to re-authenticate.

If you're an organization owner, then you can learn more about managing multiple organizations in [](/deploy-manage/cloud-organization/manage-multiple-organizations.md).

:::{tip}
To join an additional organization, [accept an invitation](/cloud-account/join-or-leave-an-organization.md#ec-accept-invitation) to join the organization. You can also [create a new organization](/deploy-manage/cloud-organization/manage-multiple-organizations.md#create-a-new-organization).
:::

:::{include} /deploy-manage/cloud-organization/_snippets/view-orgs.md
:::

:::{include} /deploy-manage/cloud-organization/_snippets/switch-orgs.md
:::

## Log in with multiple organizations

When you belong to multiple organizations, the login experience depends on whether your browser has information about the organization you most recently used:

* **Returning user (same browser):** You're automatically logged in to the organization you last used. You don't need to select an organization.
* **New browser or cleared data:** After logging in, you're presented with a list of your organizations to choose from. Select the organization you want to access.

If your last used organization enforces a specific login method (such as SAML SSO), you're directed to that login flow automatically.

If you log out, your browser remembers which organization you last used. The next time you log in, you're directed to the appropriate login page for that organization.