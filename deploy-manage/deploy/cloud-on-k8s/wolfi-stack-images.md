---
navigation_title: Wolfi stack images
applies_to:
  deployment:
    eck: ga 3.6
products:
  - id: cloud-kubernetes
description: Configure ECK to use Wolfi-based container images for Elastic Stack components for a smaller CVE footprint.
---

# Use Wolfi images for stack components on ECK

ECK supports Wolfi-based image variants for the {{stack}} components it manages. Elastic produces these images in partnership with [Chainguard](https://www.chainguard.dev/). They include only the application and its required runtime dependencies. This reduces the CVE footprint. For background, refer to [Reducing CVEs in Elastic container images](https://www.elastic.co/blog/reducing-cves-in-elastic-container-images).

::::{note}
The standard ECK operator image is Wolfi-based and does not require configuration. This page explains how to enable Wolfi variants for the stack components the operator manages.
::::

## Requirements and limitations [k8s-wolfi-requirements]

The following requirements and limitations apply to Wolfi images for stack components:

- Wolfi images are available for stack components running version 8.16.0 or later, with one restriction for {{ls}}:

  {{ls}} Wolfi images in versions `8.16.0`–`8.16.3` and `8.17.0`–`8.17.1` do not include the `openssl` binary that ECK requires to inject TLS certificates. Use `8.16.4+` or `8.17.2+` instead.

- The {{apm-server}} Wolfi image does not include a shell. Because ECK's keystore init container requires a shell, `spec.secureSettings` is not supported on {{apm-server}} resources that use Wolfi images.

## Enable Wolfi images [k8s-wolfi-enable]
To use Wolfi images, configure the ECK operator to append `-wolfi` to the container image names it resolves for stack components. For ECK configuration options, refer to [](./configure-eck.md).

::::{important}
The `container-suffix` flag cannot be combined with `--ubi-only`. If your `eck.yaml` ConfigMap contains a `ubi-only` key (including `ubi-only: false`), remove it before setting `container-suffix: -wolfi`. ECK checks whether the key exists, not its value, and rejects `container-suffix` when `ubi-only` is present.
::::

:::::{tab-set}

::::{tab-item} YAML manifests
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
::::

::::{tab-item} Helm chart
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
::::

:::::

After updating the configuration, restart the ECK operator pod. 

To verify that Wolfi images are in use, describe a stack component pod and check its image:

```sh
kubectl describe pod <pod-name> -n <namespace> | grep Image:
```

Image names should end in `-wolfi`. For example, `docker.elastic.co/elasticsearch/elasticsearch-wolfi:{{version.stack}}`.

{{package-registry}} and Enterprise Search images are Wolfi-based by default. ECK does not append the `-wolfi` suffix for those components.
