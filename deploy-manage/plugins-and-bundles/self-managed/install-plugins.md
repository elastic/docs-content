---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/plugins/current/installation.html
applies_to:
  deployment:
    self: ga
navigation_title: "Install with CLI"
description: Install Elasticsearch plugins on self-managed package and archive installs with the elasticsearch-plugin CLI.
products:
  - id: elasticsearch
---

# Install plugins [installation]

Each plugin typically documents its own installation requirements. This page covers the `elasticsearch-plugin` CLI for self-managed package and archive installs.

If you run {{es}} with the [official Docker image](/deploy-manage/deploy/self-managed/install-elasticsearch-with-docker.md), use the declarative [configuration file](manage-plugins-using-configuration-file.md) instead of running `elasticsearch-plugin install` directly.

Refer to [Plugins and bundles](/deploy-manage/plugins-and-bundles.md) for options that apply to other deployment types.

The `elasticsearch-plugin` tool is located in the `$ES_HOME/bin` directory by default, but it might be in a different location depending on which {{es}} package you installed. For more information, see [Plugins directory](plugins-directory.md).

Run the following command to get usage instructions:

```sh
sudo bin/elasticsearch-plugin -h
```

::::{important}
If {{es}} was installed using the deb or rpm package, then run `/usr/share/elasticsearch/bin/elasticsearch-plugin` as `root` so it can write to the appropriate files on disk. Otherwise, run `bin/elasticsearch-plugin` as the user that owns all of the {{es}} files.
::::

## Core {{es}} plugins [_core_elasticsearch_plugins]

Core {{es}} plugins can be installed as follows:

```sh
sudo bin/elasticsearch-plugin install [plugin_name]
```

For example, to install the core [ICU plugin](elasticsearch://reference/elasticsearch-plugins/analysis-icu.md):

```sh
sudo bin/elasticsearch-plugin install analysis-icu
```

This command installs the version of the plugin that matches your {{es}} version and shows a progress bar while downloading.

After installation, restart each node before the plugin is available. Plugins that contribute custom cluster state metadata require a full cluster restart. You can still upgrade those plugins with a rolling restart.

## Next steps

* [Install from a custom URL or file system](custom-url.md)
* [Install multiple plugins](install-multiple-plugins.md)
* [List, remove, and update plugins](list-remove-update.md)
* [Other command line parameters](other-command-line-parameters.md)
