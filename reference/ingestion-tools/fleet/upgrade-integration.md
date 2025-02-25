---
navigation_title: "Upgrade an integration"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/upgrade-integration.html
---

# Upgrade an {{agent}} integration [upgrade-integration]


::::{important}
By default, {{kib}} requires an internet connection to download integration packages from the {{package-registry}}. Make sure the {{kib}} server can connect to `https://epr.elastic.co` on port `443`. If network restrictions prevent {{kib}} from reaching the public {{package-registry}}, you can use a proxy server or host your own {{package-registry}}. To learn more, refer to [Air-gapped environments](/reference/ingestion-tools/fleet/air-gapped.md).
::::


Elastic releases {{agent}} integration updates periodically. To use new features and capabilities, upgrade the installed integration to the latest version and optionally upgrade integration policies to use the new version.

::::{tip}
In larger deployments, you should test integration upgrades on a sample {{agent}} before rolling out a larger upgrade initiative.
::::



## Upgrade an integration to the latest version [upgrade-integration-to-latest-version]

1. In {{kib}}, go to the **Integrations** page and open the **Installed integrations** tab. Search for and select the integration you want to upgrade. Notice there is a warning icon next to the version number to indicate a new version is available.
2. Click the **Settings** tab and notice the message about the new version.

    :::{image} images/upgrade-integration.png
    :alt: Settings tab under Integrations shows how to upgrade the integration
    :class: screenshot
    :::

3. Before upgrading the integration, decide whether to upgrade integration policies to the latest version, too. To use new features and capabilities, you’ll need to upgrade existing integration policies. However, the upgrade may introduce changes, such as field changes, that require you to resolve conflicts.

    * Select **Upgrade integration policies** to upgrade any eligible integration policies when the integration is upgraded.
    * To continue using the older package version, deselect **Upgrade integration policies**. You can still choose to [upgrade integration policies manually](#upgrade-integration-policies-manually) later on.

4. Click **Upgrade to latest version**.

    If you selected **Upgrade integration policies** and there are conflicts, [upgrade integration policies manually](#upgrade-integration-policies-manually) and resolve the conflicts in the policy editor.

5. After the upgrade is complete, verify that the installed version and latest version match.

::::{note}
You must upgrade standalone agents separately. If you used {{kib}} to create and download your standalone agent policy, see [Upgrade standalone agent policies after upgrading an integration](/reference/ingestion-tools/fleet/create-standalone-agent-policy.md#update-standalone-policies).
::::



## Keep integration policies up to date automatically [upgrade-integration-policies-automatically]

Some integration packages, like System, are installed by default during {{fleet}} setup. These integrations are upgraded automatically when {{fleet}} detects that a new version is available.

The following integrations are installed automatically when you select certain options in the {{fleet}} UI. All of them have an option to upgrade integration policies automatically, too:

* [Elastic Agent](integration-docs://docs/reference/elastic_agent.md) - installed automatically when the default **Collect agent logs** or **Collect agent metrics** option is enabled in an {{agent}} policy).
* [Fleet Server](integration-docs://docs/reference/fleet_server.md) - installed automatically  when {{fleet-server}} is set up through the {{fleet}} UI.
* [System](integration-docs://docs/reference/system.md) - installed automatically when the default **Collect system logs and metrics** option is enabled in an {{agent}} policy).

The [Elastic Defend](integration-docs://docs/reference/endpoint.md) integration also has an option to upgrade installation policies automatically.

Note that for the following integrations, when the integration is updated automatically the integration policy is upgraded automatically as well. This behavior cannot be disabled.

* [Elastic APM](integration-docs://docs/reference/apm.md)
* [Cloud Security Posture Management](integration-docs://docs/reference/cloud_security_posture.md#cloud_security_posture-cloud-security-posture-management-cspm)
* [Elastic Synthetics](/solutions/observability/apps/synthetic-monitoring.md)

For integrations that support the option to auto-upgrade the integration policy, when this option is selected (the default), {{fleet}} automatically upgrades your policies when a new version of the integration is available. If there are conflicts during the upgrade, your integration policies will not be upgraded, and you’ll need to [upgrade integration policies manually](#upgrade-integration-policies-manually).

To keep integration policies up to data automatically:

1. In {{kib}}, go to the **Integrations** page and open the **Installed integrations** tab. Search for and select the integration you want to configure.
2. Click **Settings** and make sure **Keep integration policies up to data automatically** is selected.

    :::{image} images/upgrade-integration-policies-automatically.png
    :alt: Settings tab under Integrations shows how to keep integration policies up to date automatically
    :class: screenshot
    :::

    If this option isn’t available on the **Settings** tab, this feature is not available for the integration you’re viewing.



## Upgrade integration policies manually [upgrade-integration-policies-manually]

If you can’t upgrade integration policies when you upgrade the integration, upgrade them manually.

1. Click the **Policies** tab and find the integration policies you want to upgrade.

    :::{image} images/upgrade-package-policy.png
    :alt: Policies tab under Integrations shows how to upgrade the package policy
    :class: screenshot
    :::

2. Click **Upgrade** to begin the upgrade process.

    The upgrade will open in the policy editor.

    :::{image} images/upgrade-policy-editor.png
    :alt: Upgrade integration example in the policy editor
    :class: screenshot
    :::

3. Make any required configuration changes and, if necessary, resolve conflicts. For more information, refer to [Resolve conflicts](#resolve-conflicts).
4. Repeat this process for each policy with an out-of-date integration.

Too many conflicts to resolve? Refer to the [troubleshooting docs](/troubleshoot/ingest/fleet/common-problems.md#upgrading-integration-too-many-conflicts) for manual steps.


## Resolve conflicts [resolve-conflicts]

When attempting to upgrade an integration policy, it’s possible that breaking changes or conflicts exist between versions of an integration. For example, if a new version of an integration has a required field and doesn’t specify a default value, {{fleet}} cannot perform the upgrade without user input. Conflicts are also likely if an experimental package greatly restructures its fields and configuration settings between releases.

If {{fleet}} detects a conflict while automatically upgrading an integration policy, it will not attempt to upgrade it. You’ll need to:

1. [Upgrade the integration policy manually](#upgrade-integration-policies-manually).
2. Use the policy editor to fix any conflicts or errors.

    :::{image} images/upgrade-resolve-conflicts.png
    :alt: Resolve field conflicts in the policy editor
    :class: screenshot
    :::

    1. Under **Review field conflicts**, notice that you can click **previous configuration**  to view the raw JSON representation of the old integration policy and compare values. This feature is useful when fields have been deprecated or removed between releases.

        :::{image} images/upgrade-view-previous-config.png
        :alt: View previous configuration to resolve conflicts
        :class: screenshot
        :::

    2. In the policy editor, fix any errors and click **Upgrade integration**.
