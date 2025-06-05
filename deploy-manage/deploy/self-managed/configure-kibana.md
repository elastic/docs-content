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