---
navigation_title: Hardened (Wolfi) images
description: Learn how ECK uses Wolfi-based hardened images to reduce CVE exposure, and how to configure Wolfi images for Elastic Stack components.
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
  - id: elasticsearch
  - id: kibana
  - id: elastic-agent
  - id: beats
  - id: apm
  - id: logstash
---

# Hardened (Wolfi) images in {{eck}} [k8s-hardened-images]

Elastic has partnered with [Chainguard](https://www.chainguard.dev/) to provide hardened container images based on [Wolfi](https://github.com/wolfi-dev/os), a minimal, security-focused Linux distribution designed for containerized environments. These images significantly reduce the CVE footprint of Elastic containers by including only the application and its necessary runtime dependencies. For background on this initiative, refer to the blog post [Reducing CVEs in Elastic container images](https://www.elastic.co/blog/reducing-cves-in-elastic-container-images).

::::{note}
Only images distributed via `docker.elastic.co` are officially supported by Elastic. Third-party hardened image sources, such as Docker Hardened Images (DHI) on Docker Hub, are not maintained by Elastic and fall outside the scope of Elastic support.
::::

## The ECK Operator image [k8s-hardened-images-operator]

Since ECK **v2.15.0**, the ECK Operator image is built on Wolfi by default. No additional configuration is required — pulling the standard operator image from `docker.elastic.co` already provides a hardened, Wolfi-based container.

## {{stack}} images managed by {{eck}} [k8s-hardened-images-stack]

Wolfi-based variants of the {{stack}} images ({{es}}, {{kib}}, {{agent}}, {{beats}}) are available from v8.16.0 onwards (v8.15.0 for {{apm-server}} and {{ls}}). However, ECK does not pull Wolfi variants by default for {{stack}} components — the standard images are used unless explicitly overridden.

To have the operator pull Wolfi-based images natively for the {{stack}} components it manages, set the `container-suffix` configuration flag to `-wolfi`. The operator then appends this suffix to the container images it resolves. This flag cannot be combined with the `--ubi-only` flag. For more details, refer to [ECK configuration flags](cloud-on-k8s://reference/eck-configuration-flags.md).

For example, set the suffix in the `elastic-operator` ConfigMap:

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

::::{warning}
The `container-suffix` flag applies to **all** resources managed by the operator, including [{{package-registry}}](package-registry.md) and [{{hosted-ems}}](elastic-maps-server.md). The images for these two components are **already natively based on Wolfi** and do not have a `-wolfi` suffix. With `container-suffix: -wolfi` set, the operator would try to pull non-existent suffixed images, causing the image pull to fail.

For these resources, explicitly set the container image in the manifest using `.spec.image` (without the suffix).

For [{{package-registry}}](package-registry.md), use:

```yaml subs=true
apiVersion: packageregistry.k8s.elastic.co/v1alpha1
kind: PackageRegistry
metadata:
  name: package-registry-sample
  namespace: default
spec:
  count: 1
  version: {{version.stack}}
  image: docker.elastic.co/package-registry/distribution:{{version.stack}}
```

Other valid tags include `lite-<version>`, `production` and `lite`. For more details, refer to [Air-gapped environments](/reference/fleet/air-gapped.md#air-gapped-diy-epr).

For [{{hosted-ems}}](elastic-maps-server.md), use:

```yaml subs=true
apiVersion: maps.k8s.elastic.co/v1alpha1
kind: ElasticMapsServer
metadata:
  name: quickstart
spec:
  count: 1
  version: {{version.stack}}
  image: docker.elastic.co/elastic-maps-service/elastic-maps-server:{{version.stack}}
```

::::

## Further reading [k8s-hardened-images-further-reading]

- [Reducing CVEs in Elastic container images](https://www.elastic.co/blog/reducing-cves-in-elastic-container-images)
