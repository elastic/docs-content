---
navigation_title: Set up Workflows
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Configure role-based access to Elastic Workflows.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Set up Workflows [workflows-setup]

:::::{applies-switch}

::::{applies-item} { "stack": "ga 9.4+", "serverless": "ga" }

To use workflows, ensure your role has the appropriate privileges. You must also have the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.

::::

::::{applies-item} stack: preview 9.3

To use workflows, you must turn on the feature and ensure your role has the appropriate privileges. You must also have the appropriate subscription. Refer to the subscription page for [Elastic Cloud](https://www.elastic.co/subscriptions/cloud) and [Elastic Stack/self-managed](https://www.elastic.co/subscriptions) for the breakdown of available features and their associated subscription tiers.

### Enable workflows [workflows-enable]

The workflows feature is turned off by default. To turn it on:

1. Go to the **Advanced Settings** management page in the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for `workflows:ui:enabled`.
3. Toggle the setting on.
4. Click **Save changes** to turn on workflows in your space, then reload the page.

The **Workflows** page displays in the main navigation menu and you can search for it using the global search field.

::::

:::::

## Manage access to workflows [workflows-role-access]

Access to workflows is controlled by [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md). The following table describes privileges required to create, edit, run, and manage workflows.

| Action | Required privilege |
|--------|-------------------|
| Access the **Workflows** page | `All` or `Read` for **Analytics > Workflows** |
| Fully manage workflows | `All` for **Analytics > Workflows** |
| Grant access to specific workflow actions | Set sub-feature privileges for **Analytics > Workflows** | 

## Enable the Template Library [workflows-templates-enable]

```{applies_to}
stack: preview 9.5+
serverless: preview
```

The [Template Library](/explore-analyze/workflows/templates/start-from-a-template.md) is turned off by default and must be enabled by an administrator. If you don't see **Template Library** in the Workflows navigation, ask an administrator to turn it on. After it's enabled, reload the page. **Template Library** appears in the Workflows navigation, and an empty workflows list shows **Explore library**.

::::{applies-switch}
:::{applies-item} stack: preview 9.5+

An administrator can enable the Template Library in either of these ways:

**Option 1: Edit `kibana.yml`**

Add the following, then restart {{kib}}:

```yaml
uiSettings.overrides:
  workflowsManagement:library:enabled: true
```

**Option 2: Use the global settings API**

In [{{dev-tools-app}}](/explore-analyze/query-filter/tools/console.md), run:

```json
POST kbn:/internal/kibana/global_settings
{
  "changes": {
    "workflowsManagement:library:enabled": true
  }
}
```
:::

:::{applies-item} serverless:

{{serverless-short}} has no Global Advanced Settings UI, so an administrator uses [{{dev-tools-app}}](/explore-analyze/query-filter/tools/console.md) to call the global settings API:

```json
POST kbn:/internal/kibana/global_settings
{
  "changes": {
    "workflowsManagement:library:enabled": true
  }
}
```
:::
::::

:::{note}
The `/internal/kibana/global_settings` endpoint is an internal API and might change without notice. There is currently no public equivalent.
:::

## What's next [workflows-what-next]

- Create and run your first workflow. Refer to [](/explore-analyze/workflows/get-started/build-your-first-workflow.md) to learn more.
- Understand how to use the YAML editor in {{kib}} to define and run workflows. Refer to [](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md) to learn more.
