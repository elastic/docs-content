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
| Access the **Workflows** page | `All` or `Read` for **Analytics → Workflows** |
| Fully manage workflows | `All` for **Analytics → Workflows** |
| Grant access to specific workflow actions | Set sub-feature privileges for **Analytics → Workflows** |

## Show managed workflows [workflows-managed-visibility]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

[Managed workflows](/explore-analyze/workflows/managed-workflows.md) are Elastic-shipped workflow definitions that install automatically and power product features. They are hidden from workflow experiences by default.

### Turn on the View filter [workflows-show-managed-setting]

1. Go to the **Advanced Settings** management page in the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for `workflows:ui:showManagedWorkflows` or **Show managed workflows**.
3. Toggle the setting on.
4. Click **Save changes**.

When the setting is on and your role includes the [managed workflow read privileges](#workflows-managed-privileges), the **Workflows** list shows a **View** filter with **Custom** and **Managed** options. **Custom** shows workflows you author yourself. **Managed** shows Elastic-shipped workflows.

### Managed workflow privileges [workflows-managed-privileges]

Managed workflow access uses additive [sub-feature privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md#_sub_feature_privileges) under **Analytics → Workflows → Managed Workflows Actions**:

| Action | Required privilege |
|--------|-------------------|
| View managed workflow definitions | **Read managed workflows** |
| View executions for managed workflows | **Read managed workflow execution** |
| Configure the [Alert analysis workflow](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-analysis-workflow.md) settings | **Update managed workflows** |

## Enable the Template library [workflows-templates-enable]

```{applies_to}
stack: preview 9.5+
serverless: preview
```

The [Template library](/explore-analyze/workflows/templates/start-from-a-template.md) is turned off by default. If **Template library** doesn't appear in the Workflows navigation, have an administrator run the following request from [{{dev-tools-app}}](/explore-analyze/query-filter/tools/console.md) on {{stack}} or {{serverless-short}}. This is a global setting, so it applies to all spaces:

```json
POST kbn:/internal/kibana/global_settings
{
  "changes": {
    "workflowsManagement:library:enabled": true
  }
}
```

:::{note}
The `/internal/kibana/global_settings` endpoint is an internal API and might change without notice. There is currently no public equivalent.
:::

When the request returns HTTP 200 and `workflowsManagement:library:enabled` has `"userValue": true`, reload the page. **Template library** appears in the Workflows navigation.

## What's next [workflows-what-next]

- Create and run your first workflow. Refer to [](/explore-analyze/workflows/get-started/build-your-first-workflow.md) to learn more.
- Create or edit a workflow by describing it in plain language. Refer to [](/explore-analyze/workflows/authoring-techniques/use-natural-language.md) to learn more.
- Understand how to use the YAML editor in {{kib}} to define and run workflows. Refer to [](/explore-analyze/workflows/authoring-techniques/use-yaml-editor.md) to learn more.
- Learn what [managed workflows](/explore-analyze/workflows/managed-workflows.md) are, or configure the Security [Alert analysis workflow](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-analysis-workflow.md).
