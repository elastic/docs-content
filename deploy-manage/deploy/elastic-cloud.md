---
applies_to:
  serverless: ga
  deployment:
    ess: ga
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/intro.html#general-what-is-serverless-elastic-differences-between-serverless-projects-and-hosted-deployments-on-ecloud
---

# Elastic Cloud [intro]

{{ecloud}} allows you to centrally manage [hosted deployments](elastic-cloud/cloud-hosted.md) of the {{stack}} and [serverless projects](elastic-cloud/serverless.md) for your Observability, Security, and Search use cases. 

These hosted deployments and serverless projects are hosted on Elastic Cloud, through the cloud provider and regions of your choice, and are tied to your organization account.

You can check the operational status of {{ecloud}} at any time from [status.elastic.co](https://status.elastic.co/).

## Sign up

You can get started by creating an {{ecloud}} organization on [cloud.elastic.co](https://cloud.elastic.co/registration).

For more details on the available sign up options and trial information, go to [](elastic-cloud/create-an-organization.md).

## Benefits of {{ecloud}}

Some of the unique benefits of {{ecloud}} include:

- Regular updates and improvements automatically deployed or made available.
- Built-in security, including encryption at rest.
- Central management of billing and licensing.
- Built-in tools for monitoring and scaling your {{ecloud}} resources.
- Central management of users, roles, and authentication, including integration with SSO providers.

For more information, refer to [](/deploy-manage/cloud-organization.md).

## Differences between serverless projects and hosted deployments[general-what-is-serverless-elastic-differences-between-serverless-projects-and-hosted-deployments-on-ecloud]

You can have multiple hosted deployments and serverless projects in the same {{ecloud}} organization, and each deployment type has its own specificities.


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

## APIs

{{ecloud}} offers APIs to manage your organization and its resources. Check the [{{ecloud}}](https://www.elastic.co/docs/api/doc/cloud/) and [{{ecloud}} serverless](https://www.elastic.co/docs/api/doc/elastic-cloud-serverless/) APIs.

More tools are available for you to make the most of your {{ecloud}} organization and {{es}}. Refer to [](/deploy-manage/deploy/elastic-cloud/tools-apis.md).