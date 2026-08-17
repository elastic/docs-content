---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/plugins/current/plugin-management-custom-url.html
applies_to:
  deployment:
    self: ga
navigation_title: "Custom URL or file system"
description: Install an Elasticsearch plugin from a custom URL or local ZIP when it is not available by name.
products:
  - id: elasticsearch
---

# Install from a custom URL or file system [plugin-management-custom-url]

A plugin can also be downloaded from a custom location by specifying a URL:

```sh
sudo bin/elasticsearch-plugin install [url] <1>
```

1. Must be a valid URL. The plugin name is determined from its descriptor.

Unix
:   To install a plugin from your local file system at `/path/to/plugin.zip`:

    ```sh
    sudo bin/elasticsearch-plugin install file:///path/to/plugin.zip
    ```

Windows
:   To install a plugin from your local file system at `C:\path\to\plugin.zip`:

    ```sh
    bin\elasticsearch-plugin install file:///C:/path/to/plugin.zip
    ```

    ::::{note}
    Any path that contains spaces must be wrapped in quotes.
    ::::

    ::::{note}
    If you install a plugin from the filesystem, the plugin distribution must not be contained in the `plugins` directory for the node that you are installing to, or installation will fail.
    ::::

HTTP
:   To install a plugin from an HTTP URL:

    ```sh
    sudo bin/elasticsearch-plugin install <EXAMPLE_PLUGIN_HOST_URL>/plugin.zip
    ```

    The plugin script refuses to talk to an HTTPS URL with an untrusted certificate. To use a self-signed HTTPS cert, add the CA cert to a local Java truststore and pass the location to the script:

    ```sh
    sudo CLI_JAVA_OPTS="-Djavax.net.ssl.trustStore=/path/to/trustStore.jks" bin/elasticsearch-plugin install <MY_HOST_URL>/plugin.zip
    ```
