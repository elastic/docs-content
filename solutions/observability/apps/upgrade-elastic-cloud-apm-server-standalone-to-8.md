---
navigation_title: "{{ecloud}} standalone"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-upgrade-8.0-cloud-standalone.html
---



# Upgrade Elastic Cloud APM Server standalone to 8. [apm-upgrade-8.0-cloud-standalone]


This upgrade guide is for the standalone method of running APM Server. Only use this guide if both of the following are true:

* You’re using {{ecloud}}.
* You’re using the APM Server binary, i.e. you haven’t switched to the Elastic APM integration.

Follow these steps to upgrade:

1. Review the APM [release notes](https://www.elastic.co/guide/en/observability/current/apm-release-notes.html), [breaking changes](https://www.elastic.co/guide/en/observability/current/apm-breaking.html), and {{observability}} [What’s new](https://www.elastic.co/guide/en/observability/current/whats-new.html) content.
2. Upgrade {{ecloud}} to 9.0.0-beta1, See [Upgrade versions](../../../deploy-manage/upgrade/deployment-or-cluster.md) for instructions.
3. (Optional) Upgrade to the APM integration. Got time for one more upgrade? See [Switch to the Elastic APM integration](switch-to-elastic-apm-integration.md).

