---
navigation_title: SSLHandshakeException
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/trb-security-sslhandshake.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Troubleshoot SSLHandshakeException and failed node connections [trb-security-sslhandshake]

**Symptoms:**

* A `SSLHandshakeException` causes a connection to a node to fail and indicates that there is a configuration issue. Some of the common exceptions are shown below with tips on how to resolve these issues.

**Resolution:**

`java.security.cert.CertificateException: No name matching node01.example.com found`
:   Indicates that a client connection was made to `node01.example.com` but the certificate returned did not contain the name `node01.example.com`. In most cases, the issue can be resolved by ensuring the name is specified during certificate creation. For more information, see [Encrypt internode communications with TLS](../../../deploy-manage/security/secure-cluster-communications.md#encrypt-internode-communication). Another scenario is when the environment does not wish to use DNS names in certificates at all. In this scenario, all settings in [`elasticsearch.yml`](/deploy-manage/stack-settings.md) should only use IP addresses including the `network.publish_host` setting.


`java.security.cert.CertificateException: No subject alternative names present`
:   Indicates that a client connection was made to an IP address but the returned certificate did not contain any `SubjectAlternativeName` entries. IP addresses are only used for hostname verification if they are specified as a `SubjectAlternativeName` during certificate creation. If the intent was to use IP addresses for hostname verification, then the certificate will need to be regenerated with the appropriate IP address. See [Encrypt internode communications with TLS](../../../deploy-manage/security/secure-cluster-communications.md#encrypt-internode-communication).


`javax.net.ssl.SSLHandshakeException: null cert chain` and `javax.net.ssl.SSLException: Received fatal alert: bad_certificate`
:   The `SSLHandshakeException` indicates that a self-signed certificate was returned by the client that is not trusted as it cannot be found in the `truststore` or `keystore`. This `SSLException` is seen on the client side of the connection.


`sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target` and `javax.net.ssl.SSLException: Received fatal alert: certificate_unknown`
:   This `SunCertPathBuilderException` indicates that a certificate was returned during the handshake that is not trusted. This message is seen on the client side of the connection. The `SSLException` is seen on the server side of the connection. The CA certificate that signed the returned certificate was not found in the `keystore` or `truststore` and needs to be added to trust this certificate.


`javax.net.ssl.SSLHandshakeException: Invalid ECDH ServerKeyExchange signature`
:   The `Invalid ECDH ServerKeyExchange signature` can indicate that a key and a corresponding certificate don’t match and are causing the handshake to fail. Verify the contents of each of the files you are using for your configured certificate authorities, certificates and keys. In particular, check that the key and certificate belong to the same key pair.


