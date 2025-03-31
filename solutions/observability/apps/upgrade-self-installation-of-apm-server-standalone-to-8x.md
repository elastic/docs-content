---
navigation_title: "Self-installation standalone"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-upgrade-8.0-self-standalone.html
---



# Upgrade a self-installation of APM Server standalone to 8.x [apm-upgrade-8.0-self-standalone]


This upgrade guide is for the standalone method of running APM Server. Only use this guide if both of the following are true:

* You have a self-installation of the {{stack}}, i.e. you’re not using {{ecloud}}.
* You’re running the APM Server binary, i.e. you haven’t switched to the Elastic APM integration.


## Prerequisites [_prerequisites_8]

1. Prior to upgrading to version 9.0.0-beta1, {{es}}, {{kib}}, and APM Server must be upgraded to version 7.17.

    * To upgrade {{es}} and {{kib}}, see the [{{stack}} Installation and Upgrade Guide](https://www.elastic.co/guide/en/elastic-stack/7.17/upgrading-elastic-stack.html)
    * To upgrade APM Server to version 7.17, see [upgrade to version 7.17](https://www.elastic.co/guide/en/apm/guide/7.17/upgrading-to-717.html).

2. Review the [Elastic APM release notes](apm-server://release-notes/index.md) and [Elastic {{observability}} release notes](/release-notes/elastic-observability/index.md).


## Upgrade steps [_upgrade_steps]

1. **Upgrade the {{stack}} to version 9.0.0-beta1**

    The {{stack}} ({{es}} and {{kib}}) must be upgraded before APM Server. See the [{{stack}} Installation and Upgrade Guide](../../../deploy-manage/upgrade/deployment-or-cluster.md) for guidance.

2. **Install the 9.0.0-beta1 APM Server release**

    See [install](apm-server-binary.md#apm-installing) to find the command that works with your system.

3. **Review your configuration file**

    Some settings have been removed or changed. You may need to update your `apm-server.yml` configuration file prior to starting the APM Server. See [Installation layout](installation-layout.md) for help in locating this file, and [Configure APM Server](configure-apm-server.md) for a list of all available configuration options.

4. **Start the APM Server**

    To start the APM Server, run:

    ```bash
    ./apm-server -e
    ```

    Additional details are available in [start the APM Server](apm-server-binary.md#apm-server-starting).

5. **(Optional) Upgrade to the APM integration**

    Got time for one more upgrade? See [Switch to the Elastic APM integration](switch-to-elastic-apm-integration.md).
