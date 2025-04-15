---
applies_to:
  deployment:
    eck:
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-tls-certificates.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-custom-http-certificate.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-kibana-http-configuration.html
---

# Manage HTTP certificates on ECK

ECK offers several options for securing the HTTP endpoints of {{es}} and {{kib}}. By default, the operator generates a dedicated CA per deployment, and issues individual certificates for each instance. Alternatively, you can supply your own certificates or integrate with external solutions like `cert-manager`.

:::{note}
This section only covers TLS certificates for the HTTP layer. TLS certificates for the transport layer that are used for internal communications between {{es}} nodes are managed by ECK and cannot be changed. You can however [set your own certificate authority for the transport layer](/deploy-manage/security/k8s-transport-settings.md#k8s-transport-ca).
:::

## {{es}} certificates [k8s-tls-certificates]

By default, the operator manages a self-signed certificate with a custom CA for each resource. The CA, the certificate and the private key are each stored in a separate `Secret`.

```sh
> kubectl get secret | grep es-http
hulk-es-http-ca-internal         Opaque                                2      28m
hulk-es-http-certs-internal      Opaque                                2      28m
hulk-es-http-certs-public        Opaque                                1      28m
```

The public certificate is stored in a secret named `<name>-[es|kb|apm|ent|agent]-http-certs-public`.

```sh
> kubectl get secret hulk-es-http-certs-public -o go-template='{{index .data "tls.crt" | base64decode }}'
-----BEGIN CERTIFICATE-----
MIIDQDCCAiigAwIBAgIQHC4O/RWX15a3/P3upsm3djANBgkqhkiG9w0BAQsFADA6
...
QLYL4zLEby3vRxq65+xofVBJAaM=
-----END CERTIFICATE-----
```

### Custom HTTP certificate [k8s-custom-http-certificate]

You can provide your own CA and certificates instead of the self-signed certificate to connect to {{stack}} applications through HTTPS using a Kubernetes secret.

Check [Setup your own certificate](./set-up-basic-security-plus-https.md#encrypt-http-communication) to learn how to do that with `elasticsearch-certutil` tool.

#### Custom self-signed certificate using OpenSSL [k8s_custom_self_signed_certificate_using_openssl]

This example illustrates how to create your own self-signed certificate for the [quickstart {{es}} cluster](/deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md) using the OpenSSL command line utility. Note the subject alternative name (SAN) entry for `quickstart-es-http.default.svc`.

```sh
$ openssl req -x509 -sha256 -nodes -newkey rsa:4096 -days 365 -subj "/CN=quickstart-es-http" -addext "subjectAltName=DNS:quickstart-es-http.default.svc" -keyout tls.key -out tls.crt
$ kubectl create secret generic quickstart-es-cert --from-file=ca.crt=tls.crt --from-file=tls.crt=tls.crt --from-file=tls.key=tls.key
```

#### Custom self-signed certificate using cert-manager [k8s_custom_self_signed_certificate_using_cert_manager]

This example illustrates how to issue a self-signed certificate for the [quickstart {{es}} cluster](/deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md) using a [cert-manager](https://cert-manager.io) self-signed issuer.

```yaml
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: quickstart-es-cert
spec:
  isCA: true
  dnsNames:
    - quickstart-es-http
    - quickstart-es-http.default.svc
    - quickstart-es-http.default.svc.cluster.local
  issuerRef:
    kind: Issuer
    name: selfsigned-issuer
  secretName: quickstart-es-cert
  subject:
    organizations:
      - quickstart
```

Here is how to issue multiple {{es}} certificates from a single self-signed CA. This is useful for example for [Remote clusters](/deploy-manage/remote-clusters/eck-remote-clusters.md) which need to trust each other’s CA, in order to avoid mounting N CAs when a cluster is connected to N other clusters.

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: selfsigned-issuer
spec:
  selfSigned: {}
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: selfsigned-ca
spec:
  isCA: true
  commonName: selfsigned-ca
  secretName: root-ca-secret
  privateKey:
    algorithm: ECDSA
    size: 256
  issuerRef:
    kind: ClusterIssuer
    name: selfsigned-issuer
---
apiVersion: cert-manager.io/v1
kind: Issuer
metadata:
  name: ca-issuer
spec:
  ca:
    secretName: root-ca-secret
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: quickstart-es-cert
spec:
  isCA: false
  dnsNames:
    - quickstart-es-http
    - quickstart-es-http.default.svc
    - quickstart-es-http.default.svc.cluster.local
  subject:
    organizations:
      - quickstart
  privateKey:
    algorithm: RSA
    encoding: PKCS1
    size: 2048
  issuerRef:
    kind: Issuer
    name: ca-issuer
  secretName: quickstart-es-cert
```

### Reserve static IP and custom domain [k8s-static-ip-custom-domain]

To use a custom domain with a self-signed certificate:

```yaml
spec:
  http:
    service:
      spec:
        type: LoadBalancer
    tls:
      selfSignedCertificate:
        subjectAltNames:
        - ip: 160.46.176.15
        - dns: hulk.example.com
```

### Provide your own certificate [k8s-setting-up-your-own-certificate]

You can bring your own certificate to configure TLS to ensure that communication between HTTP clients and the {{stack}} application is encrypted.

Create a Kubernetes secret with:

* `ca.crt`: CA certificate (optional if `tls.crt` was issued by a well-known CA).
* `tls.crt`: The certificate.
* `tls.key`: The private key to the first certificate in the certificate chain.

::::{warning}
If your `tls.crt` is signed by an intermediate CA you may need both the Root CA and the intermediate CA combined within the `ca.crt` file depending on whether the Root CA is globally trusted.
::::

```sh
kubectl create secret generic my-cert --from-file=ca.crt --from-file=tls.crt --from-file=tls.key
```

Alternatively you can also bring your own CA certificate including a private key and let ECK issue certificates with it. Any certificate SANs you have configured as described in [Reserve static IP and custom domain](#k8s-static-ip-custom-domain) will also be respected when issuing certificates with this CA certificate.

Create a Kubernetes secret with:

* `ca.crt`: CA certificate.
* `ca.key`: The private key to the CA certificate.

```sh
kubectl create secret generic my-cert --from-file=ca.crt --from-file=ca.key
```

In both cases, you have to reference the secret name in the `http.tls.certificate` section of the resource manifest.

```yaml
spec:
  http:
    tls:
      certificate:
        secretName: my-cert
```

## {{kib}} HTTP configuration in ECK [k8s-kibana-http-configuration]

By default, ECK creates a `ClusterIP` [Service](https://kubernetes.io/docs/concepts/services-networking/service/) and associates it with the {{kib}} deployment.

If you need to expose {{kib}} externally or customize the service settings, ECK provides flexible options, including support for load balancers, custom DNS/IP SANs, and user-provided certificates.

### Load balancer settings and TLS SANs [k8s-kibana-http-publish]

If you want to expose {{kib}} externally with a [load balancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer), it is recommended to include a custom DNS name or IP in the self-generated certificate.

```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
spec:
  version: 8.16.1
  count: 1
  elasticsearchRef:
    name: "elasticsearch-sample"
  http:
    service:
      spec:
        type: LoadBalancer # default is ClusterIP
    tls:
      selfSignedCertificate:
        subjectAltNames:
        - ip: 1.2.3.4
        - dns: kibana.example.com
```


### Provide your own certificate [k8s-kibana-http-custom-tls]

If you want to use your own certificate, the required configuration is identical to {{es}}. Refer to [setup your own {{es}} certificate](#k8s-setting-up-your-own-certificate) for more information.

## Disable TLS [k8s-disable-tls]

You can explicitly disable the generation of the self-signed certificate and hence disable TLS for {{kib}}, APM Server, and the HTTP layer of {{es}}.

::::{important}
Disabling TLS is not recommended outside of test or development environments.
::::

To disable TLS, add the following setting to the appropriate resource:

```yaml
spec:
  http:
    tls:
      selfSignedCertificate:
        disabled: true
```
