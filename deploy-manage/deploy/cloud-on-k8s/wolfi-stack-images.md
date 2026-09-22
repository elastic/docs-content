---
navigation_title: Wolfi stack images
applies_to:
  deployment:
    eck: ga 3.6
products:
  - id: cloud-kubernetes
---

# Use Wolfi images for stack components [k8s-wolfi-stack-images]

ECK supports Wolfi-based image variants for the stack components it manages. Elastic produces these images in partnership with [Chainguard](https://www.chainguard.dev/). They include only the application and its required runtime dependencies. This reduces the CVE footprint. For background, refer to [Reducing CVEs in Elastic container images](https://www.elastic.co/blog/reducing-cves-in-elastic-container-images).

::::{note}
The standard ECK operator image has been Wolfi-based since ECK 2.15. You do not need to configure the operator. This page explains how to enable Wolfi variants for the stack components the operator manages.
::::

## Supported versions [k8s-wolfi-supported-versions]

ECK supports Wolfi images for stack components from version 8.16.0.

::::{warning}
- Logstash Wolfi images in versions `8.16.0`–`8.16.3` and `8.17.0`–`8.17.1` do not include the `openssl` binary. ECK requires `openssl` to inject TLS certificates. Do not use those patch releases with Wolfi images and Logstash. Use `8.16.4+` or `8.17.2+` instead.

- Do not configure `spec.secureSettings` on an APM Server Wolfi image. The Wolfi APM Server image does not include a shell. ECK's keystore init container requires a shell to inject secure settings.
::::

## Enable Wolfi images [k8s-wolfi-enable]

Set the `container-suffix` configuration flag to `-wolfi`. For ECK configuration options, refer to [Configure ECK](./configure-eck.md).

::::{note}
The `container-suffix` flag cannot be combined with `--ubi-only`. If your `eck.yaml` ConfigMap contains a `ubi-only` key (including `ubi-only: false`), remove it before setting `container-suffix: -wolfi`. ECK checks whether the key exists, not its value, and rejects `container-suffix` when `ubi-only` is present.
::::

**Using a ConfigMap (YAML install)**

Edit the `elastic-operator` ConfigMap in the `elastic-system` namespace:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: elastic-operator
  namespace: elastic-system
data:
  eck.yaml: |-
    container-suffix: -wolfi
```

**Using Helm**

Set the value with `--set`:

```sh
helm upgrade elastic-operator elastic/eck-operator \
  -n elastic-system \
  --reuse-values \
  --set config.containerSuffix=-wolfi
```

Or in `values.yaml`:

```yaml
config:
  containerSuffix: "-wolfi"
```

Apply the configuration. Restart the ECK operator pod. Verify that pods pull Wolfi images. For example, {{es}} pods should use `docker.elastic.co/elasticsearch/elasticsearch-wolfi:<version>`. {{package-registry}} and Enterprise Search images are Wolfi-based by default. ECK does not append the `-wolfi` suffix for those components.
