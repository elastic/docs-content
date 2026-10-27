---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/settings.html
applies_to:
  deployment:
    self:
products:
  - id: kibana
---

# Configure {{kib}} [settings]

The {{kib}} server reads properties from the `kibana.yml` file on startup. 

The location of this file differs depending on how you installed {{kib}}:

* **Archive distributions (`.tar.gz` or `.zip`)**: Default location is `$KIBANA_HOME/config`
* **Package distributions (Debian or RPM)**: Default location is `/etc/kibana`

The config directory can be changed using the `KBN_PATH_CONF` environment variable:

```text
KBN_PATH_CONF=/home/kibana/config ./bin/kibana
```

The default host and port settings configure {{kib}} to run on `localhost:5601`. To change this behavior and allow remote users to connect, you need to update your [`server.host`](kibana://reference/configuration-reference/general-settings.md#server-host) and [`server.port`](kibana://reference/configuration-reference/general-settings.md#server-port) settings in the `kibana.yml` file.

In this file, you can also enable SSL and set a variety of other options.

Environment variables can be injected into configuration using `${MY_ENV_VAR}` syntax. By default, configuration validation will fail if an environment variable used in the config file is not present when {{kib}} starts. This behavior can be changed by using a default value for the environment variable, using the `${MY_ENV_VAR:defaultValue}` syntax.

## Available settings

For a complete list of settings that you can apply to {{kib}}, refer to [{{kib}} configuration reference](kibana://reference/configuration-reference.md).

## Reload configuration without restarting [reload-configuration]

Most {{kib}} settings are read only at startup, so changing them requires a restart. However, you can update some settings without restarting {{kib}} by sending a `SIGHUP` signal to the running process. The settings described in this section support this type of reload on Unix-like systems. On Windows, you must restart {{kib}} to apply changes made in `kibana.yml`.

:::{important}
If {{kib}} cannot parse the updated `kibana.yml` or validate the settings being reloaded, it shuts down. Check your changes before sending `SIGHUP`.
:::

### Reload logging settings [reload-logging-settings]

You can reload [{{kib}} logging settings](/deploy-manage/monitor/logging-configuration/kibana-logging.md) without restarting {{kib}}. This is useful when you need to temporarily increase logging verbosity while troubleshooting. You can change `logging.root.level`, configure a [dedicated logger](/deploy-manage/monitor/logging-configuration/kib-advanced-logging.md#dedicated-loggers), or increase verbosity for log records that match specific metadata. Reload the configuration and collect the detailed logs you need. When you finish, restore the original settings and reload the configuration.

For all available logging settings, refer to the [{{kib}} logging configuration reference](kibana://reference/configuration-reference/logging-settings.md).

To reload the logging configuration:

1. Update the `logging` settings in `kibana.yml` to configure the log levels, output, or filtering you need.
2. Send a `SIGHUP` signal to the running {{kib}} process to reload the configuration:

    ```sh
    kill -HUP <kibana_pid>
    ```

    On [Docker](/deploy-manage/deploy/self-managed/install-kibana-with-docker.md), signal the container instead:

    ```sh
    docker kill --signal=HUP <container_id>
    ```

    If you run {{kib}} with multiple worker processes, send the signal to each process.

3. Confirm the reload in the {{kib}} logs. A successful reload produces a message similar to:

    ```text
    Reloaded Kibana configuration (reason: SIGHUP signal received).
    ```

4. Verify that the updated logging settings produce the expected output.

5. If the logging changes are temporary, restore the original settings and send another `SIGHUP` signal to reload the configuration.

## Additional topics

Refer to the following documentation to learn how to perform key configuration tasks for {{kib}}: 

* [Configure SSL certificates](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-kibana-browser) to encrypt traffic between client browsers and {{kib}}
* [Enable authentication providers](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md) for {{kib}}
* Configure the {{kib}} [reporting feature](/deploy-manage/kibana-reporting-configuration.md)
* Use [Spaces](/deploy-manage/manage-spaces.md) to organize content in {{kib}}, and restrict access to this content to specific users
* Use [Connectors](/deploy-manage/manage-connectors.md) to manage connection information between {{es}}, {{kib}}, and third-party systems
* Present a [user access agreement](/deploy-manage/users-roles/cluster-or-deployment-auth/access-agreement.md) when logging on to {{kib}}
* Review [considerations for using {{kib}} in production](/deploy-manage/production-guidance/kibana-in-production-environments.md), including using load balancers
* [Monitor events inside and outside of {{kib}}](/deploy-manage/monitor.md)
* [Configure logging](/deploy-manage/monitor/logging-configuration.md)
* [Secure](/deploy-manage/security.md) {{kib}} communications and resources