---
navigation_title: Edit or delete an integration policy
description: Edit an Elastic Agent integration policy in Fleet to update its settings or the agent policies it's added to, or delete an integration policy that you no longer need.
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/edit-or-delete-integration-policy.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
type: how-to
---

# Edit or delete an {{agent}} integration policy [edit-or-delete-integration-policy]

Edit an integration policy to update its configuration settings or the {{agent}} policies that it's added to, or delete an integration policy that you no longer need. {{fleet}} distributes saved changes to all {{agent}}s enrolled in the affected agent policies.

## Before you begin [edit-or-delete-integration-policy-prereqs]

To edit or delete an integration policy, your role needs the `All` privilege for **Fleet** and **Integrations**.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.1+` If you [customize sub-feature privileges for {{fleet}}](/reference/fleet/fleet-roles-privileges.md#fleet-roles-and-privileges-sub-features), the role needs the `All` privilege for **Agent policies**.

## Edit an integration policy [edit-integration-policy]

1. In {{kib}}, find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Installed integrations** tab, select the integration.
3. On the **Integration policies** tab, find the integration policy that you want to edit. From its **Actions** menu, select **Edit integration**.
4. On the **Edit <integration>** page, update the configuration settings and the {{agent}} policies that the integration policy is added to.

    If you clear the **Agent policies** field, the integration policy is removed from all the {{agent}} policies that it was added to.

5. Select **Save integration**.

{{fleet}} distributes the saved changes to all {{agent}}s enrolled in the affected agent policies.

To find integration policies that aren't added to any {{agent}} policy, check the **Agent policies** column on the **Integration policies** tab. These integration policies are labeled `No agent policies`.

## Delete an integration policy [delete-integration-policy]

Deleting an integration policy can't be undone. The {{agent}}s enrolled in the affected agent policies stop collecting data for that integration policy. To collect the data again, [add the integration](/reference/fleet/add-integration-to-policy.md) again.

1. In {{kib}}, find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Installed integrations** tab, select the integration.
3. On the **Integration policies** tab, find the integration policy that you want to delete. From its **Actions** menu, select **Delete integration**.
4. In the confirmation dialog, select **Delete integration**.
