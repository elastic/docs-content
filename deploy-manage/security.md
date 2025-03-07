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

This section covers how to secure your Elastic Stack at the infrastructure and communication levels. Learn how to implement TLS encryption, network security controls, and data protection measures.

## Security overview

An Elastic implementation comprises many moving parts: {es} nodes forming the cluster, {kib} instances, additional stack components such as Logstash and Beats, and various clients and integrations communicating with your deployment.

To keep your data secured, Elastic offers comprehensive security features that:
- Prevent unauthorized access to your deployment
- Encrypt communications between components
- Protect data at rest
- Secure configuration settings and saved objects

Different deployment types have different security requirements and capabilities. Some security features are managed automatically, while others require manual configuration depending on your deployment type.

::::{tip}
See the [Deployment overview](/deploy-manage/deploy.md) to understand your options for deploying Elastic.
::::

### Security by deployment type

#### Communication security

| **Security Feature** | Serverless | Elastic Cloud | ECE | ECK | Self-managed |
|------------------|------------|--------------|-----|-----|--------------|
| **TLS (HTTP Layer)** | ✓ Managed  | ✓ Managed     | ✓ Configurable | ✓ Configurable | ✓ Manual |
| **TLS (Transport Layer)** | ✓ Managed | ✓ Managed | ✓ Managed | ✓ Managed | ✓ Manual |

#### Network security

| **Security Feature** | Serverless | Elastic Cloud | ECE | ECK | Self-managed |
|------------------|------------|--------------|-----|-----|--------------|
| **IP Traffic Filtering** | ✓ Available | ✓ Available | ✓ Available | ✓ Available | ✓ Available |
| **Private Link** | ✗ N/A | ✓ Available | ✗ N/A | ✗ N/A | ✗ N/A |
| **Static IPs** | ✓ Available | ✓ Available | ✗ N/A | ✗ N/A | ✗ N/A |

#### Data security

| **Security Feature** | Serverless | Elastic Cloud | ECE | ECK | Self-managed |
|------------------|------------|--------------|-----|-----|--------------|
| **Encryption at Rest** | ✓ Default | ✓ Default | ✗ Manual | ✗ Manual | ✗ Manual |
| **BYOK/CMEK** | ✗ N/A | ✓ Available | ✗ N/A | ✗ N/A | ✗ N/A |
| **Keystore Security** | ✓ Available | ✓ Available | ✓ Available | ✓ Available | ✓ Available |
| **Saved Object Encryption** | ✓ Available | ✓ Available | ✓ Available | ✓ Available | ✓ Available |

#### User session security

| **Security Feature** | Serverless | Elastic Cloud | ECE | ECK | Self-managed |
|------------------|------------|--------------|-----|-----|--------------|
| **Kibana Sessions** | ✓ Managed | ✓ Configurable | ✓ Configurable | ✓ Configurable | ✓ Configurable |

### Using this documentation

Throughout this security documentation, you'll see deployment type indicators that show which content applies to specific deployment types. Each section clearly identifies which deployment types it applies to, and deployment-specific details are separated within each topic.

To get the most relevant information for your environment, focus on sections tagged with your deployment type and look for subsections specifically addressing your deployment model.

## Security topics

This security documentation is organized into four main areas:

% TODO: Add links to the sections below

### 1. Secure your hosting environment

The security of your hosting environment forms the foundation of your overall security posture. This section covers environment-specific security controls:

- **Self-managed environments**: TLS certificates, HTTPS configuration
- **Elastic Cloud Enterprise**: TLS certificates, Cloud RBAC
- **Elastic Cloud Hosted and Serverless**: Organization-level SSO, role-based access control, and cloud API keys

### 2. Secure your deployments and clusters

Protect your deployments with features available across all deployment types:

- **Authentication and access controls**: User management, authentication protocols, and traffic filtering
- **Data protection**: Encryption, sensitive settings, and document-level security
- **Monitoring and compliance**: Audit logging and security best practices

### 3. Secure your user accounts

Individual user security helps prevent unauthorized access:

- **Multi-factor authentication**: Add an extra layer of security to your login process
- **API key management**: Secure programmatic access to Elastic resources

### 4. Secure your clients and integrations

Ensure secure communication between your applications and Elastic:

- **Client security**: Best practices for securely connecting applications to {es}
- **Integration security**: Secure configuration for Beats, Logstash, and other integrations

