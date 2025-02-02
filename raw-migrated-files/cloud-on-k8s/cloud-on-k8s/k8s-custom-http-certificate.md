# Custom HTTP certificate [k8s-custom-http-certificate]

You can provide your own CA and certificates instead of the self-signed certificate to connect to Elastic stack applications through HTTPS using a Kubernetes secret.

Check [Setup your own certificate](../../../deploy-manage/security/secure-http-communications.md#k8s-setting-up-your-own-certificate) to learn how to do that.

## Custom self-signed certificate using OpenSSL [k8s_custom_self_signed_certificate_using_openssl]

This example illustrates how to create your own self-signed certificate for the [quickstart Elasticsearch cluster](../../../deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md) using the OpenSSL command line utility. Note the subject alternative name (SAN) entry for `quickstart-es-http.default.svc`.

```sh
$ openssl req -x509 -sha256 -nodes -newkey rsa:4096 -days 365 -subj "/CN=quickstart-es-http" -addext "subjectAltName=DNS:quickstart-es-http.default.svc" -keyout tls.key -out tls.crt
$ kubectl create secret generic quickstart-es-cert --from-file=ca.crt=tls.crt --from-file=tls.crt=tls.crt --from-file=tls.key=tls.key
```


## Custom self-signed certificate using cert-manager [k8s_custom_self_signed_certificate_using_cert_manager]

This example illustrates how to issue a self-signed certificate for the [quickstart Elasticsearch cluster](../../../deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md) using a [cert-manager](https://cert-manager.io) self-signed issuer.

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

Here is how to issue multiple Elasticsearch certificates from a single self-signed CA. This is useful for example for [Remote clusters](../../../deploy-manage/remote-clusters/eck-remote-clusters.md) which need to trust each other’s CA, in order to avoid mounting N CAs when a cluster is connected to N other clusters.

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


