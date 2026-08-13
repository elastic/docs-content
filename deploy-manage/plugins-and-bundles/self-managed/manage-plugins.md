---
applies_to:
  deployment:
    self: ga
navigation_title: Extend self-managed
description: Install Elasticsearch plugins on self-managed clusters with a Docker config file or the CLI, and place shared config files on each node.
products:
  - id: elasticsearch
---

# Manage plugins on {{es}} self-managed deployments

How you manage plugins depends on how you run {{es}}. Use a declarative configuration file with the official Docker image, or the `elasticsearch-plugin` CLI for package and archive installs.

To make synonym dictionaries, scripts, SAML metadata, or similar files available to {{es}}, place them on each node's [configuration directory](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#config-files-location) and reference them from your settings. This is the self-managed equivalent of *bundles* on {{ech}} and {{ece}}, which package those files as ZIP extensions rather than placing them directly on disk.

Refer to [Plugins and bundles](/deploy-manage/plugins-and-bundles.md) for options that apply to other deployment types.

## Manage plugins with the Docker image

If you run {{es}} using the [official {{es}} Docker image](https://www.docker.elastic.co/), declare the plugins you want in `elasticsearch-plugins.yml` in the configuration directory, alongside `elasticsearch.yml`.

Each time the container starts, {{es}} compares that list with the plugins currently installed and installs, removes, or upgrades them so the running set matches the file. Official plugins are also upgraded when you upgrade {{es}}. To change the set of plugins, edit the file and restart the container. Do not run `elasticsearch-plugin install` or `remove` when the configuration file is present; those commands are disabled.

Refer to [Manage plugins using a configuration file](manage-plugins-using-configuration-file.md) for the file format, unofficial plugin locations, and proxy settings. You can also [require mandatory plugins](mandatory-plugins.md) so a node refuses to start if a critical plugin is missing.

## Manage plugins with package and archive installs

For all other installation methods, use the `elasticsearch-plugin` command-line tool to [install](install-plugins.md), [list, remove, and update](list-remove-update.md) plugins on each node. You can also [install multiple plugins](install-multiple-plugins.md) in a single command, or install from a [custom URL or file system](custom-url.md). The tool lives under `$ES_HOME/bin` by default; the exact path depends on your package. See [Plugins directory](plugins-directory.md).

After you install a plugin, restart each node before it becomes available. You can [require mandatory plugins](mandatory-plugins.md) so a node refuses to start if a critical plugin is missing. For silent, verbose, and related options, refer to [Other command line parameters](other-command-line-parameters.md).

