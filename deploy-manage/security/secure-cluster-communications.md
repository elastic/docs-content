---
navigation_title: Manage TLS encryption
applies_to:
  deployment:
    self:
    eck:
    ece:
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup.html
  - https://www.elastic.co/guide/en/kibana/current/elasticsearch-mutual-tls.html
---

% Scope: landing page for manually handling TLS certificates, and for information about TLS in Elastic Stack in general.
# TLS encryption for cluster communications

This page explains how to secure communications and setup TLS certificates between components in your {{stack}} deployment.

For {{ech}} and {{serverless-full}} deployments, communication security is fully managed by Elastic with no configuration required, including TLS certificates.

For ECE, ECK, and self-managed deployments, this page provides specific configuration guidance to secure the various communication channels between components.

:::{tip}
For a complete comparison of security feature availability and responsibility by deployment type, see [Security features by deployment type](/deploy-manage/security.md#comparison-table).
:::

## Communication channels overview

Both {{es}} and {{kib}}, the core components of the {{stack}}, expose service endpoints that must be secured. {{es}} handles traffic at two levels:
* The **transport layer**, used for internal communication between nodes in the cluster.
* The **HTTP layer**, used by external clients — including Kibana — to send requests via the REST API.

Additionally, {{kib}} functions as a web server, exposing its own **HTTP endpoint** to users, and also acts as a client when sending requests to {{es}}.

To ensure secure operation, it’s important to understand the communication channels and their specific security requirements.

| **Channel** | **Description** | **TLS requirements** |
|-------------|-----------------|--------------------|
| [{{es}} transport layer](#transport-layer-security) | Communication between {{es}} nodes within a cluster | Mutual TLS/SSL required for multi-node clusters |
| [{{es}} HTTP layer](#http-layer-security) | Communication between external clients and {{es}} through the REST API | TLS/SSL optional (but recommended) |
| [{{kib}} HTTP layer](#http-layer-security) | Communication between external browsers and {{kib}} through the REST API | TLS/SSL optional (but recommended) |

### Transport layer security

The transport layer is responsible for internal communication between {{es}} nodes in the cluster. Securing this layer prevents unauthorized nodes from joining your cluster and protects internode traffic.

The way that transport layer security is managed depends on your deployment type:

::::{tab-set}
:group: deployments

:::{tab-item} ECH and Serverless
:sync: ech
{{es}} transport security is fully managed by Elastic, and no configuration is required.
:::

:::{tab-item} ECE
:sync: ece
{{es}} transport security is fully managed by {{ece}} platform, and no configuration is required.
:::

:::{tab-item} ECK
:sync: eck
{{es}} transport security and TLS certificates are automatically configured by the operator, but you can still [customize its service and CA certificates](/deploy-manage/security/k8s-transport-settings.md).
:::

:::{tab-item} Self-managed
:sync: self
{{es}} transport security can be [automatically configured](security-certificates-keys.md), or manually set up by following the steps in [Set up basic security](set-up-basic-security.md).
:::

::::

### HTTP layer security

The HTTP layer includes the service endpoints exposed by both {{es}} and {{kib}}, supporting communications such as REST API requests, browser access to {{kib}}, and {{kib}}’s own traffic to {{es}}. Securing these endpoints helps prevent unauthorized access and protects sensitive data in transit.

::::{important}
While HTTP TLS encryption is optional in self-managed environments, it is strongly recommended for both production and non-production deployments. Even in non-production environments, unsecured endpoints can expose sensitive data or introduce avoidable risks.
::::

The way that HTTP layer security is managed depends on your deployment type:

::::{tab-set}
:group: deployments

:::{tab-item} ECH and Serverless
:sync: ech

HTTP TLS for {{es}} and {{kib}} is fully managed by Elastic. No configuration is required.
{{kib}} instances are automatically configured to connect securely to {{es}}, without requiring manual setup.
:::

:::{tab-item} ECE
:sync: ece

HTTP TLS for deployments is managed at the platform proxy level. Refer to these guides for ECE-specific security customizations:
* [Manage security certificates in ECE](./secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md)
* [Allow x509 Certificates Signed with SHA-1](./secure-your-elastic-cloud-enterprise-installation/allow-x509-certificates-signed-with-sha-1.md)
* [Configure TLS version](./secure-your-elastic-cloud-enterprise-installation/configure-tls-version.md)

{{kib}} instances are automatically configured to connect securely to {{es}}, without requiring manual setup.
:::

:::{tab-item} ECK
:sync: eck

HTTP TLS is automatically enabled for {{es}} and {{kib}} using self-signed certificates, with [several options available for customization](./k8s-https-settings.md), including custom certificates and domain names.

{{kib}} instances are automatically configured to connect securely to {{es}}, without requiring manual setup.
:::

:::{tab-item} Self-managed
:sync: self

HTTP TLS certificates for {{es}} can be [automatically configured](security-certificates-keys.md), or manually set up by following the steps in [Set up HTTP SSL](./set-up-basic-security-plus-https.md).

{{kib}} acts as both an HTTP client to {{es}} and a server for browser access. It performs operations on behalf of users, so it must be properly configured to trust the {{es}} certificates, and to present its own TLS certificate for secure browser connections. These configurations must be performed manually in self-managed deployments.

For environments with stricter security requirements, refer to [Mutual TLS authentication between {{kib}} and {{es}}](./kibana-es-mutual-tls.md).
:::

::::

## Maintaining and rotating TLS certificates [generate-certificates]

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

ECK provides flexible options for managing SSL certificates in your deployments, including automatic certificate generation and rotation, integration with external tools like `cert-manager`, or using your own custom certificates. Custom HTTP certificates require manual management.

TBD, add links to cert validity settings and cert configuration
:::

:::{tab-item} Self-managed
:sync: self

You are responsible for certificate lifecycle management, including monitoring expiration dates, renewing certificates, and redeploying them as needed. If you used Elastic tools to generate your certificates, refer to [Update TLS certificates](./updating-certificates.md) for guidance on rotating or replacing them.
:::

::::
