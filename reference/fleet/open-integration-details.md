---
navigation_title: Open an integration's details
description: Open an integration's details in Kibana to read its documentation and reach its policies, assets, and settings tabs.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
type: how-to
---

# Open an integration's details [integration-details]

An integration's details open on the **Overview** page, which shows the integration's documentation. Other tabs cover the integration's policies, assets, settings, and more. Open an integration's details to learn what it collects, or to manage an integration that you've already added.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` Selecting an integration on the **Browse integrations** tab opens the **Add <integration>** page instead, so you can [add the integration](/reference/fleet/add-integration-to-policy.md) right away. To open the integration's details, follow the steps on this page.

## Before you begin [integration-details-prerequisites]

Your role needs these privileges:

* To open an integration's details: the `Read` or `All` privilege for **Integrations**.
* To see the **Integration policies** tab: the `Read` or `All` privilege for **Fleet**.
* To see the **Configs** tab: the `All` privilege for **Fleet**.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.1+` If you [customize sub-feature privileges for {{fleet}}](/reference/fleet/fleet-roles-privileges.md#fleet-roles-and-privileges-sub-features), the **Integration policies** tab needs `Read` or `All` for **Agent policies**, and the **Configs** tab needs `All` for **Agents**.

## Open the integration's details [integration-details-steps]

The quickest way is the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md): search for the integration by name and select it. The integration's **Overview** page opens directly.

To open the details from the **Integrations** page instead:

1. Find **Integrations** in the navigation menu.
2. Select the integration:
    * If the integration is installed, select it on the **Installed integrations** tab.
    * If the integration isn't installed yet, select it on the **Browse integrations** tab.
3. {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` If the **Add <integration>** page opens, click **View documentation** in the **New to this integration?** panel, then click **Integration details**.

    Integrations that only install assets, such as dashboards, or only provide setup documentation open their **Overview** page directly. The **Overview** page also opens directly if your role has `Read` access to **Integrations** instead of `All`.

The integration's details open on the **Overview** page.

## Tabs in an integration's details [integration-details-tabs]

The tabs that you see depend on the integration, whether it's installed, and your privileges.

| Tab | What you can do there |
| --- | --- |
| **Overview** | Read the integration's documentation, including what data it collects and how to set it up. |
| **Integration policies** | [View](/reference/fleet/view-integration-policies.md), [edit, or delete](/reference/fleet/edit-delete-integration-policy.md) the integration's policies. Shown for installed integrations. |
| **Assets** | [View the assets](/reference/fleet/view-integration-assets.md) that the integration installed, such as dashboards and index templates. Shown for installed integrations that have assets. |
| **Alerting** {applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` | Create rules from the integration's [alerting rule templates](/reference/fleet/alerting-rule-templates.md). Shown for installed integrations that have alerting assets. |
| **Settings** | [Install, uninstall, or reinstall the integration's assets](/reference/fleet/install-uninstall-integration-assets.md), and [upgrade the integration](/reference/fleet/upgrade-integration.md). |
| **Configs** | View sample standalone {{agent}} configurations for the integration's data streams. |
| **API reference** | Find the inputs, streams, and variables to use when you [add the integration with the {{fleet}} API](/reference/fleet/fleet-api-docs.md). |

Some integrations also have an **Advanced** tab with settings specific to that integration.
