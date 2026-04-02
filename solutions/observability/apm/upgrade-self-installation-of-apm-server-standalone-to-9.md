---
navigation_title: Self-installation standalone
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-upgrade-8.0-self-standalone.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# Upgrade a self-installation of APM Server standalone to 9.0 [apm-upgrade-9.0-self-standalone]

This upgrade guide is for the standalone method of running APM Server. Only use this guide if both of the following are true:

* You have a self-installation of the {{stack}}, i.e. you’re not using {{ecloud}}.
* You’re running the APM Server binary, i.e. you haven’t switched to the Elastic APM integration.

## Prerequisites [_prerequisites_8]

1. Prior to upgrading to version 9.0, {{es}}, {{kib}}, and APM Server must be upgraded to version 8.18.

    * To upgrade {{es}} and {{kib}}, refer to the [{{stack}} Installation and Upgrade Guide](https://www.elastic.co/guide/en/elastic-stack/8.18/upgrading-elastic-stack.html)
    * To upgrade APM Server to version 8.18, refer to [upgrade to version 8.18](https://www.elastic.co/guide/en/observability/8.18/apm-upgrading-to-8.x.html).

2. Review the [Elastic APM release notes](apm-server://release-notes/index.md) and [Elastic {{observability}} release notes](/release-notes/elastic-observability/index.md).
3. Review the [Elastic APM breaking changes](apm-server://release-notes/breaking-changes.md).

## Upgrade steps [_upgrade_steps]

1. **Upgrade the {{stack}} to version 9.0**

    The {{stack}} ({{es}} and {{kib}}) must be upgraded before APM Server. Refer to the [{{stack}} Installation and Upgrade Guide](/deploy-manage/upgrade/deployment-or-cluster.md) for guidance.

2. **Install the 9.0 APM Server release**

    Refer to [install](/solutions/observability/apm/apm-server/binary.md#apm-installing) to find the command that works with your system.

3. **Review your configuration file**

    Some settings have been removed or changed. You may need to update your `apm-server.yml` configuration file prior to starting the APM Server. Refer to [Installation layout](/solutions/observability/apm/apm-server/installation-layout.md) for help in locating this file, and [Configure APM Server](/solutions/observability/apm/apm-server/configure.md) for a list of all available configuration options.

4. **Start the APM Server**

    To start the APM Server, run:

    ```bash
    ./apm-server -e
    ```

    Additional details are available in [start the APM Server](/solutions/observability/apm/apm-server/binary.md#apm-server-starting).

5. When upgrading from 8.18 to 9.0, if you have 7.x indices, you need to either set the indices to `readonly`, or if reindexing, add [ILM privileges](https://www.elastic.co/guide/en/apm/guide/7.17/privileges-to-setup-beats.html#_set_up_ilm) for `reindexed-v*-apm*` indices.

6. **(Optional) Upgrade to the APM integration**

    Got time for one more upgrade? Refer to [Switch to the Elastic APM integration](/solutions/observability/apm/switch-to-elastic-apm-integration.md).
