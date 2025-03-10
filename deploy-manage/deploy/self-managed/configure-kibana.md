---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/settings.html
applies_to:
  deployment:
    self:
---

# Configure {{kib}} [settings]

The {{kib}} server reads properties from the `kibana.yml` file on startup. 

The location of this file differs depending on how you installed {{kib}}

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

For a complete list of settings that you can apply to {{kib}}, refer to [{{kib}} configuration reference](kibana:///reference/configuration-reference.md).


* Link to areas to configure SSL certificates to encrypt client browsers communications (HTTPS) --> This is a bit unclear and difficult as the HTTPS endpoint configuration in Kibana appears in Elasticsearch documentation.
* Link to "Secure access to Kibana" elastic.co/guide/en/kibana/current/tutorial-secure-access-to-kibana.html
* Link to Use Kibana in production (with load balancers): elastic.co/guide/en/kibana/current/production.html
* Link to doc about using more than 1 Kibana instance? (not sure if it exists though)