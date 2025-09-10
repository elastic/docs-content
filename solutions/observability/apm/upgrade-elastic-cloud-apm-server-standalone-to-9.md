---
navigation_title: "{{ecloud}} standalone"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-upgrade-8.0-cloud-standalone.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Upgrade Elastic Cloud APM Server standalone to 8. [apm-upgrade-8.0-cloud-standalone]

This upgrade guide is for the standalone method of running APM Server. Only use this guide if both of the following are true:

* You’re using {{ecloud}}.
* You’re using the APM Server binary, i.e. you haven’t switched to the Elastic APM integration.

Follow these steps to upgrade:

1. Review the [Elastic APM release notes](apm-server://release-notes/index.md) and [Elastic {{observability}} release notes](/release-notes/elastic-observability/index.md).
2. Review the [Elastic APM breaking changes](apm-server://release-notes/breaking-changes.md).
3. Upgrade {{ecloud}} to 9.0, refer to [Upgrade your deployment](/deploy-manage/upgrade/deployment-or-cluster.md) for instructions.
4. (Optional) Upgrade to the APM integration. Got time for one more upgrade? Refer to [Switch to the Elastic APM integration](/solutions/observability/apm/switch-to-elastic-apm-integration.md).

