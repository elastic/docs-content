---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-reference-hardware.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-aws-instance-configuration.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-default-aws-configurations.html
navigation_title: Hardware
applies_to:
  deployment:
    ess:
---

# {{heroku}} hardware [ech-reference-hardware]

{{ech}} deployments use a range of virtualized hardware resources from a cloud provider, such as Amazon EC2 (AWS). Instance configurations enable the products and features of the {{stack}} to run on suitable resources that support their intended purpose. For example, if you have a logging use case that benefits from large amounts of slower but more cost-efficient storage space, you can use large spindle drives rather than more expensive SSD storage. Each instance configuration provides a combination of CPU resources, memory, and storage, all of which you can scale from small to very large.

::::{note}
All instances are set to UTC timezone.
::::

The {{heroku}} runs exclusively on AWS. To understand the available hardware, refer to the following resources: 

* [The {{ech}} hardware overview](cloud://reference/cloud-hosted/hardware.md)
* [AWS hardware](cloud://reference/cloud-hosted/aws.md)
* [AWS default hardware](cloud://reference/cloud-hosted/aws-default.md)

Some hardware profiles might not be available in your region. To learn about regions used by the {{heroku}}, refer to [](/deploy-manage/deploy/elastic-cloud/heroku-reference-regions.md).