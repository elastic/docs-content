---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/regions.html
applies_to:
  serverless:
products:
  - id: cloud-serverless
---

# Regions [regions]

A region is the geographic area where the data center of the cloud provider that hosts your project is located. Review the available {{serverless-full}} regions to decide which region to use. If you aren’t sure which region to pick, choose one that is geographically close to you to reduce latency.

{{serverless-full}} handles all hosting details for you. You are unable to change the region after you create a project.

::::{note} 
Currently, a limited number of Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP) regions are available. More regions for AWS, Azure, and GCP, will be added in the future.

::::



## Amazon Web Services (AWS) regions [regions-amazon-web-services-aws-regions]

The following AWS regions are currently available:

| Region | Name |
| :--- | :--- |
| ap-northeast-1 | Asia Pacific (Tokyo) |
| ap-southeast-1 | Asia Pacific (Singapore) |
| eu-central-1 | Europe (Frankfurt) |
| eu-west-1 | Europe (Ireland) |
| eu-west-2 | Europe (London) |
| us-east-1 | US East (N. Virginia) |
| us-east-2 | US East (Ohio) |
| us-west-2 | US West (Oregon) |


## Microsoft Azure regions [regions-azure-regions]

The following Azure regions are currently available:

| Region | Name |
| :--- | :--- |
| eastus | East US |
| northeurope | North Europe |
| australiaeast | Australia East |
| westus2 | West US 2 |

## Google Cloud Platform (GCP) regions [regions-gcp-regions]

The following GCP regions are currently available:

| Region | Name |
| :--- | :--- |
| asia-south1 | Mumbai |
| europe-west1 | Belgium |
| us-central1 | Iowa |
| us-east1 | South Carolina |
| us-east4 | Virginia |
| us-west1 | Oregon |

## Marketplaces

When procuring {{ecloud}} through [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-voru33wi6xs7k), [Azure Marketplace](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/elastic.ec-azure-pp?tab=overview), or [GCP Marketplace](https://console.cloud.google.com/marketplace/product/elastic-prod/elastic-cloud), only the regions corresponding to the same cloud service provider can be used. This ensures that you can enjoy the benefits of the marketplace, such as {{ecloud}} contributing towards your spend commitment with cloud providers.

You can implement a multi-cloud strategy by creating a separate {{ecloud}} organization, either from another marketplace, or directly at [cloud.elastic.co](https://cloud.elastic.co).
For example, if you have created a project in `eu-central-1` after signing up on AWS Marketplace, you can provision another project in GCP `europe-west1` by signing up for a second {{ecloud}} organization on GCP Marketplace, using another email address.
