---
navigation_title: "Install and uninstall integration assets"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/install-uninstall-integration-assets.html
---

# Install and uninstall {{agent}} integration assets [install-uninstall-integration-assets]


{{agent}} integrations come with a number of assets, such as dashboards, saved searches, and visualizations for analyzing data. When you add an integration to an agent policy in {{fleet}}, the assets are installed automatically. If you’re building a policy file by hand, you need to install required assets such as index templates.


## Install integration assets [install-integration-assets]

1. In {{kib}}, go to the **Integrations** page and open the **Browse integrations** tab. Search for and select an integration. You can select a category to narrow your search.
2. Click the **Settings** tab.
3. Click **Install <integration> assets** to set up the {{kib}} and {{es}} assets.

Note that it’s currently not possible to have multiple versions of the same integration installed. When you upgrade an integration, the previous version assets are removed and replaced by the current version.

::::{admonition} Current limitations with integrations and {{kib}} spaces
:class: important

{{agent}} integration assets can be installed only on a single {{kib}} [space](/deploy-manage/manage-spaces.md). If you want to access assets in a different space, you can [copy them](/explore-analyze/find-and-organize/saved-objects.md#managing-saved-objects-copy-to-space). However, many integrations include markdown panels with dynamically generated links to other dashboards. When assets are copied between spaces, these links may not behave as expected and can result in a 404 `Dashboard not found` error. Refer to known issue [#175072](https://github.com/elastic/kibana/issues/175072) for details.

These limitations and future plans for {{fleet}}'s integrations support in multi-space environments are currently being discussed in [#175831](https://github.com/elastic/kibana/issues/175831). Feedback is very welcome. For now, we recommend reviewing the specific integration documentation for any space-related considerations.

::::



## Uninstall integration assets [uninstall-integration-assets]

Uninstall an integration to remove all {{kib}} and {{es}} assets that were installed by the integration.

1. Before uninstalling an integration, [delete the integration policy](/reference/ingestion-tools/fleet/edit-delete-integration-policy.md) from any {{agent}} policies that use it.

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
