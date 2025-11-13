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

::::{important}
Transport connections between {{es}} nodes are security-critical. Malicious actors who can observe, interfere with, or establish these connections may be able to read or modify cluster data through system-internal APIs.
::::

## How mutual TLS protects transport connections

By default, {{es}} uses mutual TLS (mTLS) for node-to-node transport connections. This ensures:

- **Encryption**: Data is encrypted in transit for confidentiality and integrity
- **Authentication**: Both nodes must present valid certificates when connecting
- **Authorization**: Certificates must be issued by a trusted certificate authority

Configure trusted certificate authorities using settings like `xpack.security.transport.ssl.certificate_authorities` or `xpack.security.transport.ssl.truststore.path`.

## Certificate authority requirements

::::{warning}
Anyone with a certificate from a trusted CA can establish transport connections to your cluster and potentially access or modify data.
::::

Use a dedicated private certificate authority for each {{es}} cluster. **Do not use**:

- Public certificate authorities
- Organization-wide private certificate authorities  
- CAs shared with other applications

These broader CAs issue certificates to entities beyond your authorized {{es}} nodes, creating security risks.

## Certificate requirements

Transport certificates must either:
- Have no Extended Key Usage (EKU) extension, or
- Include both `clientAuth` and `serverAuth` in the EKU extension

Public CAs typically omit `clientAuth`, making their certificates unsuitable for mTLS.

## HTTP versus transport certificates

**Do not use the same certificate for both HTTP and transport connections.** They have different security requirements:

- **Transport certificates** (`xpack.security.transport.ssl.*`): Require mTLS and must include `clientAuth` in the EKU extension
- **HTTP certificates** (`xpack.security.http.ssl.*`): Use HTTP authentication mechanisms and typically don't need `clientAuth`

HTTP certificates can often come from public or organization-wide CAs, while transport certificates should always use a cluster-specific private CA.

## Disabling mutual TLS

If your environment prevents unauthorized node-to-node connections through other means, you can disable mTLS:

```yaml
xpack.security.transport.ssl.client_authentication: none
```

You can still use non-mutual TLS for encryption:

```yaml
xpack.security.transport.ssl.enabled: true
```

::::{warning}
Disabling mTLS allows anyone with network access to establish transport connections. Only do this if you're absolutely certain unauthorized network access cannot occur.
::::