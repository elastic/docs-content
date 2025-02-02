---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-reference-regions.html
---

# Elasticsearch Add-On for Heroku regions [ech-reference-regions]

A region is the geographic area where the data center of the cloud provider that hosts your deployment is located. Use the information listed here to decide which Elasticsearch Add-On for Heroku region to use. Your choice should be based on:

* Your geographic proximity to the region. Picking a region that is closer to you typically reduces latency for indexing and search requests.
* The features that we support for the region. Not all regions support the same set of features.

Elasticsearch Add-On for Heroku handles all hosting details for you, no additional accounts with the underlying cloud provider required. The region you select cannot be changed after you create a deployment. If you want to use a different region later on, you can create a new deployment and reindex your data into it.

::::{tip} 
If you are not sure what to pick, choose a region that is geographically close to you to reduce latency. You should always use HTTPS to connect to the Elastic stack components of your deployment.
::::



## Amazon Web Services (AWS) regions [echamazon_web_services_aws_regions] 

The following AWS regions are available:

| Region | Name | Supports |
| --- | --- | --- |
| eu-west-1 | EU (Ireland) | HTTPS only |
| us-east-1 | US East (N. Virginia) | HTTPS only |

