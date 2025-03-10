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

This section covers how to secure your Elastic environment. Learn how to implement TLS encryption, network security controls, and data protection measures.

## Security overview

An Elastic implementation comprises many moving parts: {es} nodes forming the cluster, {kib} instances, additional stack components such as Logstash and Beats, and various clients and integrations communicating with your deployment.

To keep your data secured, Elastic offers comprehensive security features that:
- Prevent unauthorized access to your deployment
- Encrypt communications between components
- Protect data at rest
- Secure sensitive settings and saved objects

Security requirements and capabilities vary by deployment. Features may be managed automatically by Elastic, require configuration, or must be fully self-managed. Refer to [Security by deployment type](#security-by-deployment-type) for details.

::::{tip}
See the [Deployment overview](/deploy-manage/deploy.md) to understand your options for deploying Elastic.
::::

### Security by deployment type

Security features have one of these statuses across deployment types:

| Status | Description |
|--------|-------------|
| **Managed** | Handled automatically by Elastic with no user configuration needed |
| **Configurable** | Built-in feature that needs your configuration (like IP filters or passwords) |
| **Self-managed** | Infrastructure-level security you implement and maintain |
| **N/A** | Not available for this deployment type |

#### Communication security

| **Security feature** | Serverless | Elastic Cloud Hosted | ECE | ECK | Self-managed |
|------------------|------------|--------------|-----|-----|--------------|
| **TLS (HTTP Layer)** | Managed | Managed | Configurable | Configurable | Self-managed |
| **TLS (Transport Layer)** | Managed | Managed | Managed | Managed | Self-managed |

#### Network security

| **Security feature** | Serverless | Elastic Cloud Hosted | ECE | ECK | Self-managed |
|------------------|------------|--------------|-----|-----|--------------|
| **IP traffic filtering** | Configurable | Configurable | Configurable | Configurable | Configurable |
| **Private link** | N/A | Configurable | N/A | N/A | N/A |
| **Static IPs** | Configurable | Configurable | N/A | N/A | N/A |

#### Data security

| **Security feature** | Serverless | Elastic Cloud Hosted | ECE | ECK | Self-managed |
|------------------|------------|--------------|-----|-----|--------------|
| **Encryption at rest** | Managed | Managed | Self-managed | Self-managed | Self-managed |
| **Bring your own encryption key** | N/A | Configurable | N/A | N/A | N/A |
| **Keystore security** | Managed | Managed | Configurable | Configurable | Configurable |
| **Saved object encryption** | Managed | Managed | Configurable | Configurable | Configurable |

#### User session security

| **Security feature** | Serverless | Elastic Cloud Hosted | ECE | ECK | Self-managed |
|------------------|------------|--------------|-----|-----|--------------|
| **Kibana Sessions** | Managed | Configurable | Configurable | Configurable | Configurable |

### Using this documentation

Throughout this security documentation, you'll see deployment type indicators that show which content applies to specific deployment types. Each section clearly identifies which deployment types it applies to, and deployment-specific details are separated within each topic.

To get the most relevant information for your environment, focus on sections tagged with your deployment type and look for subsections specifically addressing your deployment model.

## Security topics

This security documentation is organized into four main areas:

% TODO: Add links to the sections below

### 1. Secure your hosting environment

The security of your hosting environment forms the foundation of your overall security posture. This section covers environment-specific security controls:

- **Elastic Cloud Hosted and Serverless**: Organization-level SSO, role-based access control, and cloud API keys
- **Elastic Cloud Enterprise**: TLS certificates, role-based access control, and cloud API keys
- **Self-managed environments**: TLS certificates, HTTPS configuration

### 2. Secure your deployments and clusters

Protect your deployments with features available across all deployment types:

- **Authentication and access controls**: User management, API keys, authentication protocols, and traffic filtering
- **Data protection**: Encryption, sensitive settings, and document-level security
- **Monitoring and compliance**: Audit logging and security best practices

### 3. Secure your user accounts

Individual user security helps prevent unauthorized access:

- **Multi-factor authentication**: Add an extra layer of security to your login process

### 4. Secure your clients and integrations

Ensure secure communication between your applications and Elastic:

- **Client security**: Best practices for securely connecting applications to {es}
- **Integration security**: Secure configuration for Beats, Logstash, and other integrations

