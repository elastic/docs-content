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


Providers supply the key-value pairs that are used for variable substitution and conditionals. Each provider's keys are automatically prefixed with the name of the provider in the context of the {{agent}}.

For example, if a provider named `foo` provides `{"key1": "value1", "key2": "value2"}`, the key-value pairs are placed in `{"foo" : {"key1": "value1", "key2": "value2"}}`. To reference the keys, use the variables `${foo.key1}` and `${foo.key2}`.


## Provider usage by deployment model [provider_usage_by_deployment_model]

How you use providers depends on whether you're running a standalone or a {{fleet}}-managed {{agent}}.

### Using providers on standalone {{agent}} [using-providers-standalone-agent]

On standalone {{agent}}, providers can be configured through the `providers` key in the `elastic-agent.yml` configuration file. By default, all providers are enabled, but {{agent}} runs them only if they are referenced in the configuration file or in an {{agent}} policy. Disabled providers are not run even if they are referenced.

You can enable, disable, and configure provider settings as needed. For more details, refer to [Provider configuration](#provider_configuration).

### Using providers on {{fleet}}-managed {{agent}} [using-providers-fleet-managed-agent]

On {{fleet}}-managed {{agent}}, you can use provider variables in integration policy settings (for example, `${host.name}`, `${env.foo}`, `${agent.id}`), but you cannot add a `providers` configuration block directly through the {{fleet}} UI.

Some providers can be configured on {{k8s}} deployments using ConfigMaps. For more details, refer to [Advanced {{agent}} configuration managed by {{fleet}}](/reference/fleet/advanced-kubernetes-managed-by-fleet.md).


## Provider configuration [provider_configuration]

On standalone {{agent}}, provider configuration is specified under the top-level `providers` key in the `elastic-agent.yml` configuration file. All registered providers are enabled by default but they are run by {{agent}} only if they are referenced. If a provider cannot connect, no mappings are produced.

All providers are prefixed without name collisions. The name of the provider is in the key in the configuration.

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

If a provider is referenced in an {{agent}} policy, it is turned on automatically unless it's explicitly disabled in the `elastic-agent.yml` configuration file. For example, to disable the Docker provider in a standalone {{agent}}, set:

```yaml
providers:
  docker:
    enabled: false
```

With this setting, {{agent}} will not run the Docker provider even if it's referenced in an {{agent}} policy.

{{agent}} supports two broad types of providers: [context](#context-providers) and [dynamic](#dynamic-providers).


### Context providers [context-providers]

Context providers give the current context of the running {{agent}}, for example, agent information (ID, version), host information (hostname, IP addresses), and environment information (environment variables).

They can only provide a single key-value mapping. Think of them as singletons; an update of a key-value mapping results in a re-evaluation of the entire configuration. These providers are normally very static, but not required. A value can change which results in re-evaluation.

Context providers use the {{product.ecs}} naming to ensure consistency and understanding throughout documentation and projects.

{{agent}} supports the following context providers:

* [Local provider](/reference/fleet/local-provider.md)
* [Agent provider](/reference/fleet/agent-provider.md)
* [Host provider](/reference/fleet/host-provider.md)
* [Env provider](/reference/fleet/env-provider.md)
* [Kubernetes Secrets provider](/reference/fleet/kubernetes_secrets-provider.md)
* [Kubernetes LeaderElection provider](/reference/fleet/kubernetes_leaderelection-provider.md)


### Dynamic providers [dynamic-providers]

Dynamic providers give an array of multiple key-value mappings. Each key-value mapping is combined with the previous context provider’s key and value mapping which provides a new unique mapping that is used to generate a configuration.

{{agent}} supports the following context providers:

* [Local dynamic provider](/reference/fleet/local-dynamic-provider.md)
* [Docker provider](/reference/fleet/docker-provider.md)
* [Kubernetes provider](/reference/fleet/kubernetes-provider.md)


### Disabling providers by default [disable-providers-by-default]

Registered providers are run by {{agent}} if they are referenced in the {{agent}} configuration or in a policy.

On standalone {{agent}}, you can disable all providers by setting `agent.providers.initial_default: false`, preventing them from running even if they are referenced.

The following configuration disables all providers with the exception of the Docker provider, which is run when it's referenced in the policy:

```yaml
agent.providers.initial_default: false
providers:
  docker:
    enabled: true
```
