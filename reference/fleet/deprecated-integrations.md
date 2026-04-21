---
navigation_title: Deprecated integrations
applies_to:
  stack: ga 9.4+
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Understanding deprecated integrations [deprecated-integrations]

Developers can mark integration packages or some of their features as deprecated when they want to retire them, replace them with newer alternatives, or stop maintaining them. 

Deprecation serves as an advance notice that the integration will eventually be removed from the {{package-registry}}. Migration to an alternative integration or feature is recommended for deprecated packages.

A deprecation can apply to:

* **An entire integration package**
* **Individual features** within a supported integration, such as specific inputs, data streams, or configuration variables

## Deprecation lifecycle [deprecation-lifecycle]

When integration developers deprecate a package or its features:

1. They release a new package version with the `deprecated` field in the integration's manifest. The field can include the following nested fields:
   * `description`: A description of the deprecation
   * `since`: The version when the deprecation begins
   * `replaced_by`: A recommended alternative (if available)
2. Deprecation warnings are displayed throughout the {{fleet}} UI and the Integrations UI.

After the deprecation of a package or its features begins, a maintenance period follows (typically one year):

* The integration remains available in the {{package-registry}}.
* You can still install the integration on new {{agents}}, but deprecated features aren't available for new installations.
* Existing installations continue to work normally, with deprecation warnings displayed for deprecated features.
* Integration developers might provide critical bug fixes, but new features are typically not added.

After the maintenance period ends, the integration reaches end-of-life:

* The integration might be removed from the {{package-registry}}.
* New installations of the deprecated integration are impossible.
* Existing installations might continue to work but are unsupported.
* No bug fixes or updates are provided.

## Identify deprecated integrations [identify-deprecated]

{{fleet}} marks deprecated integrations in multiple locations in the UI to ensure visibility:

* **Integrations** list: Deprecated integrations are marked with a **(Deprecated)** label in their title. They remain visible in search results by default.
* **Installed integrations** list: A warning icon appears next to the integration title, and a tooltip shows a deprecation message. The integration title includes **(Deprecated)**.
* An integration's **Overview** and **Settings** pages: A warning callout displays the deprecation description, a list of the deprecated features (if any), the recommended alternatives to use, and the version in which the integration or its features were deprecated. 
* **Integration policies**: Policies with enabled deprecated features display a warning icon next to the feature, with a tooltip showing a deprecation message.

:::{note}
If your installed integration version is lower than the version in which the deprecation begins (as specified in the `since` field), {{fleet}} displays an upcoming deprecation warning instead. The warning shows when the deprecation will take effect, giving you time to plan migration before upgrading to that version.
:::

## How deprecations affect integration upgrades [upgrades-deprecated]

When you upgrade to a deprecated integration version, how {{fleet}} handles it depends on whether you have automatic policy upgrades enabled.

### Review and accept automatic upgrades [auto-upgrade-deprecated]

If you've enabled the [automatic upgrade of integration policies](/reference/fleet/upgrade-integration.md#upgrade-integration-policies-automatically) for an integration, {{fleet}} pauses automatic policy upgrades when the next version includes deprecations. 

While the automatic upgrade is paused, you'll see:

* A **Review upgrade** button on the integration's **Integration policies** page
* A warning icon in the **Attached policies** column on the **Integrations** > **Installed integrations** page

To review the pending upgrade:

1. In {{kib}}, open **Integrations** > **Installed integrations**.
2. In the **Attached policies** column, open the integration's policies.
3. In the **Version** column, select **Review upgrade** for the policy you want to update.
4. Review the deprecation warnings and recommended alternatives.
5. Choose an option:

   * **Accept upgrade**: The policy is updated to the new version.
   * **Decline**: The policy remains on the current version. You can review the upgrade again later.

If you declined and want to review the upgrade again:

1. On the integration's **Integration policies** page, open the **Actions** menu for the policy.
2. Select **Review policy upgrade**.
3. Review the deprecation warnings and recommended alternatives.
4. Choose **Accept upgrade** to apply the new version, or **Decline** to stay on the current version.

:::{important}
Plan your migration during the maintenance period. Even if you accept the upgrade, you should migrate to a recommended alternative before the integration reaches end-of-life.
:::

### Stack-aligned integrations [stack-aligned-auto-upgrade]

The following integrations are version-aligned with the {{stack}} and upgrade automatically even if deprecations are present:

* [Cloud Asset Inventory](integration-docs://reference/cloud_asset_inventory.md)
* [Cloud Security Posture Management](integration-docs://reference/cloud_security_posture.md)
* [Elastic APM](integration-docs://reference/apm.md)

If these integrations include deprecations, you'll see warnings after the upgrade completes.

### Upgrade manually [manual-upgrade-deprecated]

If you haven't enabled automatic policy upgrades for an integration, you control when upgrades occur. When you upgrade to a version with deprecations:

* Deprecation warnings appear during the upgrade process.
* The upgrade is not blocked or paused.
* You should review the deprecation notices and plan your migration before the maintenance period ends.

For step-by-step instructions, refer to [Upgrade an Elastic Agent integration](/reference/fleet/upgrade-integration.md).