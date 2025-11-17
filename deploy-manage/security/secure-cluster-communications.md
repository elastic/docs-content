---
navigation_title: Manage TLS encryption
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup.html
  - https://www.elastic.co/guide/en/kibana/current/elasticsearch-mutual-tls.html
applies_to:
  serverless:
  deployment:
    self:
    eck:
    ece:
    ess:
products:
  - id: elasticsearch
  - id: kibana
---

% Scope: landing page for manually handling TLS certificates, and for information about TLS in {{stack}} in general.
# TLS encryption for cluster communications

This page explains how to secure communications and set up TLS certificates in your {{stack}} deployments.

For {{ech}} deployments and {{serverless-full}} projects, communication security is [fully managed by Elastic](/deploy-manage/security.md#managed-security-in-elastic-cloud) with no configuration required, including TLS certificates.

For ECE, ECK, and self-managed deployments, some of this process can be automated, with opportunities for manual configuration depending on your requirements. This page provides specific configuration guidance to secure the various communication channels between components.

For a complete comparison of security feature availability and responsibility by deployment type, refer to [Security features by deployment type](/deploy-manage/security.md#comparison-table).

::::{admonition} Understanding transport contexts
The term *transport* can be confusing in {{es}} because it's used in two different contexts:
- **Transport Layer Security (TLS)** is an industry-standard protocol that secures network communication. It's the modern name for SSL, and the Elastic documentation uses the terms TLS and SSL interchangeably.
- In {{es}}, the **transport layer** refers to internal node-to-node communication, which occurs over port 9300. This communication uses the [transport interface](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md), which implements a binary protocol specific to {{es}}.

Keep this distinction in mind when configuring security settings.
::::


## Communication channels overview [communication-channels]

Both {{es}} and {{kib}}, the core components of the {{stack}}, expose service endpoints that must be secured. {{es}} handles traffic at two levels:
* The **transport layer** (defaults to port `9300`), used for internal communication between nodes in the cluster.
* The **HTTP layer** (defaults to port `9200`), used by external clients — including {{kib}} — to send requests using the REST API.

Additionally, {{kib}} functions as a web server, exposing its own **HTTP endpoint** (defaults to port `5601`) to users, and also acts as a client when sending requests to {{es}}.

To ensure secure operation, it’s important to understand the communication channels and their specific security requirements.

| **Channel** | **Description** | **TLS requirements** |
|-------------|-----------------|--------------------|
| [{{es}} transport layer](#encrypt-internode-communication) | Communication between {{es}} nodes within a cluster | Mutual TLS/SSL required for multi-node clusters |
| [{{es}} HTTP layer](#encrypt-http-communication) | Communication between external clients and {{es}} through the REST API | TLS/SSL optional (but recommended) |
| [{{kib}} HTTP layer](#encrypt-http-communication) | Communication between external browsers or REST clients and {{kib}} | TLS/SSL optional (but recommended) |

### Transport layer security [encrypt-internode-communication]

The transport layer is used for communication between {{es}} nodes in a cluster. It relies on mutual TLS for both encryption and authentication of nodes.

Securing this layer prevents unauthorized nodes from joining your cluster and protects internode data. While implementing username and password authentication at the HTTP layer is useful for securing external access, the security of communication between nodes requires TLS.

The way that transport layer security is managed depends on your deployment type:

:::::{tab-set}
:group: deployments

::::{tab-item} ECH and Serverless
:sync: ech
{{es}} transport security is fully managed by Elastic, and no configuration is required.
::::

::::{admonition}{tab-item} ECE
:sync: ece
{{es}} transport security is fully managed by {{ece}} platform, and no configuration is required.
::::

::::{tab-item} ECK
:sync: eck

:::{include} ./_snippets/eck-transport.md
:::

:::{include} ./_snippets/own-ca-warning.md
:::

::::

::::{tab-item} Self-managed
:sync: self
{{es}} transport security can be [automatically configured](self-auto-setup.md), or manually set up by following the steps in [](set-up-basic-security.md).

For additional TLS configuration options, refer to [](./self-tls.md).

:::{include} ./_snippets/own-ca-warning.md
:::

::::

:::::

### HTTP layer security [encrypt-http-communication]

The HTTP layer includes the service endpoints exposed by both {{es}} and {{kib}}, supporting communications such as REST API requests, browser access to {{kib}}, and {{kib}}’s own traffic to {{es}}. Securing these endpoints helps prevent unauthorized access and protects sensitive data in transit.

::::{important}
While HTTP TLS encryption is optional in self-managed environments, it is strongly recommended for both production and non-production deployments. Even in non-production environments, unsecured endpoints can expose sensitive data or introduce avoidable risks.
::::

The way that HTTP layer security is managed depends on your deployment type:

:::::{tab-set}
:group: deployments

::::{tab-item} ECH and Serverless
:sync: ech

HTTP TLS for {{es}} and {{kib}} is fully managed by Elastic. No configuration is required.
{{kib}} instances are automatically configured to connect securely to {{es}}, without requiring manual setup.
::::

::::{tab-item} ECE
:sync: ece

HTTP TLS for deployments is managed at the platform proxy level. Refer to these guides for ECE-specific security customizations:
* [Manage security certificates in ECE](./secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md)
* [Allow x509 Certificates Signed with SHA-1](./secure-your-elastic-cloud-enterprise-installation/allow-x509-certificates-signed-with-sha-1.md)
* [Configure TLS version](./secure-your-elastic-cloud-enterprise-installation/configure-tls-version.md)

{{kib}} instances are automatically configured to connect securely to {{es}}, without requiring manual setup.
::::

::::{tab-item} ECK
:sync: eck

:::{include} ./_snippets/eck-http.md
:::

::::

::::{tab-item} Self-managed
:sync: self

HTTP TLS certificates for {{es}} can be [automatically configured](self-auto-setup.md), or manually set up by following the steps in [Set up HTTP SSL](./set-up-basic-security-plus-https.md).

{{kib}} acts as both an HTTP client to {{es}} and a server for browser access. It performs operations on behalf of users, so it must be properly configured to trust the {{es}} certificates, and to present its own TLS certificate for secure browser connections. These configurations must be performed manually in self-managed deployments.

:::{note}
The automatic configuration does not enable TLS on the {{kib}} HTTP endpoint. To encrypt browser traffic to {{kib}}, follow the steps in [](./set-up-basic-security-plus-https.md#encrypt-kibana-browser).
:::

For environments with stricter security requirements, refer to [Mutual TLS authentication between {{kib}} and {{es}}](./kibana-es-mutual-tls.md).

For additional TLS configuration options, refer to [](./self-tls.md).
::::

:::::

## Certificates lifecycle [generate-certificates]

Managing certificates is critical for secure communications. Certificates have limited lifetimes and must be renewed before expiry to prevent service disruptions. Each deployment type provides different tools or responsibilities for managing certificates lifecycle.

::::{tab-set}
:group: deployments

:::{tab-item} ECH and Serverless
:sync: ech

Certificate lifecycle is fully managed by Elastic, including renewal and rotation.
:::

:::{tab-item} ECE
:sync: ece

In ECE, the platform automatically renews internal certificates. However, you must manually renew your custom proxy and Cloud UI certificates. For more details, refer to [Manage security certificates](secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md).
:::

:::{tab-item} ECK
:sync: eck

:::{include} ./_snippets/eck-lifecycle.md
:::

:::

:::{tab-item} Self-managed
:sync: self

You are responsible for certificate lifecycle management, including monitoring expiration dates, renewing certificates, and redeploying them as needed. If you used Elastic tools to generate your certificates, refer to [Update TLS certificates](./updating-certificates.md) for guidance on rotating or replacing them.
:::

::::
