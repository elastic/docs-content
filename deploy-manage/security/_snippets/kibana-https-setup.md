To secure browser access to {{kib}}, you need to generate a TLS certificate and private key for the server. {{kib}} uses these to encrypt HTTP traffic and establish trust with connecting browsers or API clients.

::::{important}
When creating or requesting a TLS certificate, make sure to include one or more valid **Subject Alternative Names (SANs)** that match how users will access {{kib}}, typically a fully qualified domain name (FQDN), hostname, or IP address. Most browsers will reject the certificate if none of the SANs match the address used to connect.
::::

The following steps guide you through creating a Certificate Signing Request (CSR) for {{kib}}. A CSR is used to obtain a TLS certificate from a Certificate Authority (CA). For production environments, use a trusted CA such as [Let’s Encrypt](https://letsencrypt.org/) or your organization’s internal CA to ensure browser trust.

1. Generate a CSR and private key for {{kib}}.

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
3. Submit the `kibana-server.csr` certificate signing request to your organization’s security team or certificate authority to obtain a signed certificate. The resulting certificate might be in different formats, such as a `.crt` file like `kibana-server.crt`.
4. Open `kibana.yml` and add the following lines to configure {{kib}} HTTPS endpoint to use the server certificate and unencrypted private key.

    ```yaml
    server.ssl.certificate: $KBN_PATH_CONF/kibana-server.crt
    server.ssl.key: $KBN_PATH_CONF/kibana-server.key
    ```

    ::::{note}
    `$KBN_PATH_CONF` contains the path for the {{kib}} configuration files. If you installed {{kib}} using archive distributions (`zip` or `tar.gz`), the path defaults to `$KBN_HOME/config`. If you used package distributions (Debian or RPM), the path defaults to `/etc/kibana`.
    ::::

5. Add the following line to `kibana.yml` to enable HTTPS for incoming connections.

    ```yaml
    server.ssl.enabled: true
    ```

6. Start {{kib}}.

    After making these changes, you must always access {{kib}} through HTTPS. For example, `https://<your_kibana_host>.com:5601`.
