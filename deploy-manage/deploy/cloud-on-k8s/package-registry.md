---
navigation_title: Elastic Package Registry
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-package-registry.html
applies_to:
  deployment:
    eck: ga 3.3
products:
  - id: cloud-kubernetes
---

# Deploy {{package-registry}} on {{eck}} [k8s-package-registry]

```{applies_to}
deployment:
  eck: ga 3.3
```

Starting with ECK 3.3, you can deploy and manage the {{package-registry}} (EPR) as a {{k8s}} resource using ECK. The {{package-registry}} is a service that stores Elastic package definitions in a central location, making it easier to manage integrations in air-gapped environments or when you need to use a private registry.

## Overview

The {{package-registry}} provides a centralized repository for {{product.integrations}} packages. When deployed with ECK, it runs as a containerized service in your {{k8s}} cluster and can be used by {{kib}} instances to download and manage integration packages for {{fleet}}.

## Deploy the Package Registry

To deploy the {{package-registry}}, create a `PackageRegistry` resource:

```yaml
apiVersion: packageregistry.k8s.elastic.co/v1alpha1
kind: PackageRegistry
metadata:
  name: package-registry-sample
  namespace: default
spec:
  version: {{version.stack}}
  count: 1
```

The operator automatically creates the necessary {{k8s}} resources, including:

* A Deployment for the {{package-registry}} pods
* A Service to expose the {{package-registry}} within your cluster
* TLS certificates for secure communication

## Configure the Package Registry

### Basic configuration

The following example shows a basic {{package-registry}} deployment:

```yaml
apiVersion: package-registry.k8s.elastic.co/v1alpha1
kind: PackageRegistry
metadata:
  name: package-registry-sample
  namespace: default
spec:
  version: {{version.stack}}
  count: 1
```

## Connect {{kib}} to the Package Registry

After deploying the {{package-registry}}, configure your {{kib}} instance to use it by setting the `spec.packageRegistryRef` field:

```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
  namespace: default
spec:
  version: {{version.stack}}
  count: 1
  packageRegistryRef:
    name: package-registry-sample
```

Check the [recipes directory](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/config/recipes/packageregistry) for Package Registry in the ECK source repository for additional configuration examples.

## Troubleshooting

### Packages are not available

The {{package-registry}} distribution images contain a snapshot of packages. Ensure you're using the correct image version that is equal to or greater than your {{stack}} version. For the latest packages, use the `production` or `lite` distribution tags:

* `docker.elastic.co/package-registry/distribution:production` - All packages from the production registry
* `docker.elastic.co/package-registry/distribution:lite` - Subset of commonly used packages

## See also

* [Configure Fleet in ECK](configuration-fleet.md)
* [Running ECK in air-gapped environments](air-gapped-install.md)
* [Set the proxy URL of the Elastic Package Registry](/reference/fleet/epr-proxy-setting.md)
* [Host your own Package Registry](/reference/fleet/air-gapped.md#air-gapped-diy-epr)
