You create a server certificate and private key for {{kib}}. {{kib}} uses this server certificate and corresponding private key when receiving connections from web browsers.

When you obtain a server certificate, you must set its subject alternative name (SAN) correctly to ensure that browsers will trust it. You can set one or more SANs to the {{kib}} server’s fully-qualified domain name (FQDN), hostname, or IP address. When choosing the SAN, pick whichever attribute you’ll use to connect to {{kib}} in your browser, which is likely the FQDN.

The following instructions create a Certificate Signing Request (CSR) for {{kib}}. A CSR contains information that a CA uses to generate and sign a security certificate. The certificate can be trusted (signed by a public, trusted CA) or untrusted (signed by an internal CA). A self-signed or internally-signed certificate is acceptable for development environments and building a proof of concept, but should not be used in a production environment.

::::{warning}
Before going to production, use a trusted CA such as [Let’s Encrypt](https://letsencrypt.org/) or your organization’s internal CA to sign the certificate. Using a signed certificate establishes browser trust for connections to {{kib}} for internal access or on the public internet.
::::


1. Generate a server certificate and private key for {{kib}}.

    ```shell
    ./bin/elasticsearch-certutil csr -name kibana-server -dns example.com,www.example.com
    ```

    The CSR has a common name (CN) of `kibana-server`, a SAN of `example.com`, and another SAN of `www.example.com`.

    This command generates a `csr-bundle.zip` file by default with the following contents:

    ```txt
    /kibana-server
    |_ kibana-server.csr
    |_ kibana-server.key
    ```

2. Unzip the `csr-bundle.zip` file to obtain the `kibana-server.csr` unsigned security certificate and the `kibana-server.key` unencrypted private key.
3. Send the `kibana-server.csr` certificate signing request to your internal CA or trusted CA for signing to obtain a signed certificate. The signed file can be in different formats, such as a `.crt` file like `kibana-server.crt`.
4. Open `kibana.yml` and add the following lines to configure {{kib}} to access the server certificate and unencrypted private key.

    ```yaml
    server.ssl.certificate: $KBN_PATH_CONF/kibana-server.crt
    server.ssl.key: $KBN_PATH_CONF/kibana-server.key
    ```

    ::::{note}
    `$KBN_PATH_CONF` contains the path for the {{kib}} configuration files. If you installed {{kib}} using archive distributions (`zip` or `tar.gz`), the path defaults to `$KBN_HOME/config`. If you used package distributions (Debian or RPM), the path defaults to `/etc/kibana`.
    ::::

5. Add the following line to `kibana.yml` to enable TLS for inbound connections.

    ```yaml
    server.ssl.enabled: true
    ```

6. Start {{kib}}.

::::{note}
After making these changes, you must always access {{kib}} via HTTPS. For example, `https://<your_kibana_host>.com`.
::::

