---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/env-provider.html
products:
  - id: fleet
  - id: elastic-agent
---

# Env Provider [env-provider]

Provides access to the environment variables as key-value pairs.

For example, set the variable `foo`:

```shell
foo=bar elastic-agent run
```

The environment variable can be referenced as `${env.foo}`.

::::{note}
If you run the agent as a Linux or Windows service, you can also define the environment variables in the service manifest. Refer to the example in [Proxy Server connectivity using default host variables](/reference/fleet/host-proxy-env-vars.md).
::::
