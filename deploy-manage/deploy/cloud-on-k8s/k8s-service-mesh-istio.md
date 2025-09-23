---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-service-mesh-istio.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Istio [k8s-service-mesh-istio]

The instructions in this section describe how to connect the operator and managed resources to the Istio service mesh and assume that Istio is already installed and configured on your Kubernetes cluster. To know more about Istio and how to install it, check the [product documentation](https://istio.io).

These instructions have been tested with Istio 1.24.3. Older or newer versions of Istio might require additional configuration steps not documented here.

::::{warning}
Some {{stack}} features such as [{{kib}} alerting and actions](/explore-analyze/alerts-cases.md) rely on the {{es}} API keys feature which requires TLS to be enabled at the application level. If you want to use these features, you should not disable the self-signed certificate on the {{es}} resource and enable `PERMISSIVE` mode for the {{es}} service through a `DestinationRule` or `PeerAuthentication` resource. Strict mTLS mode is currently not compatible with {{stack}} features requiring TLS to be enabled for the {{es}} HTTP layer.
::::


::::{important}
If you use a Kubernetes distribution like Minikube, which does not have support for issuing third-party security tokens, you should explicitly set `automountServiceAccountToken` field to `true` in the Pod templates to allow Istio to fallback to default service account tokens. Refer to [Istio security best practices](https://istio.io/docs/ops/best-practices/security/#configure-third-party-service-account-tokens) for more information.
::::


## Connect the operator to the Istio service mesh [k8s-service-mesh-istio-operator-connection]

The operator itself must be connected to the service mesh to deploy and manage {{stack}} resources that you wish to connect to the service mesh. This is achieved by injecting an Istio sidecar to the ECK operator Pods. The following instructions assume that [automatic sidecar injection](https://istio.io/docs/setup/additional-setup/sidecar-injection/#automatic-sidecar-injection) is enabled on your cluster through a mutating admissions webhook. Refer to [Istio injection documentation](https://istio.io/docs/setup/additional-setup/sidecar-injection/#injection) if you prefer a different method of injection.

1. Create the `elastic-system` namespace and enable sidecar injection:

    ```sh
    kubectl create namespace elastic-system
    kubectl label namespace elastic-system istio-injection=enabled
    ```

2. Install ECK:

    ```sh subs=true
    kubectl create -f https://download.elastic.co/downloads/eck/{{version.eck}}/crds.yaml
    kubectl apply -f https://download.elastic.co/downloads/eck/{{version.eck}}/operator.yaml
    ```

3. Check the configuration and make sure the installation has been successful:

    ```sh
    kubectl get pod elastic-operator-0 -n elastic-system -o=jsonpath='{range .spec.containers[*]}{.name}{"\n"}'
    ```


If the output of the above command contains both `manager` and `istio-proxy`, ECK was successfully installed with the Istio sidecar injected.

To make the [validating webhook](configure-validating-webhook.md) work under Istio, you need to exclude the inbound port 9443 from being proxied. This can be done by editing the template definition of the `elastic-operator` StatefulSet to add the following annotations to the operator Pod:

```yaml
[...]
spec:
  template:
    metadata:
      annotations:
        traffic.sidecar.istio.io/excludeInboundPorts: "9443"
        traffic.sidecar.istio.io/includeInboundPorts: '*'
[...]
```

As the default `failurePolicy` of the webhook is `Ignore`, the operator continues to function even if the above annotations are not present. The downside is that you are still able to submit an invalid manifest using `kubectl` without receiving any immediate feedback.

ECK has a fallback validation mechanism that reports validation failures as events associated with the relevant resource ({{eck_resources_list}}) that must be manually discovered by running `kubectl describe`. For example, to find the validation errors in an {{es}} resource named `quickstart`, you can run `kubectl describe elasticsearch quickstart`.


## Connect {{stack}} applications to the Istio service mesh [k8s-service-mesh-istio-stack-connection]

This section assumes that you are deploying ECK custom resources to a namespace that has [automatic sidecar injection](https://istio.io/docs/setup/additional-setup/sidecar-injection/#automatic-sidecar-injection) enabled.

If you have configured Istio in [permissive mode](https://istio.io/docs/concepts/security/#permissive-mode), examples defined elsewhere in the ECK documentation will continue to work without requiring any modifications. However, if you have enabled strict mutual TLS authentication between services either through global (`MeshPolicy`) or namespace-level (`Policy`) configuration, the following modifications to the resource manifests are necessary for correct operation.

### {{es}} [k8s-service-mesh-istio-elasticsearch]

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elastic-istio
spec:
  version: {{version.stack}}
  http:
    tls: <1>
      selfSignedCertificate:
        disabled: true
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      metadata:
        annotations:
          traffic.sidecar.istio.io/includeInboundPorts: "*"
          traffic.sidecar.istio.io/excludeOutboundPorts: "9300" <2>
          traffic.sidecar.istio.io/excludeInboundPorts: "9300"
      spec:
        automountServiceAccountToken: true <3>
```

1. Disable the default self-signed certificate generated by the operator and allow TLS to be managed by Istio. Disabling the self-signed certificate might interfere with some features such as {{kib}} Alerting and Actions.
2. Exclude the transport port (port 9300) from being proxied. Currently ECK does not support switching off X-Pack security and TLS for the {{es}} transport port. If Istio is allowed to proxy the transport port, the traffic is encrypted twice and communication between {{es}} nodes is disrupted.
3. Optional. Only set `automountServiceAccountToken` to `true` if your Kubernetes cluster does not have support for issuing third-party security tokens.


If you do not have [automatic mutual TLS](https://istio.io/latest/docs/tasks/security/authentication/mtls-migration/) enabled, you may need to create a [Destination Rule](https://istio.io/docs/reference/config/networking/destination-rule/) to allow the operator to communicate with the {{es}} cluster. A communication issue between the operator and the managed {{es}} cluster can be detected by looking at the operator logs to check if there are any errors reported with the text `503 Service Unavailable`.

```sh
kubectl logs -f -n elastic-system -c manager statefulset.apps/elastic-operator
```

If the operator logs indicate a communications problem, create a `DestinationRule` to enable mutual TLS between the operator and the affected {{es}} cluster. For example, the following rule enables mutual TLS for a specific {{es}} cluster named `elastic-istio` deployed to the `default` namespace.

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: elastic-istio
spec:
  host: "elastic-istio-es-http.default.svc.cluster.local"
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
```

Refer to the [Istio documentation](https://istio.io/docs/tasks/security/authentication/mtls-migration/) for more information about other configuration options affecting authentication between services.

#### Using init containers with Istio CNI [k8s-service-mesh-istio-cni]

There are [known issues with init containers](https://istio.io/docs/setup/additional-setup/cni/#compatibility-with-application-init-containers) when Istio CNI is configured. If you use init containers to [install {{es}} plugins](init-containers-for-plugin-downloads.md) or perform other initialization tasks that require network access, they may fail due to outbound traffic being blocked by the CNI plugin. To work around this issue, explicitly allow the external ports used by the init containers.

To install plugins using an init container, use a manifest similar to the following:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elastic-istio
spec:
  version: {{version.stack}}
  http:
    tls:
      selfSignedCertificate:
        disabled: true
  nodeSets:
  - name: default
    count: 3
    podTemplate:
      metadata:
        annotations:
          traffic.sidecar.istio.io/includeInboundPorts: "*"
          traffic.sidecar.istio.io/excludeOutboundPorts: "9300,443" <1>
          traffic.sidecar.istio.io/excludeInboundPorts: "9300"
      spec:
        automountServiceAccountToken: true
        initContainers:
          - name: install-plugins
            command:
              - sh
              - -c
              - |
                bin/elasticsearch-plugin remove --purge analysis-icu
                bin/elasticsearch-plugin install --batch analysis-icu
```

1. Plugins are downloaded over the HTTPS port (443) and needs to be allowed when Istio CNI is installed.




### {{kib}} [k8s-service-mesh-istio-kibana]

```yaml subs=true
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: elastic-istio
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRef:
    name: elastic-istio
  http:
    tls: <1>
      selfSignedCertificate:
        disabled: true
  podTemplate:
    spec:
      automountServiceAccountToken: true <2>
```

1. Disable the default self-signed certificate generated by the operator and allow TLS to be managed by Istio.
2. Optional. Only set `automountServiceAccountToken` to `true` if your Kubernetes cluster does not have support for issuing third-party security tokens.



### APM Server [k8s-service-mesh-istio-apm]

```yaml subs=true
apiVersion: apm.k8s.elastic.co/v1
kind: ApmServer
metadata:
  name: elastic-istio
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRef:
    name: elastic-istio
  http:
    tls: <1>
      selfSignedCertificate:
        disabled: true
  podTemplate:
    metadata:
      annotations:
        sidecar.istio.io/rewriteAppHTTPProbers: "true" <2>
    spec:
      automountServiceAccountToken: true <3>
```

1. Disable the default self-signed certificate generated by the operator and allow TLS to be managed by Istio.
2. Automatically re-write the health checks to go through the proxy.
3. Optional. Only set `automountServiceAccountToken` to `true` if your Kubernetes cluster does not have support for issuing third-party security tokens.
