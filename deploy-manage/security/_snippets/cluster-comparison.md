Security feature availability varies by deployment type, with each feature having one of the following statuses:

| Status | Description |
|--------|-------------|
| **Fully managed** | Handled automatically by Elastic with no user configuration needed |
| **Managed** | Handled automatically by Elastic, but certain configuration allowed |
| **Configurable** | Built-in feature that needs your configuration (like IP filters or passwords) |
| **Self-managed** | Infrastructure-level security you implement and maintain |
| **N/A** | Not available for this deployment type |

Select your deployment type below to see what's available and how implementation responsibilities are distributed:

::::{tab-set}
:group: deployment-type

:::{tab-item} {{ech}}
:sync: cloud-hosted

| Category | Security feature | Status | Notes |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP Layer) | Fully managed | Automatically configured by Elastic |
| | TLS (Transport Layer) | Fully managed | Automatically configured by Elastic |
| **Network** | IP traffic filtering | Configurable | [Configure IP-based access restrictions](/deploy-manage/security/ip-traffic-filtering.md) |
| | Private link | Configurable | [Establish a secure VPC connection](/deploy-manage/security/private-link-traffic-filters.md) |
| | Kubernetes Network Policies | N/A |  |
| **Data** | Encryption at rest | Managed | You can [bring your own encryption key](/deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md) |
| | Secure settings | Configurable | Automatically protected by Elastic |
| | Saved object encryption | Fully managed | Automatically encrypted by Elastic |
| **User session** | Kibana sessions | Configurable | [Customize session parameters](/deploy-manage/security/kibana-session-management.md) |

:::

:::{tab-item} Serverless
:sync: serverless

| Category| Security feature | Status | Description |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP Layer) | Fully managed | Automatically configured by Elastic |
| | TLS (Transport Layer) | Fully managed | Automatically configured by Elastic |
| **Network** | IP traffic filtering | Configurable | [Configure IP-based access restrictions](/deploy-manage/security/ip-traffic-filtering.md) |
| | Private link | N/A | X |
| | Kubernetes Network Policies | N/A |  |
| **Data** | Encryption at rest | Fully managed | Automatically encrypted by Elastic |
| | Secure settings | Configurable | Automatically protected by Elastic |
| | Saved object encryption | Fully managed | Automatically encrypted by Elastic |
| **User Session** | Kibana Sessions | Managed | Automatically configured by Elastic |

:::

:::{tab-item} ECE
:sync: ece

| Category| Security feature | Status | Description |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP Layer) | Managed | You can [configure custom certificates](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md) |
| | TLS (Transport Layer) | Fully managed | Automatically configured by Elastic |
| **Network** | IP traffic filtering | Configurable | [Configure IP-based access restrictions](/deploy-manage/security/ip-traffic-filtering.md) |
| | Private link | N/A | X |
| | Kubernetes Network Policies | N/A |  |
| **Data** | Encryption at rest | Self-managed | Implement at infrastructure level |
| | Secure settings | Configurable | [Configure secure settings](/deploy-manage/security/secure-settings.md) |
| | Saved object encryption | Configurable | [Enable encryption for saved objects](/deploy-manage/security/secure-saved-objects.md) |
| **User Session** | Kibana Sessions | Configurable | [Customize session parameters](/deploy-manage/security/kibana-session-management.md) |

:::

:::{tab-item} ECK
:sync: eck

| Category| Security feature | Status | Description |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP Layer) | Managed | [Multiple options](/deploy-manage/security/k8s-https-settings.md) |
| | TLS (Transport Layer) | Managed | [Multiple options](/deploy-manage/security/k8s-transport-settings.md) |
| **Network** | IP traffic filtering | Configurable | [Configure IP-based access restrictions](/deploy-manage/security/ip-traffic-filtering.md) |
| | Private link | N/A |  |
| | Kubernetes Network Policies | Configurable | [Apply network policies to your Pods](/deploy-manage/security/k8s-network-policies.md) |
| **Data** | Encryption at rest | Self-managed | Implement at infrastructure level |
| | Secure settings | Configurable | [Configure secure settings](/deploy-manage/security/k8s-secure-settings.md) |
| | Saved object encryption | Configurable | [Enable encryption for saved objects](/deploy-manage/security/secure-saved-objects.md) |
| **User Session** | Kibana Sessions | Configurable | [Customize session parameters](/deploy-manage/security/kibana-session-management.md) |

:::


:::{tab-item} Self-managed
:sync: self-managed

| Category| Security feature | Status | Description |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP Layer) | Self-managed | Implement and maintain certificates |
| | TLS (Transport Layer) | Self-managed | Implement and maintain certificates |
| **Network** | IP traffic filtering | Configurable | [Configure IP-based access restrictions](/deploy-manage/security/ip-traffic-filtering.md) |
| | Private link | N/A | X |
| | Kubernetes Network Policies | N/A |  |
| **Data** | Encryption at rest | Self-managed | Implement at infrastructure level |
| | Keystore security | Configurable | [Configure secure settings](/deploy-manage/security/secure-settings.md) storage |
| | Saved object encryption | Configurable | [Enable encryption for saved objects](/deploy-manage/security/secure-saved-objects.md) |
| **User Session** | Kibana Sessions | Configurable | [Customize session parameters](/deploy-manage/security/kibana-session-management.md) |

:::
::::