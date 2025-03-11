---
applies_to:
  deployment: all
  serverless: ga
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-files.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/secure-cluster.html
  - https://www.elastic.co/guide/en/kibana/current/xpack-security.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-securing-stack.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-securing-ece.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-security.html
  - https://www.elastic.co/guide/en/kibana/current/using-kibana-with-security.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-limitations.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/es-security-principles.html
  - https://www.elastic.co/guide/en/cloud/current/ec-faq-technical.html
---

% SR: include this info somewhere in this section
% {{ech}} doesn't support custom SSL certificates, which means that a custom CNAME for an {{ech}} endpoint such as *mycluster.mycompanyname.com* also is not supported.
%
% In {{ech}}, IP sniffing is not supported by design and will not return the expected results. We prevent IP sniffing from returning the expected results to improve the security of our underlying {{ech}} infrastructure.
%
% encryption at rest (EAR) is enabled in {{ech}} by default. We support EAR for both the data stored in your clusters and the snapshots we take for backup, on all cloud platforms and across all regions.
% You can also bring your own key (BYOK) to encrypt your Elastic Cloud deployment data and snapshots. For more information, check [Encrypt your deployment with a customer-managed encryption key](../../../deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md).

% Note that the encryption happens at the file system level.

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/346

% Scope notes: this is just communication security - link to users + roles, spaces, monitoring, ++

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/security-files.md
%      Notes: redirect only
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/secure-cluster.md
% - [ ] ./raw-migrated-files/kibana/kibana/xpack-security.md
% - [ ] ./raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-securing-stack.md
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-securing-ece.md
% - [ ] ./raw-migrated-files/cloud/cloud-heroku/ech-security.md
% - [ ] ./raw-migrated-files/kibana/kibana/using-kibana-with-security.md
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/security-limitations.md
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/es-security-principles.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-faq-technical.md

$$$field-document-limitations$$$

$$$alias-limitations$$$

$$$preventing-unauthorized-access$$$

$$$preserving-data-integrity$$$

$$$maintaining-audit-trail$$$

:::{warning}
**This page is a work in progress.** 
:::


% The documentation team is working to combine content pulled from the following pages:

% * [/raw-migrated-files/elasticsearch/elasticsearch-reference/security-files.md](/raw-migrated-files/elasticsearch/elasticsearch-reference/security-files.md)
% * [/raw-migrated-files/elasticsearch/elasticsearch-reference/secure-cluster.md](/raw-migrated-files/elasticsearch/elasticsearch-reference/secure-cluster.md)
% * [/raw-migrated-files/kibana/kibana/xpack-security.md](/raw-migrated-files/kibana/kibana/xpack-security.md)
% * [/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-securing-stack.md](/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-securing-stack.md)
% * [/raw-migrated-files/cloud/cloud-enterprise/ece-securing-ece.md](/raw-migrated-files/cloud/cloud-enterprise/ece-securing-ece.md)
% * [/raw-migrated-files/cloud/cloud-heroku/ech-security.md](/raw-migrated-files/cloud/cloud-heroku/ech-security.md)
% * [/raw-migrated-files/kibana/kibana/using-kibana-with-security.md](/raw-migrated-files/kibana/kibana/using-kibana-with-security.md)
% * [/raw-migrated-files/elasticsearch/elasticsearch-reference/security-limitations.md](/raw-migrated-files/elasticsearch/elasticsearch-reference/security-limitations.md)
% * [/raw-migrated-files/elasticsearch/elasticsearch-reference/es-security-principles.md](/raw-migrated-files/elasticsearch/elasticsearch-reference/es-security-principles.md)
% * [/raw-migrated-files/cloud/cloud/ec-faq-technical.md](/raw-migrated-files/cloud/cloud/ec-faq-technical.md)

# Security

This overview page helps you understand Elastic's security capabilities across different deployment types. You'll find:

- Key security features for protecting your Elastic deployment
- Security capabilities specific to each deployment type
- Comparison tables showing feature availability and configurability by deployment type
- Links to detailed implementation guides

## Security overview

An Elastic implementation comprises many moving parts: {{es}} nodes forming the cluster, {{kib}} instances, additional stack components such as Logstash and Beats, and various clients and integrations communicating with your deployment.

To keep your data secured, Elastic offers comprehensive security features that:
- Prevent unauthorized access to your deployment
- Encrypt communications between components
- Protect data at rest
- Secure sensitive settings and saved objects

