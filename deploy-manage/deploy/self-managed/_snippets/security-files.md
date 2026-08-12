When you install {{es}}, the following certificates and keys are generated in the {{es}} configuration directory. These files are used to connect a {{kib}} instance to your secured {{es}} cluster and to encrypt internode communication. The files are listed here for reference.

`http_ca.crt`
:   The CA certificate that is used to sign the certificates for the HTTP layer of this {{es}} cluster.

`http.p12`
:   Keystore that contains the key and certificate for the HTTP layer for this node.

`transport.p12`
:   Keystore that contains the transport certificate, private key, and cluster CA for this node.

`http.p12` and `transport.p12` are password-protected PKCS#12 keystores. {{es}} stores the passwords for these keystores as [secure settings](/deploy-manage/security/secure-settings.md). To retrieve the passwords so that you can inspect or change the keystore contents, use the [`bin/elasticsearch-keystore`](elasticsearch://reference/elasticsearch/command-line-tools/elasticsearch-keystore.md) tool.

Use the following command to retrieve the password for `http.p12`:

```sh
bin/elasticsearch-keystore show xpack.security.http.ssl.keystore.secure_password
```

Use the following command to retrieve the password for `transport.p12`:

```sh
bin/elasticsearch-keystore show xpack.security.transport.ssl.keystore.secure_password
```

Security auto-configuration sets `certs/transport.p12` as both the transport keystore and truststore on each node. Auto-generated transport certificates have a long validity period and are unlikely to expire under normal operation. To add nodes, use an [enrollment token](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md#_enroll_nodes_in_an_existing_cluster_5) rather than copying `transport.p12` between nodes. For manual transport TLS setup and certificate expiry behavior when the same PKCS#12 file is shared across all nodes, refer to [Set up transport TLS](/deploy-manage/security/set-up-basic-security.md).