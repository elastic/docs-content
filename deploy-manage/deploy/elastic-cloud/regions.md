---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/regions.html
applies_to:
  serverless:
---

# Regions [regions]

A region is the geographic area where the data center of the cloud provider that hosts your project is located. Review the available Elastic Cloud Serverless regions to decide which region to use. If you aren’t sure which region to pick, choose one that is geographically close to you to reduce latency.

Elastic Cloud Serverless handles all hosting details for you. You are unable to change the region after you create a project.

::::{note} 
Currently, a limited number of Amazon Web Services (AWS) and Microsoft Azure regions are available. More regions for AWS and Azure, as well as Google Cloud Platform (GCP), will be added in the future.

::::



## Amazon Web Services (AWS) regions [regions-amazon-web-services-aws-regions]

The following AWS regions are currently available:

| Region | Name |
| :--- | :--- |
| ap-southeast-1 | Asia Pacific (Singapore) |
| eu-west-1 | Europe (Ireland) |
| us-east-1 | US East (N. Virginia) |
| us-west-2 | US West (Oregon) |

## Microsoft Azure regions [regions-azure-regions]

```yaml {applies_to}
serverless: preview
```

The following Azure regions are currently available:

| Region | Name |
| :--- | :--- |
| eastus | East US |