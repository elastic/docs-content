---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/plugins/current/manage-plugins-using-configuration-file.html
applies_to:
  deployment:
    self: ga
navigation_title: "Config file (Docker)"
description: Declare Elasticsearch plugins in elasticsearch-plugins.yml so Docker containers install and sync them on every start.
products:
  - id: elasticsearch
---

# Manage plugins using a configuration file [manage-plugins-using-configuration-file]

::::{admonition} Docker only
:class: important

This feature is only available for [official {{es}} Docker images](https://www.docker.elastic.co/). Other {{es}} distributions will not start with a plugin configuration file.

::::

If you run a self-managed {{es}} cluster with the [official Docker image](/deploy-manage/deploy/self-managed/install-elasticsearch-with-docker.md), manage plugins with a declarative configuration file instead of the `elasticsearch-plugin` CLI. For package and archive installs, use [Install plugins](install-plugins.md).

When {{es}} starts, it compares the plugins listed in the file with those currently installed, and adds or removes plugins as required. {{es}} also upgrades official plugins when you upgrade {{es}} itself. To change the set of plugins, edit the file and restart the container. Do not run `elasticsearch-plugin install` or `remove` when the configuration file is present; those commands are disabled.

The file is called `elasticsearch-plugins.yml` and must be placed in the {{es}} configuration directory, alongside `elasticsearch.yml`. Example:

```yaml
plugins:
  - id: analysis-icu
  - id: repository-azure
  - id: custom-mapper
    location: <EXAMPLE_URL>/archive/custom-mapper-1.0.0.zip
```

This example installs the official `analysis-icu` and `repository-azure` plugins, and one unofficial plugin. Every plugin must provide an `id`. Unofficial plugins must also provide a `location`. This is typically a URL, but Maven coordinates are also supported. The downloaded plugin’s name must match the ID in the configuration file.

While {{es}} respects the [standard Java proxy system properties](https://docs.oracle.com/javase/8/docs/technotes/guides/net/proxies.md) when downloading plugins, you can also configure an HTTP proxy explicitly in the configuration file:

```yaml
plugins:
  - id: custom-mapper
    location: <EXAMPLE_URL>/archive/custom-mapper-1.0.0.zip
proxy: proxy.example.com:8443
```

You can also use [mandatory plugins](mandatory-plugins.md) so a node fails to start if a required plugin is missing.

For more Docker configuration guidance, refer to [Configure {{es}} with Docker](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-configure.md). Refer to [Plugins and bundles](/deploy-manage/plugins-and-bundles.md) for options that apply to other deployment types.
