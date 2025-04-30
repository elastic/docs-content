---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/local-provider.html
applies_to:
  stack:
products:
  - Fleet
  - Elastic Agent
---

# Local [local-provider]

Provides custom keys to use as variables. For example:

```yaml
providers:
  local:
    vars:
      foo: bar
```

