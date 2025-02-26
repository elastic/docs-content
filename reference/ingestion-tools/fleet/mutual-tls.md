---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/mutual-tls.html
---

# Elastic Agent deployment models with mutual TLS [mutual-tls]

Mutual Transport Layer Security (mTLS) provides a higher level of security and trust compared to one-way TLS, where only the server presents a certificate. It ensures that not only the server is who it claims to be, but the client is also authenticated. This is particularly valuable in scenarios where both parties need to establish trust and validate each other’s identities, such as in secure API communication, web services, or remote authentication.

For a summary of flow by which TLS is established between components using either one-way or mutual TLS, refer to [One-way and mutual TLS certifications flow](/reference/ingestion-tools/fleet/tls-overview.md).

* [Overview](#mutual-tls-overview)
* [On-premise deployments](#mutual-tls-on-premise)
* [{{fleet-server}} on {{ecloud}}](#mutual-tls-cloud)
* [{{fleet-server}} on {{ecloud}} using a proxy](#mutual-tls-cloud-proxy)
* [{{fleet-server}} on-premise and {{ech}}](#mutual-tls-on-premise-hosted-es)


## Overview [mutual-tls-overview]

With mutual TLS the following authentication and certification verification occurs:

* **Client Authentication**: The client presents its digital certificate to the server during the TLS handshake. This certificate is issued by a trusted Certificate Authority (CA) and contains the client’s public key.
* **Server Authentication**: The server also presents its digital certificate to the client, proving its identity and sharing its public key. The server’s certificate is also issued by a trusted CA.
* **Certificate Verification**: Both the client and server verify each other’s certificates by checking the digital signatures against the CAs' public key (note that the client and server need not use the same CA).

{{fleet}}-managed {{agent}} has two main connections to ensure correct operations:

* Connectivity to {{fleet-server}} (the control plane, to check in, download policies, and similar).
* Connectivity to an Output (the data plane, such as {{es}} or {{ls}}).

In order to bootstrap, {{agent}} initially must establish a secure connection to the {{fleet-server}}, which can reside on-premises or in {{ecloud}}. This connectivity verification process ensures the agent’s authenticity. Once verified, the agent receives the policy configuration. This policy download equips the agent with the knowledge of the other components it needs to engage with. For instance, it gains insights into the output destinations it should write data to.

When mTLS is required, the secure setup between {{agent}}, {{fleet}}, and {{fleet-server}} is configured through the following steps:

1. mTLS is enabled.
2. The initial mTLS connection between {{agent}} and {{fleet-server}} is configured when {{agent}} is enrolled, using the parameters passed through the `elastic-agent install` or `elastic-agent enroll` command.
3. Once enrollment has completed, {{agent}} downloads the initial {{agent}} policy from {{fleet-server}}.

    1. If the {{agent}} policy contains mTLS configuration settings, those settings will take precedence over those used during enrollment: This includes both the mTLS settings used for connectivity between {{agent}} and {{fleet-server}} (and the {{fleet}} application in {{kib}}, for {{fleet}}-managed {{agent}}), and the settings used between {{agent}} and it’s specified output.
    2. If the {{agent}} policy does not contain any TLS, mTLS, or proxy configuration settings, these settings will remain as they were specified when {{agent}} enrolled. Note that the initial TLS, mTLS, or proxy configuration settings can not be removed through the {{agent}} policy; they can only be updated.


::::{important}
When you run {{agent}} with the {{elastic-defend}} integration, the [TLS certificates](https://en.wikipedia.org/wiki/X.509) used to connect to {{fleet-server}} and {{es}} need to be generated using [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)). For a full list of available algorithms to use when configuring TLS or mTLS, see [Configure SSL/TLS for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-ssl-configuration.md). These settings are available for both standalone and {{fleet}}-managed {{agent}}.
::::



## On-premise deployments [mutual-tls-on-premise]

:::{image} images/mutual-tls-on-prem.png
:alt: Diagram of mutual TLS on premise deployment model
:::

Refer to the steps in [Configure SSL/TLS for self-managed {{fleet-server}}s](/reference/ingestion-tools/fleet/secure-connections.md). To configure mutual TLS, include the following additional parameters when you install {{agent}} and {{fleet-server}}.


### {{agent}} settings [_agent_settings]

During {{agent}} installation on premise use the following options:

|     |     |
| --- | --- |
| `--certificate-authorities` | List of CA certificates that are trusted when {{fleet-server}} connects to {{agent}} |
| `--elastic-agent-cert` | {{agent}} certificate to present to {{fleet-server}} during authentication |
| `--elastic-agent-cert-key` | {{agent}} certificate key to present to {{fleet-server}} |
| `--elastic-agent-cert-key-passphrase` | The path to the file that contains the passphrase for the mutual TLS private key that {{agent}} will use to connect to {{fleet-server}} |


### {{fleet-server}} settings [_fleet_server_settings]

During {{fleet-server}} installation on-premise {{fleet-server}} authenticates with {{es}} and {{agents}}. You can use the following CLI options to facilitate these secure connections:

|     |     |
| --- | --- |
| `--fleet-server-es-ca` | CA to use for the {{es}} connection |
| `--fleet-server-es-cert` | {{fleet-server}} certificate to present to {{es}} |
| `--fleet-server-es-cert-key` | {{fleet-server}} certificate key to present to {{es}} |
| `--certificate-authorities` | List of CA certificates that are trusted when {{agent}} connects to {{fleet-server}} and when {{fleet-server}} validates the {{agent}} identity. |
| `--fleet-server-cert` | {{fleet-server}} certificate to present to {{agents}} during authentication |
| `--fleet-server-cert-key` | {{fleet-server}}'s private certificate key used to decrypt the certificate |


### {{fleet}} settings: [_fleet_settings]

In {{kib}}, navigate to {{fleet}}, open the **Settings** tab, and choose the **Output** that you’d like to configure. In the **Advanced YAML configuration**, add the following settings:

|     |     |
| --- | --- |
| `ssl.certificate_authorities` | List of CA certificates that are trusted when {{fleet-server}} connects to {{agent}} |
| `ssl.certificate` | This certificate will be passed down to all the agents that have this output configured in their policy. This certificate is used by the agent when establishing mTLS to the output.<br>You may either apply the full certificate, in which case all the agents get the same certificate OR alternatively point to a local directory on the agent where the certificate resides, if the certificates are to be unique per agent. |
| `ssl.key` | This certificate key will be passed down to all the agents that have this output configured in their policy. The certificate key is used to decrypt the SSL certificate. |

::::{important}
Note the following when you specify these SSL settings:

* The certificate authority, certificate, and certificate key need to be specified as a path to a local file. You cannot specify a directory.
* You can define multiple CAs or paths to CAs.
* Only one certificate and certificate key can be defined.

::::


In the **Advanced YAML configuration** these settings should be added in the following format:

```shell
ssl.certificate_authorities:
  - /path/to/ca
ssl.certificate: /path/to/cert
ssl.key: /path/to/cert_key
```

OR

```shell
ssl.certificate_authorities:
  - /path/to/ca
ssl.certificate: /path/to/cert
ssl.key: /path/to/cert_key
```

:::{image} images/mutual-tls-onprem-advanced-yaml.png
:alt: Screen capture of output advanced yaml settings
:::


## {{fleet-server}} on {{ecloud}} [mutual-tls-cloud]

In this deployment model, all traffic ingress into {{ecloud}} has its TLS connection terminated at the {{ecloud}} boundary. Since this termination is not handled on a per-tenant basis, a client-specific certificate can NOT be used at this point.

:::{image} images/mutual-tls-cloud.png
:alt: Diagram of mutual TLS on cloud deployment model
:::

We currently don’t support mTLS in this deployment model. An alternate deployment model is shown below where you can deploy your own secure proxy where TLS connections are terminated.


## {{fleet-server}} on {{ecloud}} using a proxy [mutual-tls-cloud-proxy]

In this scenario, where you have access to the proxy, you can configure mTLS between the agent and your proxy.

:::{image} images/mutual-tls-cloud-proxy.png
:alt: Diagram of mutual TLS on cloud deployment model with a proxy
:::


### {{agent}} settings [_agent_settings_2]

During {{agent}} installation on premise use the following options:

|     |     |
| --- | --- |
| `--certificate-authorities` | List of CA certificates that are trusted when {{agent}} connects to {{fleet-server}} or to the proxy between {{agent}} and {{fleet-server}} |
| `--elastic-agent-cert` | {{agent}} certificate to present  during authentication to {{fleet-server}} or to the proxy between {{agent}} and {{fleet-server}} |
| `--elastic-agent-cert-key` | {{agent}}'s private certificate key used to decrypt the certificate |
| `--elastic-agent-cert-key-passphrase` | The path to the file that contains the passphrase for the mutual TLS private key that {{agent}} will use to connect to {{fleet-server}} |


## {{fleet-server}} on-premise and {{ech}} [mutual-tls-on-premise-hosted-es]

In some scenarios you may want to deploy {{fleet-server}} on your own premises. In this case, you’re able to provide your own certificates and certificate authority to enable mTLS between {{fleet-server}} and {{agent}}.

However, as with the [{{fleet-server}} on {{ecloud}}](#mutual-tls-cloud) use case, the data plane TLS connections terminate at the {{ecloud}} boundary. {{ecloud}} is not a multi-tenanted service and therefore can’t provide per-user certificates.

:::{image} images/mutual-tls-fs-onprem.png
:alt: Diagram of mutual TLS with Fleet Server on premise and {{ech}} deployment model
:::

Similar to the {{fleet-server}} on {{ecloud}} use case, a secure proxy can be placed in such an environment to terminate the TLS connections and satisfy the mTLS requirements.

:::{image} images/mutual-tls-fs-onprem-proxy.png
:alt: Diagram of mutual TLS with Fleet Server on premise and {{ech}} deployment model with a proxy
:::


### {{agent}} settings [_agent_settings_3]

During {{agent}} installation on premise use the following options, similar to [{{agent}} deployment on premises](#mutual-tls-on-premise):

|     |     |
| --- | --- |
| `--certificate-authorities` | List of CA certificates that are trusted for when {{agent}} connects to {{fleet-server}} |
| `--elastic-agent-cert` | {{agent}} certificate to present to {{fleet-server}} during authentication |
| `--elastic-agent-cert-key` | {{agent}}'s private certificate key used to decrypt the certificate |
| `--elastic-agent-cert-key-passphrase` | The path to the file that contains the passphrase for the mutual TLS private key that {{agent}} will use to connect to {{fleet-server}} |


### {{fleet-server}} settings [_fleet_server_settings_2]

During {{fleet-server}} installation on-premise use the following options so that {{fleet-server}} can authenticate itself to the agent and then also to the secure proxy server:

|     |     |
| --- | --- |
| `--fleet-server-es-ca` | CA to use for the {{es}} connection, via secure proxy. This CA is used to authenticate the TLS connection from a secure proxy |
| `--certificate-authorities` | List of CA certificates that are trusted when {{agent}} connects to {{fleet-server}} |
| `--fleet-server-cert` | {{fleet-server}} certificate to present to {{agents}} during authentication |
| `--fleet-server-cert-key` | {{fleet-server}}'s private certificate key used to decrypt the certificate |


### {{fleet}} settings [_fleet_settings_2]

This is the same as what’s described for [on premise deployments](#mutual-tls-on-premise). The main difference is that you need to use certificates that are accepted by the secure proxy, as the mTLS is set up between the agent and the secure proxy.
