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

To access the assistant, go to the **Upgrade Assistant** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

::::{tip}
Upgrade assistant should be run from the latest minor release before a major upgrade. When upgrading to 9.x, ensure you run 8.19.latest, and run the assistant there.
Running the latest patched version of 8.19 will apply latest version of the upgrade assistant logic.
::::

The assistant identifies deprecated settings in your configuration, and if any of those settings are enabled, it guides you through resolving issues that could prevent a successful upgrade. The Upgrade Assistant also helps resolve issues with older indices created before version 8.0.0, providing options to reindex older indices or mark them as read-only. 

## Required permissions [_required_permissions_11] 

To access the Upgrade Assistant, you need the `manage` cluster privilege. 

Reindexing indices requires "all" access for both the existing and target index. In versions 8.18.0 through 8.18.8 and 8.19.0 through 8.19.5, the `superuser` role is required.

You may also need additional privileges to perform specific actions.


## Feature set [_feature_set] 

Some features of the Upgrade Assistant are only needed when upgrading to a new major version. The features enabled by default are those for the next version from the one {{kib}} currently runs on.

## Deprecations [_deprecations] 

The Upgrade Assistant pulls information about deprecations from the following sources:

* {{es}} deprecation info API
* {{es}} deprecation logs
* {{kib}} deprecations API

For more information about Upgrade Assistant APIs, refer to [Upgrade Assistant APIs](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-upgrade).

