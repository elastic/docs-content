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
apiVersion: package-registry.k8s.elastic.co/v1
kind: PackageRegistry
metadata:
  name: package-registry-sample
  namespace: default
spec:
  version: {{version.stack}}
  count: 1
```

### Customize the service

You can customize how the {{package-registry}} service is exposed by configuring the service specification:

```yaml
apiVersion: package-registry.k8s.elastic.co/v1
kind: PackageRegistry
metadata:
  name: package-registry-sample
  namespace: default
spec:
  version: {{version.stack}}
  count: 1
  http:
    service:
      spec:
        type: LoadBalancer
        ports:
        - port: 8080
          targetPort: 8080
    tls:
      selfSignedCertificate:
        disabled: false
```

### Configure resource limits

You can set resource requests and limits for the {{package-registry}} pods:

```yaml
apiVersion: package-registry.k8s.elastic.co/v1
kind: PackageRegistry
metadata:
  name: package-registry-sample
  namespace: default
spec:
  version: {{version.stack}}
  count: 1
  podTemplate:
    spec:
      containers:
      - name: package-registry
        resources:
          requests:
            memory: 512Mi
            cpu: 200m
          limits:
            memory: 1Gi
            cpu: 500m
  http:
    tls:
      selfSignedCertificate:
        disabled: false
```

### Use a custom container image

If you're running in an air-gapped environment or need to use a custom image, you can specify the container image:

```yaml
apiVersion: package-registry.k8s.elastic.co/v1
kind: PackageRegistry
metadata:
  name: package-registry-sample
  namespace: default
spec:
  version: {{version.stack}}
  image: my.registry/package-registry/distribution:{{version.stack}}
  count: 1
  http:
    tls:
      selfSignedCertificate:
        disabled: false
```

## Connect Kibana to the Package Registry

After deploying the {{package-registry}}, configure your {{kib}} instance to use it by setting the `xpack.fleet.registryUrl` configuration:

```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
  namespace: default
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRef:
    name: elasticsearch-sample
  config:
    xpack.fleet.registryUrl: "https://package-registry-sample-http.default.svc:8080"
```

The service URL follows the pattern: `<package-registry-name>-http.<namespace>.svc:<port>`

For example, if your {{package-registry}} is named `package-registry-sample` in the `default` namespace and uses port `8080`, the URL would be:

```
https://package-registry-sample-http.default.svc:8080
```

:::{note}
If you're using self-signed certificates (which is the default), you may need to configure {{kib}} to trust the certificate authority. Refer to [Configure TLS settings](/deploy-manage/security/k8s-https-settings.md) for more information.
:::

## Use the Package Registry in air-gapped environments

The {{package-registry}} is particularly useful in air-gapped environments where {{kib}} cannot access the public Elastic Package Registry at `https://epr.elastic.co`.

1. Deploy the {{package-registry}} using ECK as shown in the examples above.

2. Configure {{kib}} to use your local {{package-registry}} instance:

```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
  namespace: default
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRef:
    name: elasticsearch-sample
  config:
    xpack.fleet.registryUrl: "https://package-registry-sample-http.default.svc:8080"
```

3. Ensure the {{package-registry}} container image is available in your private registry. The image is available at `docker.elastic.co/package-registry/distribution:{{version.stack}}`.

For more information about running ECK in air-gapped environments, refer to [Running ECK in air-gapped environments](air-gapped-install.md).

## Monitor the Package Registry

You can check the status of your {{package-registry}} deployment using `kubectl`:

```sh
kubectl get packageregistry -n default
```

To view detailed information:

```sh
kubectl describe packageregistry package-registry-sample -n default
```

To check the {{package-registry}} pods:

```sh
kubectl get pods -l package-registry.k8s.elastic.co/name=package-registry-sample
```

## Troubleshooting

### Package Registry is not accessible

If {{kib}} cannot connect to the {{package-registry}}, verify:

1. The {{package-registry}} service is running:
   ```sh
   kubectl get svc -l package-registry.k8s.elastic.co/name=package-registry-sample
   ```

2. The service URL in {{kib}} configuration is correct and uses the correct namespace.

3. Network policies allow traffic between {{kib}} and the {{package-registry}} pods.

4. TLS certificates are properly configured if using HTTPS.

### Packages are not available

The {{package-registry}} distribution images contain a snapshot of packages. Ensure you're using the correct image version that matches your {{stack}} version. For the latest packages, use the `production` or `lite` distribution tags:

* `docker.elastic.co/package-registry/distribution:production` - All packages from the production registry
* `docker.elastic.co/package-registry/distribution:lite` - Subset of commonly used packages

## See also

* [Configure Fleet in ECK](configuration-fleet.md)
* [Running ECK in air-gapped environments](air-gapped-install.md)
* [Set the proxy URL of the Elastic Package Registry](/reference/fleet/epr-proxy-setting.md)
* [Host your own Package Registry](/reference/fleet/air-gapped.md#air-gapped-diy-epr)
