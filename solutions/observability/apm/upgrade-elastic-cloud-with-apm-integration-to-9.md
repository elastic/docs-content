---
navigation_title: "{{ecloud}} APM integration"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-upgrade-8.0-cloud-integration.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Upgrade Elastic Cloud with the APM integration to 8.0 [apm-upgrade-8.0-cloud-integration]

This upgrade guide is for the Elastic APM integration. Only use this guide if both of the following are true:

* You’re using {{ecloud}}.
* You have already switched to and are running {{fleet}} and the Elastic APM integration.

Follow these steps to upgrade:

1. Review the [Elastic APM release notes](apm-server://release-notes/index.md) and [Elastic {{observability}} release notes](/release-notes/elastic-observability/index.md).
2. Review the [Elastic APM breaking changes](apm-server://release-notes/breaking-changes.md).
3. Upgrade your {{ecloud}} instance to 9.0. Refer to [Upgrade your deployment](/deploy-manage/upgrade/deployment-or-cluster.md) for details. As a part of this process, the APM integration will automatically upgrade to version 9.0.

::::{note}
{{ece}} users require additional TLS setup. Refer to [Add APM user settings](/solutions/observability/apm/apm-server/configure.md) for more information.
::::

