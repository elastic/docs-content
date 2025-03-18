---
navigation_title: Manage TLS certificates 
applies_to:
  deployment:
    self:
    eck:
    ece:
mapped_urls:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-security.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup.html
  - https://www.elastic.co/guide/en/kibana/current/elasticsearch-mutual-tls.html
---


% TODO: what to do about this page that doesn't exist
% * [/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-security.md](/raw-migrated-files/cloud-on-k8s/cloud-on-k8s/k8s-security.md)

$$$encrypt-internode-communication$$$
$$$generate-certificates$$$


# Manage TLS certificates

This page explains how to secure communications between components in your {{stack}} deployment.

For {{ech}} and {{serverless-full}} deployments, communications security is fully managed by Elastic with no configuration required.

For ECE, ECK, and self-managed deployments, this page provides specific configuration guidance to secure the various communication channels between components.

:::{tip}
For a complete comparison of security feature availability and responsibility by deployment type, see [Security features by deployment type](/deploy-manage/security.md#comparison-table).
:::

## Communication channels overview

Your {{stack}} deployment includes several distinct communication channels that must be secured to protect your data and infrastructure.

| **Channel** | **Description** | **Security needs** |
|-------------|-----------------|--------------------|
| [Transport layer](#transport-layer-security) | Communication between {{es}} nodes within a cluster | - Mutual TLS (required)<br>- Node authentication<br>- Node role verification |
| [HTTP layer](#http-layer-security) | Communication between external clients and {{es}} through the REST API | - TLS encryption<br>- Authentication (basic auth, API keys, or token-based)<br>- Optional client certificate authentication |
| [{{kib}}-to-{{es}}](#kib-to-es-communications) | Communication from the {{kib}} server to {{es}} for user requests and queries | - TLS encryption<br>- Service authentication (API keys, service tokens, or mutual TLS) |


## Transport layer security

The transport layer is used for communication between {{es}} nodes in a cluster. Securing this layer prevents unauthorized nodes from joining your cluster and protects internode data.

**Deployment type notes:**
- **Elastic Cloud, ECE, and Serverless**: Transport security is fully managed by Elastic. No configuration is required.
- **ECK**: Transport security is automatically configured by the operator, but you can [customize its service and SSL certificates](/deploy-manage/security/k8s-transport-settings.md).
- **Self-managed**: Transport security must be manually configured following the steps in [Set up basic security](set-up-basic-security.md).

## HTTP layer security

The HTTP layer secures client communication with your {{es}} cluster via its REST API, preventing unauthorized access and protecting data in transit.

**Deployment type notes:**
- **Elastic Cloud & Serverless**: HTTP security is fully managed by Elastic. No configuration is required.
- **ECE**: HTTP security is automatically enforced at ECE proxies using self-signed certificates and a default [wildcard DNS record](/deploy-manage/deploy/cloud-enterprise/ece-wildcard-dns.md). However, it's recommended to [configure your own certificates](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md).
- **ECK**: HTTP security is automatically configured with self-signed certificates. Custom certificates and domain names can be configured.
- **Self-managed**: HTTP security must be manually configured following [Secure HTTP communications](secure-http-communications.md).

## {{kib}}-to-{{es}} communications

{{kib}} connects to {{es}} as a client but requires special configuration as it performs operations on behalf of end users.

**Deployment type notes:**
- **Elastic Cloud & Serverless**: {{kib}}-{{es}} communication is fully managed using HTTPS and service tokens.
- **ECE/ECK**: {{kib}}-{{es}} communication is automatically secured with service tokens.
- **Self-managed**: {{kib}}-{{es}} communication must be manually secured. For mutual TLS configuration, see [Mutual TLS authentication between {{kib}} and {{es}}](secure-http-communications.md#elasticsearch-mutual-tls).

## Certificate management [generate-certificates]

Managing certificates is critical for secure communications. Certificates have limited lifetimes and must be renewed before expiry to prevent service disruptions.

**Deployment type notes:**
- **Elastic Cloud & Serverless**: Certificate management is fully automated by Elastic.
- **ECE**: ECE generates certificates for you. Refer to [](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md).

**ECK**: ECK provides flexible options for managing SSL certificates in your deployments, including automatic certificate generation and rotation, integration with external tools like `cert-manager`, or using your own custom certificates. Custom HTTP certificates require manual management.
- **Self-managed**: Certificate management is your responsibility. See [Security certificates and keys](security-certificates-keys.md).

## Next steps

- Configure [basic security and HTTPS](set-up-basic-security-plus-https.md) for self-managed deployments.
- Learn about [HTTP communication security](secure-http-communications.md) best practices.
- Understand how to securely manage [security certificates and keys](security-certificates-keys.md).
- Check [SSL/TLS version compatibility](supported-ssltls-versions-by-jdk-version.md) for optimal encryption.
