---
navigation_title: Install and uninstall integration assets
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/install-uninstall-integration-assets.html
products:
  - id: fleet
  - id: elastic-agent
---

# Install and uninstall {{agent}} integration assets [install-uninstall-integration-assets]


{{agent}} integrations come with a number of assets, such as dashboards, saved searches, and visualizations for analyzing data. When you add an integration to an agent policy in {{fleet}}, the assets are installed automatically. If you’re building a policy file by hand, you need to install required assets such as index templates.


## Install integration assets [install-integration-assets]

1. In {{kib}}, go to the **Integrations** page and open the **Browse integrations** tab. Search for and select an integration. You can select a category to narrow your search.
2. Click the **Settings** tab.
3. Click **Install <integration> assets** to set up the {{kib}} and {{es}} assets.

Note that it’s currently not possible to have multiple versions of the same integration installed. When you upgrade an integration, the previous version assets are removed and replaced by the current version.

::::{admonition} Spaces support for integration assets

Elastic Agent integrations and their assets, such as dashboards, visualizations, and saved searches, behave differently depending on your {{stack}} version:

* {applies_to}`stack: ga, removed 9.1` In versions earlier than {{stack}} 9.1, integration assets can be installed in only one {{kib}} space.
You can manually [copy them](/explore-analyze/find-and-organize/saved-objects.md#managing-saved-objects-copy-to-space) to other spaces. However, many integrations include markdown panels with dynamically generated links to other dashboards. When copied between spaces, these links might not behave as expected and can result in a `Dashboard not found` (404) error. Refer to known issue [#175072](https://github.com/elastic/kibana/issues/175072) for details.

* {applies_to}`stack: ga 9.1` Starting in {{stack}} 9.1, Fleet introduces a space-aware data model for {{agent}} policies and integrations. Agent policies can now span multiple spaces, while integration assets remain space-specific. 

  Integration assets are still installed per space, but can be managed and reinstalled independently in each space.

  If you upgraded from an earlier version, enable space awareness in Fleet before managing integrations across spaces.

  For more details, refer to [Using Spaces with Fleet](../../deploy-manage/manage-spaces-fleet.md).

::::



## Uninstall integration assets [uninstall-integration-assets]

Uninstall an integration to remove all {{kib}} and {{es}} assets that were installed by the integration.

1. Before uninstalling an integration, [delete the integration policy](/reference/fleet/edit-delete-integration-policy.md) from any {{agent}} policies that use it.

    Any {{agent}}s enrolled in the policy will stop using the deleted integration.

2. In {{kib}}, go to the **Integrations** page and open the **Installed integrations** tab. Search for and select an integration.
3. Click the **Settings** tab.
4. Click **Uninstall <integration>** to remove all {{kib}} and {{es}} assets that were installed by this integration.


## Reinstall integration assets [reinstall-integration-assets]

You may need to reinstall an integration package to resolve a specific problem, such as:

* An asset was edited manually, and you want to reset assets to their original state.
* A temporary problem (like a network issue) occurred during package installation or upgrade.
* A package was installed in a prior version that had a bug in the install code.

To reinstall integration assets:

1. In {{kib}}, go to the **Integrations** page and open the **Installed integrations** tab. Search for and select an integration.
2. Click the **Settings** tab.
3. Click **Reinstall <integration>** to set up the {{kib}} and {{es}} assets.
