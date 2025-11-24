---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/env-provider.html
applies_to:
  stack: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Env provider [env-provider]

The env provider gives access to the environment variables available to the {{agent}} process as key-value pairs. You can then reference these values in the {{agent}} configuration (for standalone agents) or in agent and integration policies in {{fleet}}.

Using environment variables lets you keep host-specific settings and deployment-specific values out of your policies and configuration files. This is especially useful in larger setups where you want to reuse the same {{agent}} policy but allow each host or container to supply its own settings.

Use the env provider when you want to:

- Provide host-specific or environment-specific values, such as proxy settings, regions, or service URLs.
- Reuse shared policies across agents while allowing each host, container, or service to define its own configuration through environment variables.


## Using the env provider [using_env_provider]

The env provider is enabled by default and requires no configuration. Define environment variables in your operating system, service definition, or container platform, and reference them in the {{agent}} configuration or {{fleet}} policy using the `${env.VAR_NAME}` syntax.

For example:

:::::{tab-set}

::::{tab-item} Standalone {{agent}}

On standalone {{agent}}, you can reference environment variables directly in the `elastic-agent.yml` configuration file.

For example, to use an environment variable as the value of the {{es}} host URL:

```yaml
outputs:
  default:
    type: elasticsearch
    hosts: ["${env.ELASTICSEARCH_HOST}"]
```

Then set the environment variable before starting {{agent}}:

```shell
ELASTICSEARCH_HOST=https://elasticsearch:9200 elastic-agent run
```

The standalone agent resolves `${env.ELASTICSEARCH_HOST}` at runtime based on the environment of the agent process.
::::

::::{tab-item} {{fleet}}-managed {{agent}}

On {{fleet}}-managed {{agent}}, you can define environment variables on each host running {{agent}} and reference them in the integration or agent policy using the `${env.VAR_NAME}` syntax.

For example, you can use an environment variable to set a host-specific log path in a filestream integration:

```yaml
inputs:
  - type: filestream
    enabled: true
    streams:
      - paths:
          - "${env.APP_LOG_DIR}/app.log"
```

Each {{agent}} uses the env provider to resolve `${env.APP_LOG_DIR}` from the environment variables defined on the host at runtime. This allows a single policy in {{fleet}} to adapt its behavior per host without creating multiple policies.
::::

:::::

:::{note}
If you're running {{agent}} as a Linux or Windows service, you can define environment variables in the service manifest or environment configuration. Refer to the example in [Proxy Server connectivity using default host variables](/reference/fleet/host-proxy-env-vars.md) for more details.

For containerized deployments, refer to [{{agent}} environment variables](/reference/fleet/agent-environment-variables.md) for a list of supported variables.
:::


## Variable chaining and fallbacks [env_provider_fallbacks]

The env provider supports chaining multiple variables with fallback values. This is useful when you want to try multiple environment variables in order, with a default value when none are set.

Using fallbacks helps you create robust policies that work across different environments without requiring every variable to be defined on every host or container.

Use the following syntax:

```yaml
${env.VAR1|env.VAR2|env.VAR3|'default-value'} <1>
```

1. {{agent}} evaluates the expression at runtime from left to right. If none of the variables are set, it uses the final literal value (in this example, `'default-value'`).

You can chain as many environment variables as needed, and the final fallback can be any literal string or value that the configuration field accepts.

For example:

```yaml
logging.level: ${env.LOG_LEVEL|env.DEFAULT_LOG_LEVEL|'info'}
```

This tries the `LOG_LEVEL` environment variable first, then `DEFAULT_LOG_LEVEL`, and finally defaults to `'info'` if neither variable is set.