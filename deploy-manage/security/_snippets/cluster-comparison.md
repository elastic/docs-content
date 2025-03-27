Security feature availability varies by deployment type, with each feature having one of the following statuses:

| Status | Description |
|--------|-------------|
| **Managed** | Handled automatically by Elastic with no user configuration needed |
| **Configurable** | Built-in feature that needs your configuration (like IP filters or passwords) |
| **Self-managed** | Infrastructure-level security you implement and maintain |
| **N/A** | Not available for this deployment type |

Select your deployment type below to see what's available and how implementation responsibilities are distributed:

::::{tab-set}
:group: deployment-type

:::{tab-item} {{ech}}
:sync: cloud-hosted

| Category | Security feature | Status | Description |
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

:::{tab-item} {{serverless-full}}
:sync: serverless

| Category| Security feature | Status | Description |
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

| Category| Security feature | Status | Description |
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

| Category| Security feature | Status | Description |
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