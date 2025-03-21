---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-reference-hardware.html
---

# Elasticsearch Add-On for Heroku hardware [ech-reference-hardware]

:::{image} /deploy-manage/images/cloud-heroku-ec-cloud-platform-hardware.png
:alt: A banner showing a plane trailing several stylized UI sliders superimposed over  cloud hardware
:::

Use this information to better understand how Elasticsearch Add-On for Heroku instance configurations (for example `azure.es.datahot.ddv4`, `gcp.es.datahot.n2.68x10x45`, or `aws.es.datahot.c6gd`) relate to the underlying cloud provider hardware that we use when you create your deployment.


## Instance configurations [ech-getting-started-configurations]

Deployments use a range of virtualized hardware resources from a cloud provider, such as Amazon EC2 (AWS), Google Compute Platform (GCP) or Microsoft Azure.  Instance configurations enable the products and features of the Elastic Stack to run on suitable resources that support their intended purpose. For example, if you have a logging use case that benefits from large amounts of slower but more cost-efficient storage space, you can use large spindle drives rather than more expensive SSD storage. Each instance configuration provides a combination of CPU resources, memory, and storage, all of which you can scale from small to very large.

::::{note}
All instances, regardless of the region or provider, are set to UTC timezone.
::::


To understand the naming convention of instance configuration per cloud provider, refer to [Azure instance configurations](ech-azure-instance-configuration.md), [GCP instance configurations](ech-gcp-instance-configuration.md) and [AWS instance configurations](ech-aws-instance-configuration.md).

::::{tip}
Instance configurations are an Elasticsearch Add-On for Heroku abstraction of virtualized resources from the provider, but you might recognize the underlying hardware they build on in the instance configuration name. We use *instance types* on AWS and Azure, and *custom machine types* on GCP. Elasticsearch Add-On for Heroku instance configurations are not the same as AWS instance types.
::::








