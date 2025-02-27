---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/secure-connections.html
---

# Configure SSL/TLS for self-managed Fleet Servers [secure-connections]

If you’re running a self-managed cluster, configure Transport Layer Security (TLS) to encrypt traffic between {{agent}}s, {{fleet-server}}, and other components in the {{stack}}.

For the install settings specific to mutual TLS, as opposed to one-way TLS, refer to [{{agent}} deployment models with mutual TLS](/reference/ingestion-tools/fleet/mutual-tls.md).

For a summary of flow by which TLS is established between components using either one-way or mutual TLS, refer to [One-way and mutual TLS certifications flow](/reference/ingestion-tools/fleet/tls-overview.md).

::::{tip}
[{{ecloud}}](https://www.elastic.co/cloud/elasticsearch-service?page=docs&placement=docs-body) provides secure, encrypted connections out of the box!
::::



## Prerequisites [prereqs]

Configure security and generate certificates for the {{stack}}. For more information about securing the {{stack}}, refer to [Configure security for the {{stack}}](/deploy-manage/deploy/self-managed/installing-elasticsearch.md).

::::{important}
{{agent}}s require a PEM-formatted CA certificate to send encrypted data to {{es}}. If you followed the steps in [Configure security for the {{stack}}](/deploy-manage/deploy/self-managed/installing-elasticsearch.md), your certificate will be in a p12 file. To convert it, use OpenSSL:

```shell
openssl pkcs12 -in path.p12 -out cert.crt -clcerts -nokeys
openssl pkcs12 -in path.p12 -out private.key -nocerts -nodes
```

Key passwords are not currently supported.

::::


::::{important}
When you run {{agent}} with the {{elastic-defend}} integration, the [TLS certificates](https://en.wikipedia.org/wiki/X.509) used to connect to {{fleet-server}} and {{es}} need to be generated using [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)). For a full list of available algorithms to use when configuring TLS or mTLS, see [Configure SSL/TLS for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md). These settings are available for both standalone and {{fleet}}-managed {{agent}}.
::::



## Generate a custom certificate and private key for {{fleet-server}} [generate-fleet-server-certs]

This section describes how to use the `certutil` tool provided by {{es}}, but you can use whatever process you typically use to generate PEM-formatted certificates.

1. Generate a certificate authority (CA). Skip this step if you want to use an existing CA.

    ```shell
    ./bin/elasticsearch-certutil ca --pem
    ```

    This command creates a zip file that contains the CA certificate and key you’ll use to sign the {{fleet-server}} certificate. Extract the zip file:

    :::{image} images/ca.png
    :alt: Screen capture of a folder called ca that contains two files: ca.crt and ca.key
    :::

    Store the files in a secure location.

2. Use the certificate authority to generate certificates for {{fleet-server}}. For example:

    ```shell
    ./bin/elasticsearch-certutil cert \
      --name fleet-server \
      --ca-cert /path/to/ca/ca.crt \
      --ca-key /path/to/ca/ca.key \
      --dns your.host.name.here \
      --ip 192.0.2.1 \
      --pem
    ```

    Where `dns` and `ip` specify the name and IP address of the {{fleet-server}}. Run this command for each {{fleet-server}} you plan to deploy.

    This command creates a zip file that includes a `.crt` and `.key` file. Extract the zip file:

    :::{image} images/fleet-server-certs.png
    :alt: Screen capture of a folder called fleet-server that contains two files: fleet-server.crt and fleet-server.key
    :::

    Store the files in a secure location. You’ll need these files later to encrypt traffic between {{agent}}s and {{fleet-server}}.



## Encrypt traffic between {{agent}}s, {{fleet-server}}, and {{es}} [_encrypt_traffic_between_agents_fleet_server_and_es]

{{fleet-server}} needs a CA certificate or the CA fingerprint to connect securely to {{es}}. It also needs to expose a {{fleet-server}} certificate so other {{agent}}s can connect to it securely.

For the steps in this section, imagine you have the following files:

|     |     |
| --- | --- |
| `ca.crt` | The CA certificate to use to connect to {{fleet-server}}. This is theCA used to [generate a certificate and key](#generate-fleet-server-certs)for {{fleet-server}}. |
| `fleet-server.crt` | The certificate you generated for {{fleet-server}}. |
| `fleet-server.key` | The private key you generated for {{fleet-server}}.<br>If the `fleet-server.key` file is encrypted with a passphrase, the passphrase will need to be specified through a file. |
| `elasticsearch-ca.crt` | The CA certificate to use to connect to {{es}}. This is the CA used to generatecerts for {{es}} (see [Prerequisites](#prereqs)).<br>Note that the CA certificate’s SHA-256 fingerprint (hash) may be used instead of the `elasticsearch-ca.crt` file for securing connections to {{es}}. |

To encrypt traffic between {{agent}}s, {{fleet-server}}, and {{es}}:

1. Configure {{fleet}} settings. These settings are applied to all {{fleet}}-managed {{agent}}s.
2. In {{kib}}, open the main menu, then click **Management > {{fleet}} > Settings**.

    1. Under **{{fleet-server}} hosts**, specify the URLs {{agent}}s will use to connect to {{fleet-server}}. For example, [https://192.0.2.1:8220](https://192.0.2.1:8220), where 192.0.2.1 is the host IP where you will install {{fleet-server}}.

        ::::{tip}
        For host settings, use the `https` protocol. DNS-based names are also allowed.
        ::::

    2. Under **Outputs**, search for the default output, then click the **Edit** icon in the **Action** column.
    3. In the **Hosts** field, specify the {{es}} URLs where {{agent}}s will send data. For example, [https://192.0.2.0:9200](https://192.0.2.0:9200).
    4. Specify either a CA certificate or CA fingerprint to connect securely {{es}}:


* If you have a valid HEX encoded SHA-256 CA trusted fingerprint from root CA, specify it in the **Elasticsearch CA trusted fingerprint** field. To learn more, refer to the [{{es}} security documentation](/deploy-manage/deploy/self-managed/installing-elasticsearch.md).
* Otherwise, under **Advanced YAML configuration**, set `ssl.certificate_authorities` and specify the CA certificate to use to connect to {{es}}. You can specify a list of file paths (if the files are available), or embed a certificate directly in the YAML configuration. If you specify file paths, the certificates must be available on the hosts running the {{agent}}s.

    File path example:

    ```yaml
    ssl.certificate_authorities: ["/path/to/your/elasticsearch-ca.crt"] <1>
    ```

    1. The path to the CA certificate on the {{agent}} host.


    Pasted certificate example:

    ```yaml
    ssl:
      certificate_authorities:
      - |
        -----BEGIN CERTIFICATE-----
        MIIDSjCCAjKgAwIBAgIVAKlphSqJclcni3P83gVsirxzuDuwMA0GCSqGSIb3DQEB
        CwUAMDQxMjAwBgNVBAMTKUVsYXN0aWMgQ2VydGlmaWNhdGUgVG9vbCBBdXRvZ2Vu
        ZXJhdGVkIENBMB4XDTIxMDYxNzAxMzIyOVoXDTI0MDYxNjAxMzIyOVowNDEyMDAG
        A1UEAxMpRWxhc3RpYyBDZXJ0aWZpY2F0ZSBUb29sIEF1dG9nZW5lcmF0ZWQgQ0Ew
        ggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDOFgtVri7Msy2iR33nLrVO
        /M/6IyF72kFXup1E67TzetI22avOxNlq+HZTpZoWGV1I4RgxiQeN12FLuxxhd9nm
        rxfZEqpuIjvo6fvU9ifC03WjXg1opgdEb6JqH93RHKw0PYimxhQfFcwrKxFseHUx
        DeUNQgHkMQhDZgIfNgr9H/1X6qSU4h4LemyobKY3HDKY6pGsuBzsF4iOCtIitE9p
        sagiWR21l1gW/lNaEW2ICKhJXbaqbE/pis45/yyPI4Q1Jd1VqZv744ejnZJnpAx9
        mYSE5RqssMeV6Wlmu1xWljOPeerOVIKUfHY38y8GZwk7TNYAMajratG2dj+v9eAV
        AgMBAAGjUzBRMB0GA1UdDgQWBBSCNCjkb66eVsIaa+AouwUsxU4b6zAfBgNVHSME
        GDAWgBSCNCjkb66eVsIaa+AouwUsxU4b6zAPBgNVHRMBAf8EBTADAQH/MA0GCSqG
        SIb3DQEBCwUAA4IBAQBVSbRObxPwYFk0nqF+THQDG/JfpAP/R6g+tagFIBkATLTu
        zeZ6oJggWNSfgcBviTpXc6i1AT3V3iqzq9KZ5rfm9ckeJmjBd9gAcyqaeF/YpWEb
        ZAtbxfgPLI3jK+Sn8S9fI/4djEUl6F/kARpq5ljYHt9BKlBDyL2sHymQcrDC3pTZ
        hEOM4cDbyKHgt/rjcNhPRn/q8g3dDhBdzjlNzaCNH/kmqWpot9AwmhhfPTcf1VRc
        gxdg0CTQvQvuceEvIYYYVGh/cIsIhV2AyiNBzV5jJw5ztQoVyWvdqn3B1YpMP8oK
        +nadUcactH4gbsX+oXRULNC7Cdd9bp2G7sQc+aZm
        -----END CERTIFICATE-----
    ```

    1. Install an {{agent}} as a {{fleet-server}} on the host and configure it to use TLS:

        1. If you don’t already have a {{fleet-server}} service token, click the **Agents** tab in {{fleet}} and follow the instructions to generate the service token now.

            ::::{tip}
            The in-product installation steps are incomplete. Before running the `install` command, add the settings shown in the next step.
            ::::

        2. From the directory where you extracted {{fleet-server}}, run the `install` command and specify the certificates to use.

            The following command installs {{agent}} as a service, enrolls it in the {{fleet-server}} policy, and starts the service.

            ::::{note}
            If you’re using DEB or RPM, or already have the {{agent}} installed, use the `enroll` command along with the following options, then start the service as described in [Start {{agent}}](/reference/ingestion-tools/fleet/start-stop-elastic-agent.md#start-elastic-agent-service).
            ::::


            ```shell
            sudo ./elastic-agent install \
               --url=https://192.0.2.1:8220 \
               --fleet-server-es=https://192.0.2.0:9200 \
               --fleet-server-service-token=AAEBAWVsYXm0aWMvZmxlZXQtc2XydmVyL3Rva2VuLTE2MjM4OTAztDU1OTQ6dllfVW1mYnFTVjJwTC2ZQ0EtVnVZQQ \
               --fleet-server-policy=fleet-server-policy \
               --fleet-server-es-ca=/path/to/elasticsearch-ca.crt \
               --certificate-authorities=/path/to/ca.crt \
               --fleet-server-cert=/path/to/fleet-server.crt \
               --fleet-server-cert-key=/path/to/fleet-server.key \
               --fleet-server-port=8220 \
               --elastic-agent-cert=/tmp/fleet-server.crt \
               --elastic-agent-cert-key=/tmp/fleet-server.key \
               --elastic-agent-cert-key-passphrase=/tmp/fleet-server/passphrase-file \
               --fleet-server-es-cert=/tmp/fleet-server.crt \
               --fleet-server-es-cert-key=/tmp/fleet-server.key \
               --fleet-server-client-auth=required
            ```

            Where:

            `url`
            :   {{fleet-server}} URL.

            `fleet-server-es`
            :   {{es}} URL

            `fleet-server-service-token`
            :   Service token to use to communicate with {{es}}.

            `fleet-server-policy`
            :   The specific policy that {{fleet-server}} will use.

            `fleet-server-es-ca`
            :   CA certificate that the current {{fleet-server}} uses to connect to {{es}}.

            `certificate-authorities`
            :   List of paths to PEM-encoded CA certificate files that should be trusted for the other {{agents}} to connect to this {fleet-server}

            `fleet-server-cert`
            :   The path for the PEM-encoded certificate (or certificate chain) which is associated with the fleet-server-cert-key to expose this {{fleet-server}} HTTPS endpoint to the other {agents}

            `fleet-server-cert-key`
            :   Private key to use to expose this {{fleet-server}} HTTPS endpoint to the other {agents}

            `elastic-agent-cert`
            :   The certificate to use as the client certificate for {{agent}}'s connections to {{fleet-server}}.

            `elastic-agent-cert-key`
            :   The path to the private key to use as for {{agent}}'s connections to {{fleet-server}}.

            `elastic-agent-cert-key`
            :   The path to the file that contains the passphrase for the mutual TLS private key that {{agent}} will use to connect to {{fleet-server}}. The file must only contain the characters of the passphrase, no newline or extra non-printing characters. This option is only used if the `elastic-agent-cert-key` is encrypted and requires a passphrase to use.

            `fleet-server-es-cert`
            :   The path to the client certificate that {{fleet-server}} will use when connecting to {{es}}.

            `fleet-server-es-cert-key`
            :   The path to the private key that {{fleet-server}} will use when connecting to {{es}}.

            `fleet-server-client-auth`
            :   One of `none`, `optional`, or `required`. Defaults to `none`. {{fleet-server}}'s client_authentication option for client mTLS connections. If `optional` or `required` is specified, client certificates are verified using CAs specified in the `--certificate-authorities` flag.

            Note that additionally an optional passphrase for the private key may be specified with:

            `fleet-server-cert-key-passphrase`
            :   Passphrase file used to decrypt {{fleet-server}}'s private key.

            What happens if you enroll {{fleet-server}} without specifying certificates?
            If the certificates are managed by your organization and installed at the system level, they will be used to encrypt traffic between {{agent}}s, {{fleet-server}}, and {{es}}.
            If system-level certificates don’t exist, {{fleet-server}} automatically generates self-signed certificates. Traffic between {{fleet-server}} and {{agent}}s over HTTPS is encrypted, but the certificate chain cannot be verified. Any {{agent}}s enrolling in {{fleet-server}} will need to pass the `--insecure` flag to acknowledge that the certificate chain is not verified.
            Allowing {{fleet-server}} to generate self-signed certificates is useful to get things running for development, but not recommended in a production environment.


    2. Install your {{agent}}s and enroll them in {{fleet}}.

        {{agent}}s connecting to a secured {{fleet-server}} need to pass in the CA certificate used by the {{fleet-server}}. The CA certificate used by {{es}} is already specified in the agent policy because it’s set under {{fleet}} settings in {{kib}}. You do not need to pass it on the command line.

        The following command installs {{agent}} as a service, enrolls it in the agent policy associated with the specified token, and starts the service.

        ```shell
        sudo elastic-agent install --url=https://192.0.2.1:8220 \
          --enrollment-token=<string> \
          --certificate-authorities=/path/to/ca.crt
        ```

        Where:

        `url`
        :   {{fleet-server}} URL to use to enroll the {{agent}} into {{fleet}}.

        `enrollment-token`
        :   The enrollment token for the policy that will be applied to the {{agent}}.

        `certificate-authorities`
        :   CA certificate to use to connect to {{fleet-server}}. This is the CA used to [generate a certificate and key](#generate-fleet-server-certs) for {{fleet-server}}.

        Don’t have an enrollment token? On the **Agents** tab in {{fleet}}, click **Add agent**. Under **Enroll and start the Elastic Agent**, follow the in-product installation steps, making sure that you add the `--certificate-authorities` option before you run the command.


