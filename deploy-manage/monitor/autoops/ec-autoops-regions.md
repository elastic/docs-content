---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-regions.html
navigation_title: Regions
applies_to:
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

## AutoOps for {{ECH}} regions

AutoOps for {{ECH}} is currently available in the following regions for AWS:

| Region | Name |
| --- | --- | --- | --- |
| us-east-1 | N. Virginia |
| us-east-2 | Ohio |
| us-west-1 | N. California |
| us-west-2 | Oregon |
| ca-central-1 | Canada |
| eu-west-1 | Ireland |
| eu-west-2 | London |
| eu-west-3 | Paris |
| eu-north-1 | Stockholm |
| eu-central-1 | Frankfurt |
| eu-central-2 | Zurich |
| eu-south-1 | Milan |
| me-south-1 | Bahrain |
| ap-east-1 | Hong Kong |
| ap-northeast-1 | Tokyo |
| ap-northeast-2 | Seoul |
| ap-southeast-1 | Singapore |
| ap-southeast-2 | Sydney |
| ap-south-1 | Mumbai |
| sa-east-1 | Sao Paulo |
| af-south-1 | Cape Town |

Regions for Azure and GCP are coming soon.

## AutoOps for self-managed clusters regions

You can also use AutoOps with your ECE ({{ece}}), ECK ({{eck}}), or self-managed clusters through [Cloud Connect](/deploy-manage/cloud-connect.md). 

This service is currently available in the following regions for AWS:

:::{include} ../_snippets/autoops-cc-regions.md
:::

<br>
::::{note} 
AutoOps is currently not available for GovCloud customers.
::::
