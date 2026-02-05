---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/local-provider.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Local provider [local-provider]

Provides custom keys to use as variables. For example:

```yaml
providers:
  local:
    vars:
      foo: bar
```

