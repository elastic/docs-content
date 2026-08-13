---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/plugins/current/installing-multiple-plugins.html
applies_to:
  deployment:
    self: ga
navigation_title: "Install multiple plugins"
description: Install several Elasticsearch plugins in one elasticsearch-plugin command on self-managed deployments.
products:
  - id: elasticsearch
---

# Install multiple plugins [installing-multiple-plugins]

Multiple plugins can be installed in one invocation:

```sh
sudo bin/elasticsearch-plugin install [plugin_id] [plugin_id] ... [plugin_id]
```

Each `plugin_id` can be any valid form for installing a single plugin (for example, the name of a core plugin, or a custom URL).

For example, to install the core [ICU plugin](elasticsearch://reference/elasticsearch-plugins/analysis-icu.md):

```sh
sudo bin/elasticsearch-plugin install analysis-icu
```

This command installs the versions of the plugins that match your {{es}} version. The installation is treated as a transaction: all of the plugins are installed, or none of them are installed if any installation fails.
