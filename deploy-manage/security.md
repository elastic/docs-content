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

% We do provide [static IP ranges](../../../deploy-manage/security/elastic-cloud-static-ips.md), but they should be used with caution as noted in the documentation. IP addresses assigned to cloud resources can change without notice. This could be initiated by cloud providers with no knowledge to us. For this reason, we generally do not recommend that you use firewall rules to allow or restrict certain IP ranges. If you do wish to secure communication for deployment endpoints on {{ech}}, please use [Private Link](../../../deploy-manage/security/traffic-filtering.md). However, in situations where using Private Link services do not meet requirements (for example, secure traffic **from** Elastic Cloud), static IP ranges can be used.

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/346

% Scope notes: this is just communication security - link to users + roles, spaces, monitoring, ++

$$$field-document-limitations$$$

$$$alias-limitations$$$

$$$preventing-unauthorized-access$$$

$$$preserving-data-integrity$$$

$$$maintaining-audit-trail$$$

:::{warning}
**This page is a work in progress.** 
:::


# Security

An Elastic implementation comprises many moving parts: {{es}} nodes forming the cluster, {{kib}} instances, additional stack components such as Logstash and Beats, and various clients and integrations, all communicating with your cluster.

To keep your data secured, Elastic offers security features that prevent bad actors from tampering with your data, and encrypt communications to, from, and within your cluster. Regardless of your deployment type, Elastic sets up certain security features for you automatically.

The documentation is organized into three main areas.

* [Secure your orchestrator](security/secure-hosting-environment.md): Setup security in your [{{ece}}](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation.md) or [{{eck}}](/deploy-manage/security/secure-your-eck-installation.md) installations.
* [Secure your cluster or deployment](./security/secure-your-cluster-deployment.md): Learn about how to manage basic Elastic security features. You’ll also learn how to implement advanced security measures.
* [Secure your clients and integrations](security/secure-clients-integrations.md): Secure communications between your applications and the {{stack}}.

::::{note}
As part of your overall security strategy, you can also do the following:

* Prevent unauthorized access with [password protection and role-based access control](/deploy-manage/users-roles.md).
* Control access to dashboards and other saved objects in your UI using [Spaces](/deploy-manage/manage-spaces.md).
* Connect a local cluster to a [remote cluster](/deploy-manage/remote-clusters.md) to enable [cross-cluster replication](/deploy-manage/tools/cross-cluster-replication.md) and [cross-cluster search](/solutions/search/cross-cluster-search.md).
* Manage [API keys](/deploy-manage/api-keys.md) used for programmatic access to Elastic.
::::

The availability and configurability of security features vary by deployment type. On every page, you'll see deployment type indicators that show which content applies to specific deployment types. Focus on sections tagged with your deployment type and look for subsections specifically addressing your deployment model.

At the end of this doc, there's also a [comparison table](#comparison-table) showing feature availability and configurability by deployment type.

## Managed security in Elastic Cloud
```yaml {applies_to}
deployment:
  ess: all
serverless: all
```

Elastic Cloud has built-in security. For example, HTTPS communications between Elastic Cloud and the internet, as well as inter-node communications, are secured automatically, and cluster data is encrypted at rest. 

In {{ech}}, you can augment these security features in the following ways:
* Configure [traffic filtering](./security/traffic-filtering.md) to prevent unauthorized access to your deployments.
* Encrypt your deployment with a [customer-managed encryption key](./security/encrypt-deployment-with-customer-managed-encryption-key.md).
* [Secure your settings](./security/secure-settings.md) using {{es}} and {{kib}} keystores.
* Use the list of [Elastic Cloud static IPs](./security/elastic-cloud-static-ips.md) to allow or restrict communications in your infrastructure.

::::{note}
Serverless projects are fully managed and secured by Elastic, and do not have any configurable security features at the project level.
::::

