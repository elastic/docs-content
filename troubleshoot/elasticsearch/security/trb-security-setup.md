---
navigation_title: Password setup failures
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/trb-security-setup.html
applies_to:
  stack:
  deployment:
    eck:
    ess:
    ece:
    self:
products:
  - id: elasticsearch
---

# Diagnose password setup connection failures [trb-security-setup]

The [elasticsearch-setup-passwords command](elasticsearch://reference/elasticsearch/command-line-tools/setup-passwords.md) sets passwords for the built-in users by sending user management API requests. If your cluster uses SSL/TLS for the HTTP (REST) interface, the command attempts to establish a connection with the HTTPS protocol. If the connection attempt fails, the command fails.

**Symptoms:**

1. {{es}} is running HTTPS, but the command fails to detect it and returns the following errors:

    ```shell
    Cannot connect to elasticsearch node.
    java.net.SocketException: Unexpected end of file from server
    ...
    ERROR: Failed to connect to elasticsearch at
    http://127.0.0.1:9200/_security/_authenticate?pretty.
    Is the URL correct and elasticsearch running?
    ```

2. SSL/TLS is configured, but trust cannot be established. The command returns the following errors:

    ```shell
    SSL connection to
    https://127.0.0.1:9200/_security/_authenticate?pretty
    failed: sun.security.validator.ValidatorException:
    PKIX path building failed:
    sun.security.provider.certpath.SunCertPathBuilderException:
    unable to find valid certification path to requested target
    Check the elasticsearch SSL settings under
    xpack.security.http.ssl.
    ...
    ERROR: Failed to establish SSL connection to elasticsearch at
    https://127.0.0.1:9200/_security/_authenticate?pretty.
    ```

3. The command fails because hostname verification fails, which results in the following errors:

    ```shell
    SSL connection to
    https://idp.localhost.test:9200/_security/_authenticate?pretty
    failed: java.security.cert.CertificateException:
    No subject alternative DNS name matching
    elasticsearch.example.com found.
    Check the elasticsearch SSL settings under
    xpack.security.http.ssl.
    ...
    ERROR: Failed to establish SSL connection to elasticsearch at
    <ELASTICSEARCH_HOST_URL>:9200/_security/_authenticate?pretty.
    ```


**Resolution:**

1. If your cluster uses TLS/SSL for the HTTP interface but the `elasticsearch-setup-passwords` command attempts to establish a non-secure connection, use the `--url` command option to explicitly specify an HTTPS URL. Alternatively, set the `xpack.security.http.ssl.enabled` setting to `true`.
2. If the command does not trust the {{es}} server, verify that you configured the `xpack.security.http.ssl.certificate_authorities` setting or the `xpack.security.http.ssl.truststore.path` setting.
3. If hostname verification fails, you can disable this verification by setting `xpack.security.http.ssl.verification_mode` to `certificate`.

For more information about these settings, see [Security settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md).

