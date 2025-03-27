---
applies_to:
  deployment:
    eck:
    ece:
    self:
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup-https.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-tls-certificates.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-custom-http-certificate.html
  - https://www.elastic.co/guide/en/kibana/current/Security-production-considerations.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-kibana-http-configuration.html
---

% EEDUGON NOTE: security section might miss a section to secure the transport layer (not the HTTP).
% There we should integrate the content of https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-transport-settings.html which is currently in ECK (/deploy-manage) doc.

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

% pending to solve too

$$$configuring-tls-browser-kib$$$
$$$encrypt-http-communication$$$
$$$encrypt-kibana-http$$$

% Weird redirect in current system, not sure what to do

# Secure HTTP communications

## Overview

Securing HTTP communications is essential for protecting data transmitted between:

- {{kib}} and {{es}}
- {{kib}} and web browsers
- External monitoring systems and {{es}}
- Any HTTP client and your {{stack}} deployment

Different deployment types have different requirements:

| Deployment Type | HTTP Security Configuration |
|-----------------|----------------------------|
| {{ech}}/{{serverless-short}} | Automatically configured |
| Self-managed | Manual configuration required |
| {{eck}} | Configurable with defaults |
| {{ece}} | Manual configuration required |

## Self-managed deployments

```{applies_to}
self:
```

For self-managed deployments, you need to generate and configure certificates for secure HTTP communications.

### Prerequisites

Complete all steps in: 

- [Set up basic security](/deploy-manage/security/set-up-basic-security.md)
- [](/deploy-manage/security/set-up-basic-security-plus-https.md)

### Mutual TLS between {{kib}} and {{es}} [elasticsearch-mutual-tls]

Secure Sockets Layer (SSL) and Transport Layer Security (TLS) provide encryption for data-in-transit. While these terms are often used interchangeably, {{kib}} supports only TLS, which supersedes the old SSL protocols.

TLS requires X.509 certificates to authenticate the communicating parties and perform encryption of data-in-transit. Each certificate contains a public key and has and an associated — but separate — private key; these keys are used for cryptographic operations. {{kib}} supports certificates and private keys in PEM or PKCS#12 format.

In a standard TLS configuration, the server presents a signed certificate to authenticate itself to the client. In a mutual TLS configuration, the client also presents a signed certificate to authenticate itself to the server.

{{es}} {{security-features}} are enabled on your cluster by default, so each request that {{kib}} (the client) makes to {{es}} (the server) is authenticated. Most requests made by end users through {{kib}} to {{es}} are authenticated by using the credentials of the logged-in user.

