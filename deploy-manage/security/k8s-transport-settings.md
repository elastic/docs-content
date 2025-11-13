---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-transport-settings.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Manage transport certificates on ECK [k8s-transport-settings]

The transport module in {{es}} is used for internal communication between nodes within the cluster as well as communication between remote clusters. Check the [{{es}} documentation](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md) for details. For customization options of the HTTP layer, check [Access services](../deploy/cloud-on-k8s/accessing-services.md) and [HTTP TLS certificates](./k8s-https-settings.md).

## Customize the Transport Service [k8s_customize_the_transport_service]

In the `spec.transport.service.` section, you can change the Kubernetes service used to expose the {{es}} transport module:

```yaml
spec:
  transport:
    service:
      metadata:
        labels:
          my-custom: label
      spec:
        type: LoadBalancer
```

Check the [Kubernetes Publishing Services (ServiceTypes)](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) that are currently available.

::::{note}
When you change the `clusterIP` setting of the service, ECK deletes and re-creates the service, as `clusterIP` is an immutable field. This will cause a short network disruption, but in most cases it should not affect existing connections as the transport module uses long-lived TCP connections.
::::


## Configure a custom Certificate Authority [k8s-transport-ca]

{{es}} uses X.509 certificates to establish encrypted and authenticated connections across nodes in the cluster. By default, ECK creates a self-signed CA certificate to issue a certificate [for each node in the cluster](/deploy-manage/security/set-up-basic-security.md#encrypt-internode-communication).

You can use a Kubernetes secret to provide your own CA instead of the self-signed certificate that ECK will then use to create node certificates for transport connections. The CA certificate must be stored in the secret under `ca.crt` and the private key must be stored under `ca.key`.

You need to reference the name of a secret that contains the TLS private key and the CA certificate, in the `spec.transport.tls.certificate` section, as shown in this example:

```yaml
spec:
  transport:
    tls:
      certificate:
        secretName: custom-ca
```


## Customize the node transport certificates [k8s_customize_the_node_transport_certificates]

The operator generates a self-signed TLS certificates for each node in the cluster. You can add extra IP addresses or DNS names to the generated certificates as follows:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: 8.16.1
  transport:
    tls:
      subjectAltNames:
      - ip: 1.2.3.4
      - dns: hulk.example.com
  nodeSets:
  - name: default
    count: 3
```


## Issue node transport certificates with third-party tools [k8s-transport-third-party-tools]

:::{warning}
Transport connections between {{es}} nodes are security-critical and you must protect them carefully. Malicious actors who can observe or interfere with node-to-node transport traffic can read or modify cluster data. A malicious actor who can establish a transport connection might be able to invoke system-internal APIs, including APIs that read or modify cluster data.

If you choose to issue node transport certificates using third-party tools, then carefully review [](/deploy-manage/security/self-tls-considerations.md) to ensure that the certificates that you provide meet the security requirements for transport connections.
:::

When following the instructions in [Configure a custom Certificate Authority](#k8s-transport-ca) the issuance of certificates is orchestrated by the ECK operator and the operator needs access to the CAs private key. If this is undesirable it is also possible to configure node transport certificates without involving the ECK operator. The following two pre-requisites apply:

1. The tooling used must be able to issue individual certificates for each {{es}} node and dynamically add or remove certificates as the cluster scales up and down.
2. The ECK operator must be configured to be aware of the CA in use for the [remote cluster](../remote-clusters/eck-remote-clusters.md#k8s-remote-clusters-connect-external) support to work.

The following example configuration using [cert-manager csi-driver](https://cert-manager.io/docs/projects/csi-driver/) and [trust-manager](https://cert-manager.io/docs/projects/trust-manager/) meets these two requirements:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: es
spec:
  version: 8.16.1
  transport:
    tls:
      certificateAuthorities:
        configMapName: trust <2>
      selfSignedCertificates:
        disabled: true <1>
  nodeSets:
  - name: default
    count: 3
    config:
      xpack.security.transport.ssl.key: /usr/share/elasticsearch/config/cert-manager-certs/tls.key
      xpack.security.transport.ssl.certificate: /usr/share/elasticsearch/config/cert-manager-certs/tls.crt
    podTemplate:
      spec:
        containers:
        - name: elasticsearch
          volumeMounts:
          - name: transport-certs
            mountPath: /usr/share/elasticsearch/config/cert-manager-certs
        volumes:
        - name: transport-certs
          csi:
            driver: csi.cert-manager.io
            readOnly: true
            volumeAttributes:
              csi.cert-manager.io/issuer-name: ca-cluster-issuer <2>
              csi.cert-manager.io/issuer-kind: ClusterIssuer
              csi.cert-manager.io/dns-names: "${POD_NAME}.${POD_NAMESPACE}.svc.cluster.local" <3>
```

1. Disables the self-signed certificates generated by ECK for the transport layer.
2. The example assumes that a `ClusterIssuer` by the name of `ca-cluster-issuer` exists and a PEM encoded version of the CA certificate is available in a ConfigMap (in the example named `trust`).  The CA certificate must be in a file called `ca.crt` inside the ConfigMap in the same namespace as the {{es}} resource.
3. If the remote cluster server is enabled, then the DNS names must also include both:* The DNS name for the related Kubernetes `Service`: `<cluster-name>-es-remote-cluster.${POD_NAMESPACE}.svc`
* The Pod DNS name: `${POD_NAME}.<cluster-name>-es-<nodeset-name>.${POD_NAMESPACE}.svc`

The following manifest is only provided to illustrate how these certificates can be configured in principle, using the trust-manager Bundle resource and cert-manager provisioned certificates:

```yaml
apiVersion: trust.cert-manager.io/v1alpha1
kind: Bundle
metadata:
  name: trust
spec:
  sources:
  - secret:
      name: "root-ca-secret"
      key: "tls.crt"
  target:
    configMap:
      key: "ca.crt"

apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {} <1>
---
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: ca-cluster-issuer
spec:
  ca:
    secretName: root-ca-secret
...
```

1. This example uses a self-signed issuer for the root CA and a second issuer for the {{es}} cluster transport certificates as the cert-manager CSI driver does not support self-signed CAs.


When transitioning from a configuration that uses externally provisioned certificates back to ECK-managed self-signed transport certificates it is important to ensure that the externally provisioned CA remains configured as a trusted CA through the `.spec.transport.tls.certificateAuthorities` attribute until all nodes in the cluster have been updated to use the ECK-managed certificates. When transitioning from ECK-managed certificates to externally provisioned ones, ECK ensures automatically that the ECK CA remains configured until the transition has been completed.


