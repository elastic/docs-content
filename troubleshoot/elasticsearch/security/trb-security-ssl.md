---
navigation_title: SSL/TLS exceptions
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/trb-security-ssl.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Common SSL/TLS exceptions [trb-security-ssl]

**Symptoms:**

* You might see some exceptions related to SSL/TLS in your logs. Some of the common exceptions are shown below with tips on how to resolve these issues.<br>

**Resolution:**

`WARN: received plaintext http traffic on a https channel, closing connection`
:   Indicates that there was an incoming plaintext http request. This typically occurs when an external applications attempts to make an unencrypted call to the REST interface. Make sure that all applications are using `https` when calling the REST interface with SSL enabled.


`org.elasticsearch.common.netty.handler.ssl.NotSslRecordException: not an SSL/TLS record:`
:   Indicates that there was incoming plaintext traffic on an SSL connection. This typically occurs when a node is not configured to use encrypted communication and tries to connect to nodes that are using encrypted communication. Verify that all nodes are using the same setting for `xpack.security.transport.ssl.enabled`.

For more information about this setting, see [Security settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md).


`java.io.StreamCorruptedException: invalid internal transport message format, got`
:   Indicates an issue with data received on the transport interface in an unknown format. This can happen when a node with encrypted communication enabled connects to a node that has encrypted communication disabled. Verify that all nodes are using the same setting for `xpack.security.transport.ssl.enabled`.

For more information about this setting, see [Security settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md).


`java.lang.IllegalArgumentException: empty text`
:   This exception is typically seen when a `https` request is made to a node that is not using `https`. If `https` is desired, ensure the following setting is in [`elasticsearch.yml`](/deploy-manage/stack-settings.md):

```yaml
xpack.security.http.ssl.enabled: true
```

For more information about this setting, see [Security settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md).


`ERROR: unsupported ciphers [...] were requested but cannot be used in this JVM`
:   This error occurs when a SSL/TLS cipher suite is specified that cannot supported by the JVM that {{es}} is running in. Security tries to use the specified cipher suites that are supported by this JVM. This error can occur when using the Security defaults as some distributions of OpenJDK do not enable the PKCS11 provider by default. In this case, we recommend consulting your JVM documentation for details on how to enable the PKCS11 provider.

Another common source of this error is requesting cipher suites that use encrypting with a key length greater than 128 bits when running on an Oracle JDK. In this case, you must install the [JCE Unlimited Strength Jurisdiction Policy Files](../../../deploy-manage/security/enabling-cipher-suites-for-stronger-encryption.md).