To [enroll {{kib}} with an {{es}} cluster](/deploy-manage/security/security-certificates-keys.md#stack-start-with-security), you pass a generated enrollment token. This token configures {{kib}} to authenticate with {{es}} using a [service account token](/deploy-manage/users-roles/cluster-or-deployment-auth/service-accounts.md#service-accounts-tokens). {{kib}} also supports mutual TLS authentication with {{es}} via a [Public Key Infrastructure (PKI) realm](/deploy-manage/users-roles/cluster-or-deployment-auth/pki.md). With this setup, {{es}} needs to verify the signature on the {{kib}} client certificate, and it also needs to map the client certificate’s distinguished name (DN) to the appropriate `kibana_system` role.

::::{note}
Using a PKI realm is a [subscription feature](https://www.elastic.co/subscriptions).
::::

#### Configure {{kib}} and {{es}} to use mutual TLS authentication [_configure_kib_and_es_to_use_mutual_tls_authentication]

If you haven’t already, start {{kib}} and connect it to {{es}} using the [enrollment token](/deploy-manage/security/security-certificates-keys.md#stack-start-with-security).

1. Obtain a client certificate and private key for {{kib}}.

    {{kib}} uses the client certificate and corresponding private key when connecting to {{es}}.

    ::::{note}
    This is not the same as the server certificate that {{kib}} will present to web browsers.
    ::::


    You may choose to generate a client certificate and private key using the [`elasticsearch-certutil`](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md) tool. If you followed the {{es}} documentation for [generating the certificates authority](/deploy-manage/security/set-up-basic-security.md#generate-certificates), then you already have a certificate authority (CA) to sign the {{es}} server certificate. You may choose to use the same CA to sign the {{kib}} client certificate. For example:

    ```sh
    bin/elasticsearch-certutil cert -ca elastic-stack-ca.p12 -name kibana-client -dns <your_kibana_hostname>
    ```

    This will generate a client certificate and private key in a PKCS#12 file named `kibana-client.p12`. In this example, the client certificate has a Common Name (CN) of `"kibana-client"` and a subject alternative name (SAN) of `"<your_kibana_hostname>"`. The SAN may be required if you have hostname verification enabled on {{es}}.

2. Obtain the certificate authority (CA) certificate chain for {{kib}}.

    {{es}} needs the appropriate CA certificate chain to properly establish trust when receiving connections from {{kib}}.

    If you followed the instructions to generate a client certificate, then you will have a PKCS#12 file for {{kib}}. You can extract the CA certificate chain from this file. For example:

    ```sh
    openssl pkcs12 -in kibana-client.p12 -cacerts -nokeys -out kibana-ca.crt
    ```

    This will produce a PEM-formatted file named `kibana-ca.crt` that contains the CA certificate from the PKCS#12 file.

3. Configure {{es}} with a PKI realm and a native realm.

    By default, {{es}} provides a native realm for authenticating with a username and password. However, to support both a PKI realm (for {{kib}}) and a native realm (for end users), you must configure each realm in `elasticsearch.yml`:

    ```yaml
    xpack.security.authc.realms.pki.realm1.order: 1
    xpack.security.authc.realms.pki.realm1.certificate_authorities: "/path/to/kibana-ca.crt"
    xpack.security.authc.realms.native.realm2.order: 2
    ```

4. Configure {{es}} to request client certificates.

    By default, {{es}} will not request a client certificate when establishing a TLS connection. To change this, you must set up optional client certificate authentication in `elasticsearch.yml`:

    ```yaml
    xpack.security.http.ssl.client_authentication: "optional"
    ```

5. Restart {{es}}.
6. Use {{kib}} to create a role mapping in {{es}} for the client certificate.

    This role mapping will assign the `kibana_system` role to any user that matches the included mapping rule, which is set to equal the client certificate’s DN attribute:

    ![Role mapping for the {{kib}} client certificate](/deploy-manage/images/kibana-mutual-tls-role-mapping.png "")

    For more information, see [](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md).

7. Configure {{kib}} to use the client certificate and private key.

    You need to specify the information required to access your client certificate and corresponding private key.

    1. If your certificate and private key are contained in a PKCS#12 file:

        Specify your PKCS#12 file in `kibana.yml`:

        ```yaml
        elasticsearch.ssl.keystore.path: "/path/to/kibana-client.p12"
        ```

        If your PKCS#12 file is encrypted, add the decryption password to your [{{kib}} keystore](secure-settings.md):

        ```yaml
        bin/kibana-keystore add elasticsearch.ssl.keystore.password
        ```

        ::::{tip}
        If your PKCS#12 file isn’t protected with a password, depending on how it was generated, you may need to set `elasticsearch.ssl.keystore.password` to an empty string.
        ::::

    2. Otherwise, if your certificate and private key are in PEM format:

        Specify your certificate and private key in `kibana.yml`:

        ```yaml
        elasticsearch.ssl.certificate: "/path/to/kibana-client.crt"
        elasticsearch.ssl.key: "/path/to/kibana-client.key"
        ```

        If your private key is encrypted, add the decryption password to your [{{kib}} keystore](secure-settings.md):

        ```yaml
        bin/kibana-keystore add elasticsearch.ssl.keyPassphrase
        ```

8. Configure {{kib}} *not* to use a username and password for {{es}}.

    You must remove the `elasticsearch.username` and `elasticsearch.password` settings from `kibana.yml`. If these are present, {{kib}} will attempt to use them to authenticate to {{es}} via the native realm.

9. Restart {{kib}}.

These steps enable {{kib}} to authenticate to {{es}} using a certificate. However, end users will only be able to authenticate to {{kib}} with a username and password. To allow end users to authenticate to {{kib}} using a client certificate, see [{{kib}} PKI authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md#pki-authentication).


## Securing client applications

When connecting client applications to {{es}}, use these best practices:

- Always use HTTPS for all connections
- Validate server certificates to prevent man-in-the-middle attacks
- Use API keys or token-based authentication rather than basic auth where possible
- Implement appropriate connection pooling and retry mechanisms
- Consider mutual TLS for high-security environments

For code examples and library-specific guidance, see [HTTP/REST client security](httprest-clients-security.md).

## Securing Beats connections

% TODO: Put in clients section

When sending data from Beats to Elasticsearch, you need to secure those communications with TLS and proper authentication.

Key configuration requirements:
- Configure Beats to use HTTPS when connecting to Elasticsearch
- Set up appropriate authentication (API keys recommended)
- Verify Elasticsearch server certificates

For detailed instructions on configuring Beats security settings, see [Configure Beats security](/deploy-manage/security/set-up-basic-security-plus-https.md#configure-beats-security).

## {{ece}} (ECE)

```{applies_to}
deployment:
    ece: all
```

For ECE deployments, certificate management and TLS configuration are handled at the platform level. Refer to these guides for ECE-specific security configurations:

- [Manage security certificates in ECE](secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md)
- [Allow x509 Certificates Signed with SHA-1](secure-your-elastic-cloud-enterprise-installation/allow-x509-certificates-signed-with-sha-1.md)
- [Configure TLS version](secure-your-elastic-cloud-enterprise-installation/configure-tls-version.md)

## {{eck}} (ECK) [k8s-tls-certificates]

```{applies_to}
deployment:
    eck: all
```

:::{note}
This section only covers TLS certificates for the HTTP layer. TLS certificates for the transport layer that are used for internal communications between Elasticsearch nodes are managed by ECK and cannot be changed. You can however set your own certificate authority for the [transport layer](/deploy-manage/security/k8s-transport-settings.md#k8s-transport-ca).
:::

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

You can provide your own CA and certificates instead of the self-signed certificate to connect to Elastic stack applications through HTTPS using a Kubernetes secret.

Check [Setup your own certificate](/deploy-manage/security/secure-http-communications.md#k8s-setting-up-your-own-certificate) to learn how to do that.

#### Custom self-signed certificate using OpenSSL [k8s_custom_self_signed_certificate_using_openssl]

This example illustrates how to create your own self-signed certificate for the [quickstart Elasticsearch cluster](/deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md) using the OpenSSL command line utility. Note the subject alternative name (SAN) entry for `quickstart-es-http.default.svc`.

```sh
$ openssl req -x509 -sha256 -nodes -newkey rsa:4096 -days 365 -subj "/CN=quickstart-es-http" -addext "subjectAltName=DNS:quickstart-es-http.default.svc" -keyout tls.key -out tls.crt
$ kubectl create secret generic quickstart-es-cert --from-file=ca.crt=tls.crt --from-file=tls.crt=tls.crt --from-file=tls.key=tls.key
```

#### Custom self-signed certificate using cert-manager [k8s_custom_self_signed_certificate_using_cert_manager]

This example illustrates how to issue a self-signed certificate for the [quickstart Elasticsearch cluster](/deploy-manage/deploy/cloud-on-k8s/elasticsearch-deployment-quickstart.md) using a [cert-manager](https://cert-manager.io) self-signed issuer.

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

Here is how to issue multiple Elasticsearch certificates from a single self-signed CA. This is useful for example for [Remote clusters](/deploy-manage/remote-clusters/eck-remote-clusters.md) which need to trust each other’s CA, in order to avoid mounting N CAs when a cluster is connected to N other clusters.

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

### Setup your own certificate [k8s-setting-up-your-own-certificate]

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

Alternatively you can also bring your own CA certificate including a private key and let ECK issue certificates with it. Any certificate SANs you have configured as decribed in [Reserve static IP and custom domain](#k8s-static-ip-custom-domain) will also be respected when issuing certificates with this CA certificate.

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

### Disable TLS [k8s-disable-tls]

You can explicitly disable TLS for Kibana, APM Server, and the HTTP layer of Elasticsearch.

```yaml
spec:
  http:
    tls:
      selfSignedCertificate:
        disabled: true
```

### Kibana HTTP configuration in ECK [k8s-kibana-http-configuration]

#### Load balancer settings and TLS SANs [k8s-kibana-http-publish]

By default a `ClusterIP` [Service](https://kubernetes.io/docs/concepts/services-networking/service/) is created and associated with the {{kib}} deployment. If you want to expose {{kib}} externally with a [load balancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer), it is recommended to include a custom DNS name or IP in the self-generated certificate.

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


#### Provide your own certificate [k8s-kibana-http-custom-tls]

If you want to use your own certificate, the required configuration is identical to {{es}}. Refer to [Set up HTTPS for the Elastic Stack](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-http-communication).

#### Disable TLS [k8s-kibana-http-disable-tls]

You can disable the generation of the self-signed certificate and hence [disable TLS](/deploy-manage/security/secure-your-cluster-deployment.md). This is not recommended outside of testing clusters.

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
    tls:
      selfSignedCertificate:
        disabled: true
```