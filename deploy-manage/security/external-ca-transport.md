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

By default, {{es}} uses mutual TLS (mTLS) to secure node-to-node transport connections. Mutual TLS means that data is encrypted in transit, ensuring confidentiality and integrity, and also that both nodes in a connection must present a valid certificate to the other node when establishing the connection. Each node requires that certificates be issued by a trusted certificate authority (CA), ensuring that only authorized nodes can connect. Configure trusted certificate authorities using settings in the [`xpack.security.transport.ssl.*`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#transport-tls-ssl-settings) namespace, such as `xpack.security.transport.ssl.certificate_authorities` and `xpack.security.transport.ssl.truststore.path`. 

{{es}} comes with a built-in tool called [`elasticsearch-certutil`](/deploy-manage/security/set-up-basic-security.md), which you can use to create and manage a dedicated certificate authority for each of your clusters, and to issue TLS certificates from this certificate authority. If you prefer not to use `elasticsearch-certutil`, then you must obtain the certificates from another certificate authority using standard TLS tools. Any certificate authority that is not managed using `elasticsearch-certutil` is referred to as an "external certificate authority" or "external CA". 

This page explains the requirements and best practices to ensure that certificates generated using an external CA work correctly and protect your cluster properly.

::::{warning}
Transport connections between {{es}} nodes are security-critical and you must protect them carefully. Malicious actors who can observe or interfere with unencrypted node-to-node transport traffic can read or modify cluster data. A malicious actor who can establish a transport connection might be able to invoke system-internal APIs, including APIs that read or modify cluster data.
::::

## Transport mTLS certificate requirements for external CAs

Obtain your transport certificates from a certificate authority that only issues certificates to {{es}} nodes permitted to connect to your cluster. Do not use a public certificate authority or an organization-wide private certificate authority, because these issue certificates to entities beyond your authorized cluster nodes. Use a dedicated private certificate authority for each {{es}} cluster.

Certificates used for transport mTLS must either have no Extended Key Usage extension, or include both `clientAuth` and `serverAuth` values in the extension. Public certificate authorities typically omit the `clientAuth` value in the Extended Key Usage extension, making them unsuitable for mTLS. 

### Transport certificates vs. HTTP certificates

Transport certificates have different security requirements than [HTTP certificates](/deploy-manage/security/secure-cluster-communications.md#encrypt-http-communication). HTTP server certificates don't require the `clientAuth` Extended Key Usage extension because they are used solely for server authentication, regardless of whether mTLS is enabled. In practice, HTTP connections don't typically use mTLS because HTTP has its own authentication mechanisms. 

HTTP certificates can come from public or organization-wide certificate authorities, while transport certificates should use a cluster-specific private CA. In most cases, you should not use the same CA or certificate for both HTTP and transport connections.

## Turning off mTLS for transport connections [turn-off-mtls]

If your environment has some other way to prevent unauthorized node-to-node connections, you can disable mTLS by setting `xpack.security.transport.ssl.client_authentication: none`. You can still use non-mutual TLS to ensure the confidentiality and integrity of node-to-node traffic by setting `xpack.security.transport.ssl.enabled: true`. With non-mutual TLS, transport certificates don't require the `clientAuth` value in the Extended Key Usage extension.

::::{warning}
Turning off mTLS by setting `xpack.security.transport.ssl.client_authentication` to `optional` or `none` allows anyone with network access to establish transport connections. Malicious actors can use these connections to invoke system-internal APIs that might read or modify cluster data. Use mTLS to 
protect your node-to-node transport connections unless you are absolutely certain that unauthorized network access to these nodes cannot occur.
::::