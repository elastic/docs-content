---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/upgrade-assistant.html
applies_to:
  stack: ga
products:
  - id: kibana
  - id: cloud-enterprise
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: elasticsearch
---

# Upgrade Assistant [upgrade-assistant]

The Upgrade Assistant helps you [prepare to upgrade](/deploy-manage/upgrade/prepare-to-upgrade.md) to the next major version of the {{stack}}. 

The Upgrade Assistant isn't available on every deployment type and version. If it's [available for yours](#availability), go to the **Upgrade Assistant** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

::::{note}
The Upgrade Assistant relies only on local {{es}} and {{kib}} APIs to detect deprecations and prepare your cluster for upgrade. It doesn't depend on any external service, so you can use it in air-gapped environments without internet access. For details on the APIs it uses, refer to [Deprecations](#_deprecations).
::::

::::{tip}
Upgrade assistant should be run from the latest minor release before a major upgrade. When upgrading to 9.x, ensure you run 8.19.latest, and run the assistant there.
Running the latest patched version of 8.19 will apply latest version of the upgrade assistant logic.
::::

The assistant identifies deprecated settings in your configuration, and if any of those settings are enabled, it guides you through resolving issues that could prevent a successful upgrade. The Upgrade Assistant also helps resolve issues with older indices created before version 8.0.0, providing options to reindex older indices or mark them as read-only. 

:::{tip}
If there are issues with your data or configuration, the Upgrade Assistant provides next steps or more details. Refer to [](/troubleshoot/elasticsearch/troubleshooting-upgrade-assistant.md).
:::

## Availability [availability]

Whether you can use the Upgrade Assistant depends on your deployment type and {{stack}} version:

| Deployment | 9.0 | 9.1 and later |
|---|---|---|
| Self-managed | Available | Available, but off by default |
| {{ech}} | Available | Not available |
| {{serverless-short}} | Not available | Not available |

{applies_to}`self: ga 9.1+` To use the app on a self-managed deployment, set `xpack.upgrade_assistant.ui.enabled` to `true` in `kibana.yml`, then restart {{kib}}. The app then appears in the navigation menu and in the global search field. For the full list of settings, refer to the [{{kib}} general settings](kibana://reference/configuration-reference/general-settings.md).

## Required permissions [_required_permissions_11] 

To access the Upgrade Assistant, you need the `manage` cluster privilege. 

Reindexing indices requires "all" access for both the existing and target index. In versions 8.18.0 through 8.18.8 and 8.19.0 through 8.19.5, the `superuser` role is required.

You may also need additional privileges to perform specific actions.


## Feature set [_feature_set] 

Some features of the Upgrade Assistant are only needed when upgrading to a new major version.

## Deprecations [_deprecations] 

The Upgrade Assistant pulls information about deprecations from the following sources:

* {{es}} deprecation info API
* {{es}} deprecation logs
* {{kib}} deprecations API

For more information about Upgrade Assistant APIs, refer to [Upgrade Assistant APIs]({{kib-apis}}group/endpoint-upgrade).

The {{es}} deprecation info API reports features that will be removed or changed in the next major version, such as cluster, node, and index level settings. You must address the reported issues before upgrading to the next major version. However, no action is required when upgrading within a major version, such as from {{es}} {{version.stack.base}} to {{version.stack}}. Deprecated features remain fully supported and continue to work in the current version, and when upgrading to a newer minor or patch release in the same major version.

