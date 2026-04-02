---
products:
  - id: kibana
  - id: elastic-agent
applies_to:
  stack: ga 9.1
  serverless: ga
---

# Using Spaces with {{fleet}} [spaces-fleet]

Fleet supports a **space-aware** data model. You can use [Kibana spaces](/deploy-manage/manage-spaces.md) to manage Agent policies and integrations per space. Combined with granular [user roles](/reference/fleet/fleet-roles-privileges.md), this feature enables true role-based access control for {{agent}} management.

For **new deployments** on {{stack}} 9.1.0 or later, space awareness is enabled by default.
For **upgraded deployments** from earlier versions, you must explicitly [enable space awareness](#spaces-fleet-enable).

To use space awareness with {{fleet}}:

- [Enable the space awareness feature](#spaces-fleet-enable) (for upgraded deployments)
- [Assign and manage Agent policies across spaces](#spaces-manage-policies)
- [Make integration assets available across spaces](#spaces-manage-assets)

## Enable space awareness in Fleet [spaces-fleet-enable]

You must enable space awareness for deployments upgraded to 9.1.0 or later. Space awareness requires a one-time migration that copies your existing {{fleet}} data into a new, space-aware model. Previous data is preserved in snapshots in case you need to roll back.

To enable space awareness in upgraded deployments:

1. Navigate to the **Fleet** app.
2. Click the **Settings** tab.
3. Scroll to **Advanced settings**.
4. Under **Migrate to space-aware agent policies**, click **Start migration**.
5. Confirm the migration.


## Manage Agent policies across spaces [spaces-manage-policies]

To control where an Agent Policy is available:

1. Navigate to the Agent Policy’s **Settings** tab.

   :::{image} /deploy-manage/images/kibana-space-fleet-policy.png
   :alt: Agent Policy settings tab
   :screenshot:
   :::

2. Use the **Spaces** dropdown to select one or more spaces.

   :::{image} /deploy-manage/images/kibana-space-policy-settings.png
   :alt: Agent Policy spaces dropdown
   :screenshot:
   :::

Agent policies can be assigned to multiple spaces. In this example, the policy is visible in both the "Default" space and "My second space."

:::{image} /deploy-manage/images/kibana-space-multispace.png
:alt: Policy in multiple spaces
:screenshot:
:::


Access to a policy is still governed by each user's {{fleet}} permissions within selected spaces.

## Manage integration assets across spaces [spaces-manage-assets]

When you add an integration to an Agent policy, assets such as dashboards and visualizations are installed **only in the current space** by default.

If the Agent Policy spans multiple spaces, install the integration's assets in each space manually:

1. Switch to the desired Kibana space.
2. Go to the **Integrations** app > **Installed integrations** tab.
3. Click the name of the integration.

   :::{image} /deploy-manage/images/kibana-space-integration.png
   :alt: Installed integrations list
   :screenshot:
   :::

4. Open the **Assets** tab.

   :::{image} /deploy-manage/images/kibana-space-add-asset.png
   :alt: Kibana Assets tab
   :screenshot:
   :::

5. Click **Install Kibana assets in current space**.

  This installs dashboards and other UI assets into the selected space.

:::{note}
Due to limitations in Kibana’s saved object model, integration assets are copied per space. These saved objects are considered **managed** and are **readonly**.
:::
