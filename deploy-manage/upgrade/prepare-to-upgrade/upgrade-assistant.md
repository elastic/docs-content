---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/upgrade-assistant.html
---

# Upgrade Assistant [upgrade-assistant]

The Upgrade Assistant helps you prepare for your upgrade to the next version of the {{stack}}. To access the assistant, go to **{{stack-manage-app}} > Upgrade Assistant**.

The assistant identifies deprecated settings in your configuration and guides you through the process of resolving issues if any deprecated features are enabled.


## Required permissions [_required_permissions_11] 

The `manage` cluster privilege is required to access the **Upgrade assistant**. Additional privileges may be needed to perform certain actions.


## Feature set [_feature_set] 

Some features of the Upgrade assistant are only needed when upgrading to a new major version. The feature set enabled by default are those for the very next version from the one {{kib}} currently runs on.


## Deprecations [_deprecations] 

The Upgrade assistant pulls information about deprecations from the following sources:

* {{es}} Deprecation Info API
* {{es}} deprecation logs
* {{kib}} deprecations API

For more information about Upgrade Assistant APIs, refer to [Upgrade Assistant APIs](https://www.elastic.co/guide/en/kibana/current/upgrade-assistant-api.html).

