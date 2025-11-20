---
navigation_title: Agent providers
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/providers.html
applies_to:
  stack: ga
products:
  - id: fleet
  - id: elastic-agent
---

# {{agent}} providers [providers]

Providers supply key-value pairs for variable substitution and conditional logic. In other words, they define dynamic values {{agent}} can use when building configurations.

Each provider’s keys are automatically grouped under the provider name within the {{agent}} context. For example, if the `foo` provider supplies `{"key1": "value1", "key2": "value2"}`, {{agent}} stores these key-value pairs as `{"foo": {"key1": "value1", "key2": "value2"}}`.
You can then reference the values using the `${foo.key1}` and `${foo.key2}` variables.

How you can configure and use {{agent}} providers depends on whether you're running a standalone or a {{fleet}}-managed {{agent}}. For more information, refer to:

* [Configure providers on standalone {{agent}}](#configure-providers-standalone-agent)
* [Using providers on {{fleet}}-managed {{agent}}](#using-providers-fleet-managed-agent)


## Provider types

{{agent}} supports two types of providers: [context](#context-providers) and [dynamic](#dynamic-providers).


### Context providers [context-providers]

Context providers supply the current context of the running {{agent}} such as agent information (ID, version), host information (hostname, IP addresses), and environment information (environment variables).

These providers supply only a single key-value mapping. They are generally static, although this is not required. If the key's value changes, the entire configuration is re-evaluated.

To ensure consistency and clarity across documentation and projects, context providers use the {{product.ecs}} naming conventions.

{{agent}} supports the following context providers:

* [Local provider](/reference/fleet/local-provider.md) - Provides custom keys to use as variables.
* [Agent provider](/reference/fleet/agent-provider.md) - Provides information about the {{agent}} such as ID, version, and build details.
* [Host provider](/reference/fleet/host-provider.md) - Provides information about the current host such as hostname, IP addresses, platform, and architecture.
* [Env provider](/reference/fleet/env-provider.md) - Provides access to environment variables as key-value pairs.
* [{{k8s}} Secrets provider](/reference/fleet/kubernetes_secrets-provider.md) - Provides access to the {{k8s}} Secrets API.
* [{{k8s}} LeaderElection provider](/reference/fleet/kubernetes_leaderelection-provider.md) - Enables leader election between {{agent}} instances running on {{k8s}} to ensure only one agent holds the leader lock.


### Dynamic providers [dynamic-providers]

Dynamic providers supply an array of multiple key-value mappings. Each key-value mapping is combined with the previous context provider’s key and value mapping which provides a new unique mapping that is used to generate a configuration.

{{agent}} supports the following dynamic providers:

* [Local dynamic provider](/reference/fleet/local-dynamic-provider.md) - Defines multiple key-value pairs to generate multiple configurations.
* [Docker provider](/reference/fleet/docker-provider.md) - Provides Docker container metadata such as ID, name, image, and labels.
* [{{k8s}} provider](/reference/fleet/kubernetes-provider.md) - Provides metadata from {{k8s}} resources such as pods, nodes, and services.


## Configure providers on standalone {{agent}} [configure-providers-standalone-agent]

On standalone {{agent}}, providers can be configured through the top-level `providers` key in the `elastic-agent.yml` configuration file. By default, all providers are enabled, but {{agent}} runs them only if they are referenced in the configuration file or in an {{agent}} policy. Disabled providers are not run even if they are referenced. If a provider cannot connect, no mappings are produced.

You can enable, disable, and configure provider settings as needed. All providers are prefixed without name collisions. In the configuration, the name of the provider is in the key.

The following example shows two providers (`local` and `local_dynamic`) that supply custom keys on a standalone {{agent}}:

```yaml
providers:
  local:
    vars:
      foo: bar
  local_dynamic:
    items:
      - vars:
          item: key1
      - vars:
          item: key2
      - vars:
          item: key3
```

If a provider is referenced in an {{agent}} policy, it is turned on automatically unless it's explicitly disabled in the `elastic-agent.yml` configuration file.


### Disable providers [disable-providers-by-default]

On standalone {{agent}}, you can disable a specific provider, so it cannot be run even if it is referenced. For example, to disable the Docker provider on a standalone {{agent}}, set:

```yaml
providers:
  docker:
    enabled: false
```

With this setting, {{agent}} will not run the Docker provider even if it's referenced in an {{agent}} policy.

You can also disable all providers by setting `agent.providers.initial_default: false`. The following configuration disables all providers with the exception of the Docker provider, which is run when it's referenced in the policy:

```yaml
agent.providers.initial_default: false
providers:
  docker:
    enabled: true
```


## Using providers on {{fleet}}-managed {{agent}} [using-providers-fleet-managed-agent]

On {{fleet}}-managed {{agent}}, you can use provider variables in integration policy settings (for example, `${host.name}`, `${env.foo}`, `${agent.id}`), but you cannot add a `providers` configuration block directly through the {{fleet}} UI.

Some providers can be configured on {{k8s}} deployments using ConfigMaps. For more details, refer to [Advanced {{agent}} configuration managed by {{fleet}}](/reference/fleet/advanced-kubernetes-managed-by-fleet.md).