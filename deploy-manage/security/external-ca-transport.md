---
applies_to:
  deployment:
    self:
    eck:
products:
  - id: elasticsearch
navigation_title: External CA for TLS
---

# Using an external certificate authority to secure node-to-node connections

By default, {{es}} uses mutual transport layer security (mutual TLS or mTLS) to secure node-to-node transport connections. Mutual TLS means that data is encrypted in transit, ensuring confidentiality and integrity, and also that both nodes in a connection must present a valid certificate to the other node when establishing the connection. Each node requires that certificates be issued by a trusted certificate authority (CA), ensuring that only authorized nodes can connect. Configure trusted certificate authorities using settings in the [`xpack.security.transport.ssl.*`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#transport-tls-ssl-settings) namespace, such as `xpack.security.transport.ssl.certificate_authorities` and `xpack.security.transport.ssl.truststore.path`.

{{es}} comes with a built-in tool called [`elasticsearch-certutil`](/deploy-manage/security/set-up-basic-security.md), which you can use to create and manage a dedicated certificate authority for each of your clusters, and to issue TLS certificates from this certificate authority. If you prefer not to use `elasticsearch-certutil`, then you must obtain the certificates from another certificate authority using standard TLS tools. Any certificate authority that is not managed using `elasticsearch-certutil` is referred to as an "external certificate authority" or "external CA."

This page explains the requirements and best practices to ensure that certificates generated using an external CA work correctly and protect your cluster properly.

::::{note}
The TLS security model identifies each CA by its CA certificate. Different CA certificates are considered to be different CAs in this model. In contrast, if there is a team in your organization who is responsible for issuing TLS certificates, then you might consider this team to be a single entity known to you as "the certificate authority." This team manages many different CA certificates, and therefore many different CAs according to the TLS security model.

This documentation follows the TLS convention and considers distinct CA certificates to be distinct CAs, even if they are all managed by the same team.
::::

::::{warning}
Transport connections between {{es}} nodes are security-critical and you must protect them carefully. Malicious actors who can observe or interfere with unencrypted node-to-node transport traffic can read or modify cluster data. A malicious actor who can establish a transport connection might be able to invoke system-internal APIs, including APIs that read or modify cluster data.
::::

## Transport mTLS certificate requirements for external CAs

Certificates used for transport mTLS must either have no Extended Key Usage (EKU) extension, or must include both `clientAuth` and `serverAuth` values in the extension. Public certificate authorities typically include the `serverAuth` value, but not the `clientAuth` value, in their EKU extension, making them unsuitable for mTLS.

Obtain your transport certificates from a certificate authority that only issues certificates to {{es}} nodes permitted to connect to your cluster. Do not use a public certificate authority or an organization-wide private certificate authority, because these issue certificates to entities beyond your authorized cluster nodes. Use a dedicated certificate authority for each {{es}} cluster.

::::{note}
Mutual TLS considers all certificates issued by the same CA to be equally trusted, and therefore requires you to create a different CA for each trust domain. Each {{es}} cluster should be a separate trust domain.
::::

::::{warning}
Any holder of both a private key and a corresponding certificate issued by your cluster's transport CA will be permitted to open transport connections with your cluster. A malicious actor who obtains access to these things might be able to invoke system-internal APIs, including APIs that read or modify cluster data. To mitigate this risk, do not use a cluster's transport CA to issue transport certificates for other clusters, and do not use it to issue certificates for any other purpose.
::::

### Transport certificates vs. HTTP certificates

Transport certificates have different security requirements than [HTTP certificates](/deploy-manage/security/secure-cluster-communications.md#encrypt-http-communication). HTTP server certificates don't require the `clientAuth` value in their Extended Key Usage extension because they are used solely for server authentication, regardless of whether mTLS is enabled. HTTP connections typically don't use mTLS because HTTP has its own authentication mechanisms.

HTTP certificates can come from public or organization-wide certificate authorities, while transport certificates should use a dedicated, cluster-specific, private CA. Do not use the same certificate for both HTTP and transport connections.

## Turning off mTLS for transport connections [turn-off-mtls]

If your environment has some other way to prevent unauthorized node-to-node connections, you can disable mTLS by setting `xpack.security.transport.ssl.client_authentication: none`. You can still use non-mutual TLS to ensure the confidentiality and integrity of node-to-node traffic by setting `xpack.security.transport.ssl.enabled: true`. With non-mutual TLS, transport certificates don't require the `clientAuth` value in the Extended Key Usage extension.

::::{warning}
Turning off mTLS by setting `xpack.security.transport.ssl.client_authentication` to `optional` or `none` allows anyone with network access to establish transport connections. Malicious actors can use these connections to invoke system-internal APIs that might read or modify cluster data. Use mTLS to protect your node-to-node transport connections unless you are absolutely certain that unauthorized network access to these nodes cannot occur.
::::