Refer to [Elastic Cloud security](https://www.elastic.co/cloud/security) for more details about Elastic security and privacy programs.

## Cluster or deployment security features

You can configure the following aspects of your Elastic implementation to maintain and enhance security:

### Manage TLS certificates
```yaml {applies_to}
deployment:
  ece: all
  eck: all
  self: all
```

TLS certificates apply security controls to network communications. TLS is the modern name for what used to be called Secure Sockets Layer (SSL).

TLS certificates are used in two places:
* **The HTTP layer**: Used for communication between your cluster or deployment and the internet.
* **The transport layer**: Used mainly for inter-node communications, and in certain cases for cluster to cluster communication.

The way that TLS certificates are managed depends on your deployment type:

* In self-managed {{es}} clusters, you [manage both of these certificates yourself](./security/secure-cluster-communications.md). You can also [Configure Kibana and Elasticsearch to use mutual TLS](./security/secure-http-communications.md#elasticsearch-mutual-tls).
* In {{ece}}, you can use one or more [proxy certificates](./security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md) to secure the HTTP layer. These certificates are managed at the ECE installation level. Transport-level encryption is managed by ECE and certificates can’t be changed.
* In {{eck}}, you can [manage certificates for the HTTP layer](./security/secure-http-communications.md#k8s-custom-http-certificate). Certificates for the transport layer are managed by ECK and can’t be changed. However, you can set your own certificate authority, customize certificate contents, and provide your own certificate generation tools using [transport settings](./security/k8s-transport-settings.md).

::::{tip}
Elastic Cloud manages TLS certificates for you.
::::

#### Enable cipher suites for stronger encryption

TBD  - to refine
Refer to [](./security/enabling-cipher-suites-for-stronger-encryption.md) for more details.
(These cipher_suites settings are used for a bunch of different auth realms as well as http/transport layer)

### Restrict connections using traffic filtering
```yaml {applies_to}
deployment:
  ess: all
  ece: all
  eck: all
  self: all
```

[Traffic filtering](./security/traffic-filtering.md) allows you to limit how your deployments can be accessed. Add another layer of security to your installation and deployments by restricting inbound traffic to only the sources that you trust.

* For all deployment types, you can configure [IP-based traffic filters](./security/ip-traffic-filtering.md).

* For Elastic Cloud Hosted, you can also configure [private link traffic filters](./security/private-link-traffic-filters.md).

* For {{eck}}, you can use [Kubernetes network policies](./security/k8s-network-policies.md).

### Allow or deny Elastic Cloud IP ranges
```yaml {applies_to}
deployment:
  ess: all
```

Elastic Cloud publishes a list of IP addresses used by its services for both incoming and outgoing traffic. Users can use these lists to configure their network firewalls as needed to allow or restrict traffic related to Elastic Cloud services.

[Learn more about Elastic Cloud static IPs](./security/elastic-cloud-static-ips.md).

### Manage Kibana sessions
```yaml {applies_to}
deployment:
  ess: all
  ece: all
  eck: all
  self: all
```

Control the timeout and lifespan of logged-in sessions to Kibana, as well as the number of concurrent sessions each user can have.

[Learn more about {{kib}} session management](./security/kibana-session-management.md).

### Encryption at rest
```yaml {applies_to}
serverless: all
deployment:
  ess: all
```

By default, Elastic Cloud already encrypts your deployment data, project data, and snapshots at rest.

If you’re using Elastic Cloud Hosted, then you can reinforce this mechanism by providing your own encryption key, also known as [Bring Your Own Key (BYOK)](./security/encrypt-deployment-with-customer-managed-encryption-key.md).

::::{note}
Other deployment types don’t implement encryption at rest out of the box. For self-managed clusters, to implement encryption at rest, the hosts running the cluster must be configured with disk-level encryption, such as `dm-crypt`. In addition, snapshot targets must ensure that data is encrypted at rest as well.

Configuring `dm-crypt` or similar technologies is outside the scope of this documentation, and issues related to disk encryption are outside the scope of support.
::::

### Secure your settings
```yaml {applies_to}
deployment:
  ess: all
  ece: all
  eck: all
  self: all
```

Some of the settings that you configure in Elasticsearch Service are sensitive, such as passwords, and relying on file system permissions to protect these settings is insufficient. Learn how to configure secure settings in the {{es}} keystore or {{kib}} keystore.

[Learn more about storing settings in a keystore](./security/secure-settings.md).


### Secure saved objects
```yaml {applies_to}
deployment:
  ess: all
  ece: all
  eck: all
  self: all
```

Kibana stores entities such as dashboards, visualizations, alerts, actions, and advanced settings as saved objects, which are kept in a dedicated, internal {{es}} index. If such an object includes sensitive information, for example a PagerDuty integration key or email server credentials used by the alert action, {{kib}} encrypts it and makes sure it cannot be accidentally leaked or tampered with.

Encrypting sensitive information means that a malicious party with access to the Kibana internal indices won’t be able to extract that information without also knowing the encryption key.

[Learn how to configure and rotate the saved object encryption key](./security/secure-saved-objects.md).


### Other topics
```yaml {applies_to}
deployment:
  ess: all
  ece: all
  eck: all
  self: all
```

TBD / to determine if needed

% we need to refine this table, but the idea is awesome IMO
## Security features by deployment type [comparison-table]

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
