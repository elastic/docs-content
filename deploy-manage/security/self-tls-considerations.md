---
navigation_title: Considerations
applies_to:
  deployment:
    self:
    eck:
products:
  - id: elasticsearch
navigation_title: External CA considerations
---

# Considerations for using an external CA for transport layer security

By default, {{es}} uses mutual TLS (mTLS) to secure node-to-node transport connections. With mTLS, data is encrypted in transit and both nodes must present valid certificates when connecting. Each node requires that certificates be issued by a trusted certificate authority, ensuring that only authorized nodes can connect. Configure trusted certificate authorities using settings in the [`xpack.security.transport.ssl.*`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#transport-tls-ssl-settings) namespace, such as `xpack.security.transport.ssl.certificate_authorities` and `xpack.security.transport.ssl.truststore.path`. 

::::{warning}
Transport connections between {{es}} nodes are security-critical and you must protect them carefully. Malicious actors who can observe or interfere with node-to-node transport traffic can read or modify cluster data. A malicious actor who can establish a transport connection might be able to invoke system-internal APIs, including APIs that read or modify cluster data.
::::

## External CA mTLS transport certificate requirements

Obtain your transport certificates from a certificate authority that only issues certificates to {{es}} nodes permitted to connect to your cluster. Do not use a public certificate authority or an organization-wide private certificate authority, because these issue certificates to entities beyond your authorized cluster nodes. Use a dedicated private certificate authority for each {{es}} cluster.

Certificates used for mTLS must either have no Extended Key Usage extension, or include both `clientAuth` and `serverAuth` values in the extension. Public certificate authorities typically omit the `clientAuth` value in the Extended Key Usage extension, making them unsuitable for mTLS. 

### Transport certificates vs. HTTP certificates

Transport certificates have different security requirements than [HTTP certificates](/deploy-manage/security/secure-cluster-communications.md#encrypt-http-communication). HTTP connections don't typically use mTLS because HTTP has its own authentication mechanisms. Because of this, HTTP certificates usually don't need to include the `clientAuth` value in their Extended Key Usage extension. HTTP certificates can come from public or organization-wide certificate authorities, while transport certificates should use a cluster-specific private CA. In most cases, you should not use the same certificate for both HTTP and transport connections.

## Turning off mTLS for transport connections [turn-off-mtls]

If your environment has some other way to prevent unauthorized node-to-node connections, you can disable mTLS by setting `xpack.security.transport.ssl.client_authentication: none`. You can still use non-mutual TLS for encryption by setting `xpack.security.transport.ssl.enabled: true`. With non-mutual TLS, transport certificates don't require the `clientAuth` value in the Extended Key Usage extension.

::::{warning}
Turning off mTLS by setting `xpack.security.transport.ssl.client_authentication` to `optional` or `none` allows anyone with network access to establish transport connections. Malicious actors can use these connections to invoke system-internal APIs that may read or modify cluster data. Use mTLS to 
protect your node-to-node transport connections unless you are absolutely certain that unauthorized network access to these nodes cannot occur.
::::