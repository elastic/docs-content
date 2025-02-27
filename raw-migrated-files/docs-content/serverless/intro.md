# Elastic Cloud Serverless [intro]

## Differences between serverless projects and hosted deployments on {{ecloud}} [general-what-is-serverless-elastic-differences-between-serverless-projects-and-hosted-deployments-on-ecloud]

You can run [hosted deployments](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md) of the {{stack}} on {{ecloud}}. These hosted deployments provide more provisioning and advanced configuration options.

|     |     |     |
| --- | --- | --- |
| Option | Serverless | Hosted |
| **Cluster management** | Fully managed by Elastic. | You provision and manage your hosted clusters. Shared responsibility with Elastic. |
| **Scaling** | Autoscales out of the box. | Manual scaling or autoscaling available for you to enable. |
| **Upgrades** | Automatically performed by Elastic. | You choose when to upgrade. |
| **Pricing** | Individual per project type and based on your usage. | Based on deployment size and subscription level. |
| **Performance** | Autoscales based on your usage. | Manual scaling. |
| **Solutions** | Single solution per project. | Full Elastic Stack per deployment. |
| **User management** | Elastic Cloud-managed users. | Elastic Cloud-managed users and native Kibana users. |
| **API support** | Subset of [APIs](https://www.elastic.co/docs/api). | All Elastic APIs. |
| **Backups** | Projects automatically backed up by Elastic. | Your responsibility with Snapshot & Restore. |
| **Data retention** | Editable on data streams. | Index Lifecycle Management. |

