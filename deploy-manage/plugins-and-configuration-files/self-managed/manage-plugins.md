---
applies_to:
  deployment:
    self: ga
navigation_title: In self-managed
description: Install Elasticsearch plugins on self-managed clusters with a Docker configuration file or the elasticsearch-plugin CLI, and place shared config files on each node.
products:
  - id: elasticsearch
---

# Manage plugins on {{es}} self-managed deployments

How you install plugins depends on how you run {{es}}. Use a declarative configuration file with the official Docker image, or the `elasticsearch-plugin` CLI for package and archive installs. To browse available plugins, refer to [{{es}} plugins](elasticsearch://reference/elasticsearch-plugins/index.md).

To make synonym dictionaries, SAML metadata, or similar files available to {{es}}, place them in each node's [configuration directory](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#config-files-location) and reference them from your settings. This is the self-managed equivalent of *bundles* on {{ech}} and {{ece}}, which package those files as ZIP extensions rather than placing them directly on disk.

Refer to [](/deploy-manage/plugins-and-configuration-files.md) for options that apply to other deployment types.

## Install plugins with the Docker image [self-managed-plugins-docker]

::::{admonition} Docker only

This method is only available for [official {{es}} Docker images](https://www.docker.elastic.co/). Other {{es}} distributions will not start with a plugin configuration file present.

::::

If you run {{es}} with the [official Docker image](/deploy-manage/deploy/self-managed/install-elasticsearch-with-docker.md), declare the plugins you want in a file named `elasticsearch-plugins.yml`, and place it in the configuration directory alongside `elasticsearch.yml`:

```yaml
plugins:
  - id: analysis-icu
  - id: repository-azure
  - id: custom-mapper
    location: <EXAMPLE_URL>/archive/custom-mapper-1.0.0.zip
```

This example installs the official `analysis-icu` and `repository-azure` plugins, and one unofficial plugin. Every plugin must provide an `id`. Unofficial plugins must also provide a `location`, typically a URL, although Maven coordinates are also supported. The name of the downloaded plugin must match its `id`.

Each time the container starts, {{es}} compares this list against the plugins currently installed and adds or removes plugins so that the running set matches the file. Official plugins are also upgraded when you upgrade {{es}}. To change the set of plugins, edit the file and restart the container.

::::{important}
Do not run `elasticsearch-plugin install` or `elasticsearch-plugin remove` while the configuration file is present. Both commands are disabled.
::::

## Install plugins with the `elasticsearch-plugin` CLI [self-managed-plugins-cli]

For package and archive installs, use the `elasticsearch-plugin` tool on each node. 

By default, the tool is in `$ES_HOME/bin` and it installs plugins into `$ES_HOME/plugins`. Both locations depend on how you installed {{es}}, so check the directory layout for your package type:

* [`.tar.gz` archives](/deploy-manage/deploy/self-managed/install-elasticsearch-from-archive-on-linux-macos.md#targz-layout)
* [Windows `.zip` archives](/deploy-manage/deploy/self-managed/install-elasticsearch-with-zip-on-windows.md#windows-layout)
* [Debian packages](/deploy-manage/deploy/self-managed/install-elasticsearch-with-debian-package.md#deb-layout)
* [RPM packages](/deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md#rpm-layout)

::::{important}
If you installed {{es}} from the deb or rpm package, run `/usr/share/elasticsearch/bin/elasticsearch-plugin` as `root` so that it can write to the appropriate files on disk. Otherwise, run `bin/elasticsearch-plugin` as the user that owns all of the {{es}} files.
::::

To install an official plugin, pass its name. The following command installs the [ICU analysis plugin](elasticsearch://reference/elasticsearch-plugins/analysis-icu.md) at the version matching your {{es}} version:

```sh
sudo bin/elasticsearch-plugin install analysis-icu
```

To install a plugin that is not available by name, such as a community plugin or one you wrote yourself, pass a URL or a path to a local ZIP file instead. The plugin name is determined from its descriptor:

```sh
sudo bin/elasticsearch-plugin install <EXAMPLE_PLUGIN_HOST_URL>/plugin.zip
sudo bin/elasticsearch-plugin install file:///path/to/plugin.zip
```

You can combine any of these forms to install several plugins at once. The installation is treated as a transaction, so either all of the plugins are installed, or none of them are:

```sh
sudo bin/elasticsearch-plugin install analysis-icu file:///path/to/plugin.zip
```

## After you install a plugin

Restart each node before the plugin becomes available. Plugins that contribute custom cluster state metadata require a full cluster restart, although you can still upgrade those plugins with a rolling restart.

Plugins are built for a specific version of {{es}} and must be reinstalled each time you upgrade the cluster. Text analysis plugins created with the [stable plugin API](elasticsearch://extend/creating-stable-plugins.md) are the exception.

If a plugin is critical to your cluster, add it to the [`plugin.mandatory`](elasticsearch://reference/elasticsearch-plugins/mandatory-plugins.md) setting in `elasticsearch.yml` so that a node refuses to start when the plugin is missing.

## Reference

For the full `elasticsearch-plugin` command surface, refer to the following pages:

* [Listing, removing, and updating installed plugins](elasticsearch://reference/elasticsearch-plugins/listing-removing-updating.md)
* [Other command line parameters](elasticsearch://reference/elasticsearch-plugins/_other_command_line_parameters.md): batch mode, proxy settings, custom config directories, and exit codes
* [Custom URL or file system](elasticsearch://reference/elasticsearch-plugins/plugin-management-custom-url.md): self-signed certificates and platform-specific paths
