Security feature availability varies by deployment type, with each feature having one of the following statuses:

| Status | Description |
|--------|-------------|
| **Fully managed** | Handled automatically by Elastic with no user configuration needed |
| **Managed** | Handled automatically by Elastic, but certain configuration allowed |
| **Configurable** | Built-in feature that needs your configuration (like IP filters or passwords) |
| **N/A** | Not available for this deployment type |

Select your deployment type below to see what's available and how implementation responsibilities are distributed:

::::{tab-set}
:group: deployment-type

:::{tab-item} ECH
:sync: cloud-hosted

| Category | Security feature | Status | Notes |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP layer) | Fully managed | Automatically configured by Elastic |
| | TLS (Transport layer) | Fully managed | Automatically configured by Elastic |
| **Network** | IP filtering | Configurable | [Configure IP-based access restrictions](/deploy-manage/security/ip-filtering-cloud.md) |
| | Private connectivity and VPC filtering | Configurable | [Establish a secure VPC connection](/deploy-manage/security/private-connectivity.md) |
| | Kubernetes network policies | N/A |  |
| **Data** | Encryption at rest | Managed | You can [bring your own encryption key](/deploy-manage/security/encrypt-deployment-with-customer-managed-encryption-key.md) |
| | Secure settings | Configurable | [Configure secure settings](/deploy-manage/security/secure-settings.md) |
| | Saved object encryption | Fully managed | Automatically encrypted by Elastic |
| **User session** | {{kib}} sessions | Configurable | [Customize session parameters](/deploy-manage/security/kibana-session-management.md) |

:::

:::{tab-item} Serverless
:sync: serverless

| Category| Security feature | Status | Notes |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP layer) | Fully managed | Automatically configured by Elastic |
| | TLS (Transport layer) | Fully managed | Automatically configured by Elastic |
| **Network** | IP filtering | Configurable | [Configure IP-based access restrictions](/deploy-manage/security/ip-filtering-cloud.md) |
| | Private connectivity and VPC filtering | N/A |  |
| | Kubernetes network policies | N/A |  |
| **Data** | Encryption at rest | Fully managed | Automatically encrypted by Elastic |
| | Secure settings | N/A |  |
| | Saved object encryption | Fully managed | Automatically encrypted by Elastic |
| **User session** | {{kib}} sessions | Fully managed | Automatically configured by Elastic |

:::

:::{tab-item} ECE
:sync: ece

| Category| Security feature | Status | Notes |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP layer) | Managed | You can [configure custom certificates](/deploy-manage/security/secure-your-elastic-cloud-enterprise-installation/manage-security-certificates.md) |
| | TLS (Transport layer) | Fully managed | Automatically configured by Elastic |
| **Network** | IP filtering | Configurable | [Configure IP-based access restrictions](/deploy-manage/security/ip-filtering-cloud.md) |
| | Private connectivity and VPC filtering | N/A |  |
| | Kubernetes network policies | N/A |  |
| **Data** | Encryption at rest | N/A |  |
| | Secure settings | Configurable | [Configure secure settings](/deploy-manage/security/secure-settings.md) |
| | Saved object encryption | Configurable | [Enable encryption for saved objects](/deploy-manage/security/secure-saved-objects.md) |
| **User session** | {{kib}} sessions | Configurable | [Customize session parameters](/deploy-manage/security/kibana-session-management.md) |

:::

:::{tab-item} ECK
:sync: eck

| Category| Security feature | Status | Notes |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP layer) | Managed | [Multiple options](/deploy-manage/security/k8s-https-settings.md) for customization |
| | TLS (Transport layer) | Managed | [Multiple options](/deploy-manage/security/k8s-transport-settings.md) for customization |
| **Network** | IP filtering | Configurable | [Configure IP-based access restrictions](/deploy-manage/security/ip-filtering-basic.md) |
| | Private connectivity and VPC filtering | N/A |  |
| | Kubernetes network policies | Configurable | [Apply network policies to your Pods](/deploy-manage/security/k8s-network-policies.md) |
| **Data** | Encryption at rest | N/A |  |
| | Secure settings | Configurable | [Configure secure settings](/deploy-manage/security/k8s-secure-settings.md) |
| | Saved object encryption | Configurable | [Enable encryption for saved objects](/deploy-manage/security/secure-saved-objects.md) |
| **User session** | {{kib}} sessions | Configurable | [Customize session parameters](/deploy-manage/security/kibana-session-management.md) |

:::


:::{tab-item} Self-managed
:sync: self-managed

| Category| Security feature | Status | Notes |
|------------------|------------|--------------|-------------|
| **Communication** | TLS (HTTP layer) | Configurable | Can be automatically or manually configured. See [Initial security setup](/deploy-manage/security/self-setup.md) |
| | TLS (Transport layer) | Configurable | Can be automatically or manually configured. See [Initial security setup](/deploy-manage/security/self-setup.md) |
| **Network** | IP filtering | Configurable | [Configure IP-based access restrictions](/deploy-manage/security/ip-filtering-basic.md) |
| | Private connectivity and VPC filtering | N/A |  |
| | Kubernetes network policies | N/A |  |
| **Data** | Encryption at rest | N/A |  |
| | Keystore security | Configurable | [Configure secure settings](/deploy-manage/security/secure-settings.md) |
| | Saved object encryption | Configurable | [Enable encryption for saved objects](/deploy-manage/security/secure-saved-objects.md) |
| **User session** | {{kib}} sessions | Configurable | [Customize session parameters](/deploy-manage/security/kibana-session-management.md) |

:::
::::