---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/plugins/current/listing-removing-updating.html
applies_to:
  deployment:
    self: ga
navigation_title: "List, remove, and update"
description: List, remove, and update installed Elasticsearch plugins on self-managed nodes with the CLI.
products:
  - id: elasticsearch
---

# List, remove, and update installed plugins [listing-removing-updating]

## List plugins [_listing_plugins]

Retrieve the currently loaded plugins with the `list` option:

```sh
sudo bin/elasticsearch-plugin list
```

Alternatively, use the [nodes info API]({{es-apis}}operation/operation-nodes-info) to find out which plugins are installed on each node in the cluster.

## Remove plugins [_removing_plugins]

Plugins can be removed manually by deleting the appropriate directory under `plugins/`, or with the plugin script:

```sh
sudo bin/elasticsearch-plugin remove [pluginname]
```

After a Java plugin has been removed, restart the node to complete the removal.

By default, plugin configuration files (if any) are preserved on disk so configuration is not lost while upgrading a plugin. To purge configuration files while removing a plugin, use `-p` or `--purge`. You can also use this option after a plugin is removed to clean up lingering configuration files.

## Remove multiple plugins [removing-multiple-plugins]

Remove multiple plugins in one invocation:

```sh
sudo bin/elasticsearch-plugin remove [pluginname] [pluginname] ... [pluginname]
```

## Update plugins [_updating_plugins]

Except for text analysis plugins created using the [stable plugin API](elasticsearch://extend/creating-stable-plugins.md), plugins are built for a specific version of {{es}} and must be reinstalled each time {{es}} is updated.

```sh
sudo bin/elasticsearch-plugin remove [pluginname]
sudo bin/elasticsearch-plugin install [pluginname]
```
