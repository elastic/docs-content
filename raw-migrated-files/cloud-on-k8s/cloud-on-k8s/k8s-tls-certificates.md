# TLS certificates [k8s-tls-certificates]

This section only covers TLS certificates for the HTTP layer. TLS certificates for the transport layer that are used for internal communications between Elasticsearch nodes are managed by ECK and cannot be changed. You can however set your own certificate authority for the [transport layer](../../../deploy-manage/deploy/cloud-on-k8s/transport-settings.md#k8s-transport-ca).

## Default self-signed certificate [k8s-default-self-signed-certificate]

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

### Reserve static IP and custom domain [k8s-static-ip-custom-domain]

To use a custom domain name with the self-signed certificate, you can reserve a static IP and/or use an Ingress instead of a `LoadBalancer` `Service`. Whatever you use, your DNS must be added to the certificate SAN in the `spec.http.tls.selfSignedCertificate.subjectAltNames` section of your Elastic resource manifest.

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



## Setup your own certificate [k8s-setting-up-your-own-certificate]

You can bring your own certificate to configure TLS to ensure that communication between HTTP clients and the Elastic Stack application is encrypted.

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

Alternatively you can also bring your own CA certificate including a private key and let ECK issue certificates with it. Any certificate SANs you have configured as decribed in [Reserve static IP and custom domain](../../../deploy-manage/security/secure-http-communications.md#k8s-static-ip-custom-domain) will also be respected when issuing certificates with this CA certificate.

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


## Disable TLS [k8s-disable-tls]

You can explicitly disable TLS for Kibana, APM Server, and the HTTP layer of Elasticsearch.

```yaml
spec:
  http:
    tls:
      selfSignedCertificate:
        disabled: true
```


