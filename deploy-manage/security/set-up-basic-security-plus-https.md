---
navigation_title: Set up HTTPS
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup-https.html
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
---

% Scope: HTTP certificates setup / manual configuration / multi or single node cluster
% original title: Set up basic security for the {{stack}} plus secured HTTPS traffic
# Set up HTTPS [security-basic-setup-https]

Enabling TLS on the HTTP layer, widely known as HTTPS, ensures that all client communications with your cluster are encrypted, adding a critical layer of security.

This document focuses on the **manual configuration** of HTTPS for {{es}} and {{kib}}. Use this approach if you want to provide your own TLS certificates, generate them with Elastic’s tools, or have full control over the configuration.

Note that HTTPS configuration for {{kib}} is always manual. Alternatively, {{es}} supports [automatic HTTPS setup](./self-auto-setup.md), which can simplify the process if full customization isn't required.

In this guide, you will learn how to:

* [Generate and configure TLS certificates for the HTTP endpoints of your {{es}} nodes](#encrypt-http-communication).
* [Configure {{kib}} to securely connect to {{es}} over HTTPS](#encrypt-kibana-elasticsearch) by trusting the Certificate Authority (CA) used by {{es}}.
* [Generate and configure TLS certificates for the {{kib}} HTTP interface to secure {{kib}} access](#encrypt-kibana-browser).

Refer to [HTTP TLS/SSL settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#http-tls-ssl-settings) for the complete list of available settings in {{es}}.

::::{note}
This guide uses the `elasticsearch-certutil` tool to generate Certificate Authorities (CAs) and TLS certificates. However, using this tool is not required. You can use publicly trusted certificates, your organization's internal certificate management system, or any other method that produces valid certificates.

If you already have certificates available, you can skip the certificate generation steps and proceed directly to the {{es}} and {{kib}} configuration steps.
::::

::::{tip}
When running `elasticsearch-certutil` in `http` mode, the tool prompts you to choose how to generate the TLS certificates. One key question is whether you want to generate a Certificate Signing Request (CSR).

* Answer `n` to skip the CSR and sign your certificates using a Certificate Authority (CA) [you previously created](./set-up-basic-security.md#generate-certificates). You’ll be prompted to provide the path to your CA, which the tool will use to generate a `.p12` certificate. The steps in this guide follow this workflow for {{es}} certificates.
* Answer `y` to generate a CSR that can be signed by your organization's internal CA or external certificate provider. This is common in environments where trust is managed centrally. The steps in this guide follow this workflow for {{kib}} certificate.

Both workflows are supported. Choose the one that best fits your infrastructure and trust model.
::::


## Prerequisites [basic-setup-https-prerequisites]

If security feature wasn't already enabled in your cluster, complete all steps in [](./set-up-minimal-security.md).

For multi-node clusters, ensure you have completed the [transport TLS setup](./set-up-basic-security.md). As part of that process, you will have created a Certificate Authority (CA) that this guide reuses to issue HTTP certificates. 

If you prefer to use a separate CA for HTTP, you can generate a new one using the same process. For example:

```bash
elasticsearch-certutil ca --out http-ca.p12
```

Then, use this CA to sign your HTTP certificates in the next section and for {{kib}} HTTP endpoint.

## Generate and configure TLS certificates for {{es}} nodes [encrypt-http-communication]
% Encrypt HTTP client communications for {{es}}

Once TLS is enabled, all client communications with the cluster will be encrypted. Clients must connect using `https` and be configured to trust the Certificate Authority (CA) that signed the {{es}} certificates.

1. On **every** node in your cluster, stop {{es}} and {{kib}} if they are running.
2. On any single node, from the directory where you installed {{es}}, run the {{es}} HTTP certificate tool to generate TLS certificates for your nodes.

    ```shell
    ./bin/elasticsearch-certutil http
    ```

    This command generates a `.zip` file that contains certificates and keys to use with {{es}} and {{kib}}. Each folder contains a `README.txt` explaining how to use these files.

    1. When asked if you want to generate a CSR, enter `n`.
    2. When asked if you want to use an existing CA, enter `y`.
    3. Enter the path to your CA. This is the absolute path to the `elastic-stack-ca.p12` file that you generated for your cluster.
    4. Enter the password for your CA.
    5. Enter an expiration value for your certificate. You can enter the validity period in years, months, or days. For example, enter `90D` for 90 days.
    6. When asked if you want to generate one certificate per node, enter `y`.

        Each certificate will have its own private key, and will be issued for a specific hostname or IP address.

    7. When prompted, enter the name of the first node in your cluster.
    8. Enter all hostnames used to connect to your first node. These hostnames will be added as DNS names in the Subject Alternative Name (SAN) field in your certificate.

        List every hostname and variant used to connect to your cluster over HTTPS.

    9. Enter the IP addresses that clients can use to connect to your node.
    10. Repeat these steps for each additional node in your cluster.

3. After generating a certificate for each of your nodes, enter a password for your private key when prompted.
4. Unzip the generated `elasticsearch-ssl-http.zip` file. This compressed file contains one directory for both {{es}} and {{kib}}.

    ```txt
    /elasticsearch
    |_ README.txt
    |_ http.p12
    |_ sample-elasticsearch.yml
    ```

    ```txt
    /kibana
    |_ README.txt
    |_ elasticsearch-ca.pem
    |_ sample-kibana.yml
    ```

5. On **every** node in your cluster, complete the following steps:

    1. Copy the relevant `http.p12` certificate to the `$ES_PATH_CONF` directory.
    2. Edit the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) file to enable HTTPS security and specify the location of the `http.p12` security certificate.

        ```yaml
        xpack.security.http.ssl.enabled: true
        xpack.security.http.ssl.keystore.path: http.p12
        ```

    3. Add the password for your private key to the [secure settings](/deploy-manage/security/secure-settings.md) in {{es}}.

        ```shell
        ./bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password
        ```

    4. Start {{es}}.



## Encrypt HTTP communications for {{kib}} [encrypt-kibana-http]

{{kib}} handles two separate types of HTTP traffic that should be encrypted:
* **Outgoing requests from {{kib}} to {{es}}**: {{kib}} acts as an HTTP client and must be configured to trust the TLS certificate used by {{es}}.
* **Incoming requests from browsers or API clients to {{kib}}**: {{kib}} acts as an HTTP server, and you should configure a TLS certificate for its public-facing endpoint to secure clients traffic.


### Encrypt traffic between {{kib}} and {{es}} [encrypt-kibana-elasticsearch]

:::{include} /deploy-manage/security/_snippets/kibana-client-https-setup.md
:::



### Encrypt traffic between your browser and {{kib}} [encrypt-kibana-browser]

:::{include} /deploy-manage/security/_snippets/kibana-https-setup.md
:::

## What’s next? [whats-next]

After having enabled HTTPS, you should configure any other client that interacts with {{es}} or {{kib}} to use HTTPS and trust the appropriate CA certificate. Refer to [Secure other {{stack}} components](/deploy-manage/security/secure-clients-integrations.md) and [Securing HTTP client applications](./httprest-clients-security.md) for more details.

For other tasks related with TLS encryption in self-managed deployments, refer to [](./self-tls.md).

For other security features, refer to [](./secure-your-cluster-deployment.md).
