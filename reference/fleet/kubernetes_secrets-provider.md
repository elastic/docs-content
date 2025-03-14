---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/kubernetes_secrets-provider.html
---

# Kubernetes Secrets Provider [kubernetes_secrets-provider]

Provides access to the Kubernetes Secrets API.

Use the format `${kubernetes_secrets.<default>.<somesecret>.<value>}` to reference a Kubernetes Secrets variable, where `default` is the namespace of the Secret, `somesecret` is the name of the Secret and `value` is the field of the Secret to access.

To obtain the values for the secrets, a request to the API Server is made. To avoid multiple requests for the same secret and to not overwhelm the API Server, a cache to store the values is used by default. This configuration can be set by using the variables `cache_*` (see below).

The provider needs a `kubeconfig` file to establish connection to the Kubernetes API. It can automatically reach the API if it’s run in an InCluster environment ({{agent}} runs as pod).

```yaml
providers.kubernetes_secrets:
  #kube_config: /Users/elastic-agent/.kube/config
  #kube_client_options:
  #  qps: 5
  #  burst: 10
  #cache_disable: false
  #cache_refresh_interval: 60s
  #cache_ttl: 1h
  #cache_request_timeout: 5s
```

`kube_config`
:   (Optional) Use the given config file as configuration for the Kubernetes client. If `kube_config` is not set, `KUBECONFIG` environment variable will be checked and will fall back to InCluster if it’s not present.

`kube_client_options`
:   (Optional) Configure additional options for the Kubernetes client. Supported options are `qps` and `burst`. If not set, the Kubernetes client’s default QPS and burst settings are used.

`cache_disable`
:   (Optional) Disables the cache for the secrets. When disabled, thus is set to `true`, code makes a request to the API Server to obtain the value. To continue using the cache, set the variable to `false`. Default is `false`.

`cache_refresh_interval`
:   (Optional) Defines the period to update all secret values kept in the cache. Defaults to `60s`.

`cache_ttl`
:   (Optional) Defines for how long a secret should be kept in the cache if not being requested. The default is `1h`.

`cache_request_timeout`
:   (Optional) Defines how long the API Server can take to provide the value for a given secret. Defaults to `5s`.

If you run agent on Kubernetes, the proper rule in the `ClusterRole` is required to provide access to the {{agent}} pod in the Secrets API:

```yaml
- apiGroups: [""]
  resources:
    - secrets
  verbs: ["get"]
```

::::{warning}
The above rule will give permission to {{agent}} pod to access Kubernetes Secrets API. Anyone who has access to the {{agent}} pod (`kubectl exec` for example) will also have access to the Kubernetes Secrets API. This allows access to a specific secret, regardless of the namespace that it belongs to. This option should be carefully considered.
::::
