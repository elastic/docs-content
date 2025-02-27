---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/env-provider.html
---

# Env Provider [env-provider]

Provides access to the environment variables as key-value pairs.

For example, set the variable `foo`:

```shell
foo=bar elastic-agent run
```

The environment variable can be referenced as `${env.foo}`.

