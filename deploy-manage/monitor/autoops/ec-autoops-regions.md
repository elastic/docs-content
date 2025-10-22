---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-regions.html
navigation_title: Regions
applies_to:
  serverless:
  deployment:
    self:
    ece:
    eck:
    ess: all
products:
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# AutoOps regions [ec-autoops-regions]

A region is where a cloud service provider's data center hosts your deployments or clusters.

::::{note} 
AutoOps is currently not available in any region for GovCloud customers.
::::

## AutoOps for {{ECH}} regions

AutoOps for {{ECH}} is currently available in the following regions for AWS:

| Region | Name |
| --- | --- | --- | --- |
| us-east-1 | US East (N. Virginia) |
| us-east-2 | US East (Ohio) |
| us-west-1 | US West (N. California) |
| us-west-2 | US West (Oregon) |
| ca-central-1 | Canada (Central) |
| eu-west-1 | Europe (Ireland) |
| eu-west-2 | Europe (London) |
| eu-west-3 | Europe (Paris) |
| eu-north-1 | Europe (Stockholm) |
| eu-central-1 | Europe (Frankfurt) |
| eu-central-2 | Europe (Zurich) |
| eu-south-1 | Europe (Milan) |
| me-south-1 | Middle East (Bahrain) |
| ap-east-1 | Asia Pacific (Hong Kong) |
| ap-northeast-1 | Asia Pacific (Tokyo) |
| ap-northeast-2 | Asia Pacific (Seoul) |
| ap-southeast-1 | Asia Pacific (Singapore) |
| ap-southeast-2 | Asia Pacific (Sydney) |
| ap-south-1 | Asia Pacific (Mumbai) |
| sa-east-1 | South America (Sao Paulo) |
| af-south-1 | Africa (Cape Town) |

Regions for Azure and GCP are coming soon.

## AutoOps for {{serverless-full}} regions

AutoOps for serverless projects is currently available in the following regions for AWS:

| Region | Name |
| --- | --- | --- | --- |
| us-east-1 | US East (N. Virginia) |
| eu-west-1 | Europe (Ireland) |
| ap-southeast-1 | Asia Pacific (Singapore) |
| us-west-2 | US West (Oregon) |

The only exception is the **Search AI Lake** view, which is available in all CSP regions across AWS, Azure, and GCP.

## AutoOps for self-managed clusters regions

You can also use AutoOps with your ECE ({{ece}}), ECK ({{eck}}), or self-managed clusters through [Cloud Connect](/deploy-manage/cloud-connect.md). 

This service is currently available in the following regions for AWS:

:::{include} ../_snippets/autoops-cc-regions.md
:::
