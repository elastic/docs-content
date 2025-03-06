---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ciphers.html
---

# Enabling cipher suites for stronger encryption [ciphers]

The TLS and SSL protocols use a cipher suite that determines the strength of encryption used to protect the data. You may want to increase the strength of encryption used when using a Oracle JVM; the IcedTea OpenJDK ships without these restrictions in place. This step is not required to successfully use encrypted communication.

The *Java Cryptography Extension (JCE) Unlimited Strength Jurisdiction Policy Files* enable the use of additional cipher suites for Java in a separate JAR file that you need to add to your Java installation. You can download this JAR file from Oracle’s [download page](http://www.oracle.com/technetwork/java/javase/downloads/index.html). The *JCE Unlimited Strength Jurisdiction Policy Files`* are required for encryption with key lengths greater than 128 bits, such as 256-bit AES encryption.

After installation, all cipher suites in the JCE are available for use but requires configuration in order to use them. To enable the use of stronger cipher suites with {{es}} {{security-features}}, configure the [`cipher_suites` parameter](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ssl-tls-settings).

::::{note}
The *JCE Unlimited Strength Jurisdiction Policy Files* must be installed on all nodes in the cluster to establish an improved level of encryption strength.
::::


