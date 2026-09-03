---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/plugins/current/mandatory-plugins.html
applies_to:
  deployment:
    self: ga
navigation_title: "Mandatory plugins"
description: Require specific Elasticsearch plugins so nodes refuse to start if a critical plugin is missing.
products:
  - id: elasticsearch
---

# Configure mandatory plugins [mandatory-plugins]

If you rely on certain plugins, you can define mandatory plugins by adding the `plugin.mandatory` setting to `config/elasticsearch.yml`. For example:

```yaml
plugin.mandatory: analysis-icu,lang-js
```

For safety, a node will not start if it is missing a mandatory plugin.

To learn how settings are applied across deployment types, refer to [Stack settings](/deploy-manage/stack-settings.md).
