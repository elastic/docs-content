---
navigation_title: Elastic Package Registry
applies_to:
  deployment:
    eck: ga 3.3
products:
  - id: cloud-kubernetes
---

# Deploy {{package-registry}} on {{eck}} [k8s-package-registry]

The {{package-registry}} is a service that stores Elastic package definitions in a central location, making it easier to manage integrations in air-gapped environments or when you need to use a private registry. You can deploy and manage the {{package-registry}} (EPR) as a {{k8s}} resource using ECK. When deployed with ECK, the registry runs as a containerized service in your {{k8s}} cluster and can be used by {{kib}} instances to download and manage integration packages for {{fleet}}.

## Deploy the Package Registry

To deploy the {{package-registry}}, create a `PackageRegistry` resource:

```yaml subs=true
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

## Connect {{kib}} to the Package Registry

After deploying the {{package-registry}}, configure your {{kib}} instance to use it by setting the `spec.packageRegistryRef` field:

```yaml subs=true
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

Refer to the [recipes directory](https://github.com/elastic/cloud-on-k8s/tree/{{version.eck | M.M}}/config/recipes/packageregistry) in the ECK source repository for additional configuration examples.

## Troubleshooting

### Packages are not available

Since the {{package-registry}} distribution images contain a snapshot of packages, if you are seeing issues where packages are not available, ensure you're using the correct image version that is equal to or greater than your {{stack}} version. For the latest packages, use the `production` or `lite` distribution tags, for example:

* `docker.elastic.co/package-registry/distribution:production` - All packages from the production registry
* `docker.elastic.co/package-registry/distribution:lite` - Subset of commonly used packages

```yaml subs=true
apiVersion: packageregistry.k8s.elastic.co/v1alpha1
kind: PackageRegistry
metadata:
  name: package-registry-sample
  namespace: default
spec:
  version: {{version.stack}}
  count: 1
  image: docker.elastic.co/package-registry/distribution:production-{{version.stack}}
```

## See also

* [](configuration-fleet.md)
* [](air-gapped-install.md)
* [](/reference/fleet/epr-proxy-setting.md)
* [](/reference/fleet/air-gapped.md#air-gapped-diy-epr)
