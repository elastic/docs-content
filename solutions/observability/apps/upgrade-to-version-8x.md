---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-upgrading-to-8.x.html
---

# Upgrade to version 8.x [apm-upgrading-to-8.x]

This guide explains the upgrade process for version 9.0.0-beta1. For a detailed look at what’s new, see:

* [Elastic {{observability}} release notes](https://www.elastic.co/guide/en/observability/current/whats-new.html)
* [What’s new in {{kib}}](https://www.elastic.co/guide/en/kibana/current/whats-new.html)
* [{{es}} release highlights](https://www.elastic.co/guide/en/elasticsearch/reference/current/release-highlights.html)


## Notable APM changes [_notable_apm_changes]

* All index management has been removed from APM Server; the built-in {{es}} apm-data plugin is entirely responsible for setting up index templates, index lifecycle polices, and index pipelines.
* APM Server now only writes to well-defined data streams; writing to classic indices is no longer supported.
* APM Server has a new {{es}} output implementation with defaults that should be sufficient for most use cases.

As a result of the above changes, a number of index management and index tuning configuration variables have been removed. See the APM [release notes](/release-notes/elastic-apm/release-notes.md), [breaking changes](https://www.elastic.co/guide/en/observability/current/apm-breaking.html) for full details.


## Find your upgrade guide [_find_your_upgrade_guide]

Starting in version 7.14, there are two ways to run Elastic APM. Determine which method you’re using, then use the links below to find the correct upgrading guide.

* **Standalone**: Users in this mode run and configure the APM Server binary.
* **{{fleet}} and the APM integration**: Users in this mode run and configure {{fleet}} and the Elastic APM integration.

**Self-installation (non-{{ecloud}} users) upgrade guides**

* [Self-installation standalone](upgrade-self-installation-of-apm-server-standalone-to-8x.md)
* [Self-installation APM integration](upgrade-self-installation-of-apm-integration-to-8x.md)

**{{ecloud}} upgrade guides**

* [{{ecloud}} standalone](upgrade-elastic-cloud-apm-server-standalone-to-8.md)
* [{{ecloud}} APM integration](upgrade-elastic-cloud-with-apm-integration-to-80.md)
