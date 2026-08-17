---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/plugins/current/_other_command_line_parameters.html
applies_to:
  deployment:
    self: ga
navigation_title: "Other CLI parameters"
description: Use silent, verbose, and related elasticsearch-plugin CLI options when installing plugins on self-managed clusters.
products:
  - id: elasticsearch
---

# Use other command line parameters [_other_command_line_parameters]

The `elasticsearch-plugin` script supports additional command line parameters.

## Silent/verbose mode [_silentverbose_mode]

The `--verbose` parameter outputs more debug information, while `--silent` turns off all output including the progress bar. The script may return the following exit codes:

`0`
:   Everything was OK

`64`
:   Unknown command or incorrect option parameter

`74`
:   IO error

`70`
:   Any other error

## Batch mode [_batch_mode]

Certain plugins require more privileges than those provided by default in core {{es}}. These plugins list the required privileges and ask for confirmation before continuing with installation.

When you run the plugin install script from another program (for example, install automation), the script should detect that it is not being called from a console and skip confirmation, automatically granting all requested permissions. If console detection fails, force batch mode with `-b` or `--batch`:

```sh
sudo bin/elasticsearch-plugin install --batch [pluginname]
```

## Custom config directory [_custom_config_directory]

If your `elasticsearch.yml` config file is in a custom location, specify the path to the config directory when using the plugin script:

```sh
sudo ES_PATH_CONF=/path/to/conf/dir bin/elasticsearch-plugin install <plugin name>
```

## Proxy settings [_proxy_settings]

To install a plugin through a proxy, add the proxy details to the `CLI_JAVA_OPTS` environment variable with the Java settings `http.proxyHost` and `http.proxyPort` (or `https.proxyHost` and `https.proxyPort`):

```sh
sudo CLI_JAVA_OPTS="-Dhttp.proxyHost=host_name -Dhttp.proxyPort=port_number -Dhttps.proxyHost=host_name -Dhttps.proxyPort=https_port_number" bin/elasticsearch-plugin install analysis-icu
```

Or on Windows:

```sh
set CLI_JAVA_OPTS="-Dhttp.proxyHost=host_name -Dhttp.proxyPort=port_number -Dhttps.proxyHost=host_name -Dhttps.proxyPort=https_port_number"
bin\elasticsearch-plugin install analysis-icu
```
