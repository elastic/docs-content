---
navigation_title: "{{ecloud}} APM integration"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-upgrade-8.0-cloud-integration.html
---



# Upgrade Elastic Cloud with the APM integration to 8.0 [apm-upgrade-8.0-cloud-integration]


This upgrade guide is for the Elastic APM integration. Only use this guide if both of the following are true:

* You’re using {{ecloud}}.
* You have already switched to and are running {{fleet}} and the Elastic APM integration.

Follow these steps to upgrade:

1. Review the APM [release notes](https://www.elastic.co/guide/en/observability/current/apm-release-notes.html), [breaking changes](https://www.elastic.co/guide/en/observability/current/apm-breaking.html), and {{observability}} [What’s new](https://www.elastic.co/guide/en/observability/current/whats-new.html) content.
2. Upgrade your {{ecloud}} instance to 9.0.0-beta1. See [Upgrade versions](../../../deploy-manage/upgrade/deployment-or-cluster.md) for details. The APM integration will automatically be upgraded to version 9.0.0-beta1 as a part of this process.

::::{note}
{{ece}} users require additional TLS setup. See [Add APM user settings](https://www.elastic.co/guide/en/cloud-enterprise/{{ece-version-link}}/ece-manage-apm-settings.html) for more information.
::::


