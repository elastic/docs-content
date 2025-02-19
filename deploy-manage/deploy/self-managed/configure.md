---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/settings.html
---

# Configure [settings]

The {{kib}} server reads properties from the `kibana.yml` file on startup. The location of this file differs depending on how you installed {{kib}}. For example, if you installed {{kib}} from an archive distribution (`.tar.gz` or `.zip`), by default it is in `$KIBANA_HOME/config`. By default, with package distributions (Debian or RPM), it is in `/etc/kibana`.  The config directory can be changed via the `KBN_PATH_CONF` environment variable:

```text
KBN_PATH_CONF=/home/kibana/config ./bin/kibana
```

The default host and port settings configure {{kib}} to run on `localhost:5601`. To change this behavior and allow remote users to connect, you’ll need to update your `kibana.yml` file. You can also enable SSL and set a variety of other options.

Environment variables can be injected into configuration using `${MY_ENV_VAR}` syntax. By default, configuration validation will fail if an environment variable used in the config file is not present when Kibana starts. This behavior can be changed by using a default value for the environment variable, using the `${MY_ENV_VAR:defaultValue}` syntax.

For a list of settings, refer to [](asciidocalypse://kibana/docs/reference/configuration-reference)