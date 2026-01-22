---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn how to enable workflows and configure role-based access.
---

# Set up workflows [workflows-setup]

Before you can use workflows, you need to turn on the feature and ensure users have the appropriate permissions. In addition, you must have the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.

## Enable workflows [workflows-enable]

The workflows feature is turned off by default. To turn it on:

1. Go to the **Advanced Settings** management page in the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for `workflows:ui:enabled`.
3. Toggle the setting on.
4. Click **Save changes** to turn on workflows in your space, then reload the page. 

Workflows displays in the main navigation menu and you can search for it using the global search field.

## Manage access to workflows [workflows-role-access]

Access to workflows is controlled by [{{kib}} privilege](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) privileges. Ensure users have the appropriate roles assigned to create, edit, run, and manage workflows.

| Action | Required privilege |
|--------|-------------------|
| Access the **Workflows** page | `All` or `Read` for **Analytics > Workflows** |
| Fully manage workflows | `All` for **Analytics > Workflows** |
| Grant access to specific workflow actions | Set sub-feature privileges for **Analytics > Workflows** | 