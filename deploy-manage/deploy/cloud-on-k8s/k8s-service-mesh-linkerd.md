---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-service-mesh-linkerd.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Linkerd [k8s-service-mesh-linkerd]

The following sections describe how to connect the operator and managed resources to the Linkerd service mesh. It is assumed that Linkerd is already installed and configured on your Kubernetes cluster. If you are new to Linkerd, refer to the [product documentation](https://linkerd.io) for more information and installation instructions.

::::{note}
These instructions have been tested with Linkerd 2.7.0.
::::


## Connect the operator to the Linkerd service mesh [k8s-service-mesh-linkerd-operator-connection]

In order to connect the operator to the service mesh, Linkerd sidecar must be injected into the ECK deployment. This can be done during installation as follows:

```sh subs=true
kubectl create -f https://download.elastic.co/downloads/eck/{{version.eck}}/crds.yaml
linkerd inject https://download.elastic.co/downloads/eck/{{version.eck}}/operator.yaml | kubectl apply -f -
```

Confirm that the operator is now meshed:

```sh
linkerd stat sts/elastic-operator -n elastic-system
```

If the installation was successful, the output of the above command should show `1/1` under the `MESHED` column.


## Connect {{stack}} applications to the Linkerd service mesh [k8s-service-mesh-linkerd-stack-connection]

The easiest way to connect applications to the service mesh is by adding the `linkerd.io/inject: enabled` annotation to the deployment namespace. For example, if you are planning to deploy {{stack}} applications to a namespace named `elastic-stack`, annotate it as follows to enable [automatic Linkerd sidecar injection](https://linkerd.io/2/features/proxy-injection/).

```sh
kubectl annotate namespace elastic-stack linkerd.io/inject=enabled
```

Any {{es}}, {{kib}}, or APM Server resources deployed to a namespace with the above annotation will automatically join the mesh.

Alternatively, if you only want specific resources to join the mesh, add the `linkerd.io/inject: enabled` annotation to the `podTemplate` (check [API documentation](cloud-on-k8s://reference/api-docs.md)) of the resource as follows:

```yaml
podTemplate:
  metadata:
    annotations:
      linkerd.io/inject: enabled
```

If automatic sidecar injection is enabled and [auto mounting of service account tokens](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/#use-the-default-service-account-to-access-the-api-server) is not disabled on your Kubernetes cluster, examples defined elsewhere in the ECK documentation will continue to work under Linkerd without requiring any modifications. However, as the default behavior of ECK is to enable TLS for {{es}}, {{kib}} and APM Server resources, you will not be able to view detailed traffic information from Linkerd dashboards and command-line utilities. The following sections illustrate the optional configuration necessary to enhance the integration of {{stack}} applications with Linkerd.

### {{es}} [k8s-service-mesh-linkerd-elasticsearch]

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elastic-linkerd
spec:
  version: {{version.stack}}
  http:
    tls: <1>
      selfSignedCertificate:
        disabled: true
  nodeSets:
  - name: default
    count: 3
    config:
      node.store.allow_mmap: false
    podTemplate:
      metadata:
        annotations:
          linkerd.io/inject: enabled <2>
      spec:
        automountServiceAccountToken: true <3>
```

1. Disable automatic TLS to allow Linkerd to gather more statistics about connections (optional).
2. Explicitly enable sidecar injection (optional if the namespace is already annotated).
3. Enable service account token mounting to provide service identity (only required to enable mTLS if service account auto-mounting is disabled).



### {{kib}} and APM Server [k8s-service-mesh-linkerd-kibana-apm]

The configuration is almost identical for {{kib}} and APM Server resources.

```yaml subs=true
apiVersion: ...
kind: ...
metadata:
  name: elastic-linkerd
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRef:
    name: elastic-linkerd
  http:
    tls: <1>
      selfSignedCertificate:
        disabled: true
  podTemplate:
    metadata:
      annotations:
        linkerd.io/inject: enabled <2>
    spec:
      automountServiceAccountToken: true <3>
```

1. Disable automatic TLS to allow Linkerd to gather more statistics about connections (optional).
2. Explicitly enable sidecar injection (optional if the namespace is already annotated).
3. Enable service account token mounting to provide service identity (only required to enable mTLS if service account auto-mounting is disabled).