:::{note}
The availability and configurability of security features vary by deployment type. Refer to [Security by deployment type](#security-features-by-deployment-type) for a comparison table.
:::

## Security topics

The documentation is organized into four main areas.

On every page, you'll see deployment type indicators that show which content applies to specific deployment types. Focus on sections tagged with your deployment type and look for subsections specifically addressing your deployment model.

### 1. Secure your orchestrator

The [security of your orchestrator](security/secure-hosting-environment.md) forms the foundation of your overall security posture. This section covers environment-specific security controls:

- [**Elastic Cloud Hosted and Serverless**](security/secure-your-elastic-cloud-organization.md)
- [**Elastic Cloud Enterprise**](security/secure-your-elastic-cloud-enterprise-installation.md)
- [**Elastic Cloud on Kubernetes**](security/secure-your-eck-installation.md)

:::{note}
There is no orchestration layer for self-managed deployments because you directly control the host environment. Refer to [](security/manually-configure-security-in-self-managed-cluster.md) to learn more about securing self-managed installations.
:::

### 2. Secure your deployments and clusters

[Secure your deployments](security/secure-your-cluster-deployment.md) with features available across all deployment types:

- [**Traffic filtering**](security/traffic-filtering.md): IP filtering, private links, and static IPs
- [**Secure communications**](security/secure-cluster-communications.md): TLS configuration, certificates management
- [**Data protection**](security/data-security.md): Encryption at rest, secure settings, saved objects
- [**Session management**](security/kibana-session-management.md): Kibana session controls
- [**FIPS 140-2 compliance**](security/fips-140-2.md): Federal security standards

### 3. Secure your personal account

[Secure your personal account](security/secure-your-personal-account.md) to help prevent unauthorized access:

- Multi-factor authentication and account security best practices

### 4. Secure your clients and integrations

[Secure your clients and integrations](security/secure-clients-integrations.md) to ensure secure communication between your applications and Elastic:

- [**Client security**](security/httprest-clients-security.md): Best practices for securely connecting applications to {{es}}
- **Integration security**: Secure configuration for Beats, Logstash, and other integrations

## Security features by deployment type

Security feature availability varies by deployment type, with each feature having one of the following statuses:

| **Status** | **Description** |
|--------|-------------|
| **Managed** | Handled automatically by Elastic with no user configuration needed |
| **Configurable** | Built-in feature that needs your configuration (like IP filters or passwords) |
| **Self-managed** | Infrastructure-level security you implement and maintain |
| **N/A** | Not available for this deployment type |

Select your deployment type below to see what's available and how implementation responsibilities are distributed:

::::{tab-set}
:group: deployment-type

:::{tab-item} Elastic Cloud Hosted
:sync: cloud-hosted

| **Security Category** | **Security Feature** | **Status** | **Description** |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP Layer) | Managed | Automatically configured by Elastic |
| | TLS (Transport Layer) | Managed | Automatically configured by Elastic |
| **Network** | IP traffic filtering | Configurable | Configure IP-based access restrictions |
| | Private link | Configurable | Establish secure VPC connection |
| | Static IPs | Configurable | Enable fixed IP addresses |
| **Data** | Encryption at rest | Managed | Automatically encrypted by Elastic |
| | Bring your own encryption key | Configurable | Implement customer-provided keys |
| | Keystore security | Managed | Automatically protected by Elastic |
| | Saved object encryption | Managed | Automatically encrypted by Elastic |
| **User Session** | Kibana Sessions | Configurable | Customize session parameters |

:::

:::{tab-item} Serverless
:sync: serverless

| **Security Category** | **Security Feature** | **Status** | **Description** |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP Layer) | Managed | Automatically configured by Elastic |
| | TLS (Transport Layer) | Managed | Automatically configured by Elastic |
| **Network** | IP traffic filtering | Configurable | Configure IP-based access restrictions |
| | Private link | N/A | X |
| | Static IPs | Configurable | Enable fixed IP addresses |
| **Data** | Encryption at rest | Managed | Automatically encrypted by Elastic |
| | Bring your own encryption key | N/A | X |
| | Keystore security | Managed | Automatically protected by Elastic |
| | Saved object encryption | Managed | Automatically encrypted by Elastic |
| **User Session** | Kibana Sessions | Managed | Automatically configured by Elastic |

:::

:::{tab-item} ECE/ECK
:sync: ece-eck

| **Security Category** | **Security Feature** | **Status** | **Description** |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP Layer) | Configurable | Configure custom certificates |
| | TLS (Transport Layer) | Managed | Automatically configured by Elastic |
| **Network** | IP traffic filtering | Configurable | Configure IP-based access restrictions |
| | Private link | N/A | X |
| | Static IPs | N/A | X |
| **Data** | Encryption at rest | Self-managed | Implement at infrastructure level |
| | Bring your own encryption key | N/A | X |
| | Keystore security | Configurable | Configure secure settings storage |
| | Saved object encryption | Configurable | Enable encryption for saved objects |
| **User Session** | Kibana Sessions | Configurable | Customize session parameters |

:::

:::{tab-item} Self-managed
:sync: self-managed

| **Security Category** | **Security Feature** | **Status** | **Description** |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP Layer) | Self-managed | Implement and maintain certificates |
| | TLS (Transport Layer) | Self-managed | Implement and maintain certificates |
| **Network** | IP traffic filtering | Configurable | Configure IP-based access restrictions |
| | Private link | N/A | X |
| | Static IPs | N/A | X |
| **Data** | Encryption at rest | Self-managed | Implement at infrastructure level |
| | Bring your own encryption key | N/A | X |
| | Keystore security | Configurable | Configure secure settings storage |
| | Saved object encryption | Configurable | Enable encryption for saved objects |
| **User Session** | Kibana Sessions | Configurable | Customize session parameters |

:::

::::

## Next steps

Refer to the following sections for detailed instructions about securing your hosting environment:

* [Elastic Cloud Hosted and Serverless security setup](/deploy-manage/security/secure-your-elastic-cloud-organization.md)
* [Elastic Cloud Enterprise (ECE) security setup](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation.md)
* [Elastic Cloud on Kubernetes (ECK) security setup](/deploy-manage/security/secure-your-eck-installation.md)
* [Self-managed cluster security setup](/deploy-manage/security/manually-configure-security-in-self-managed-cluster.md)