---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-default-aws-configurations.html
---

# Elasticsearch Add-On for Heroku AWS default provider instance configurations [ech-default-aws-configurations]

Following are the preferred instance types / machine configurations, storage types, disk to memory ratios, and virtual CPU to RAM ratios for all instance configurations available on {{ess}} and provided by AWS.

| Instance configuration | Preferred Instance Type or Machine Configuration1 | Storage Type1 | Disk:Memory Ratio2 | vCPU/RAM Ratio |
| --- | --- | --- | --- | --- |
| aws.es.datahot.i3 | i3 | NVMe | 30:1 | 0.138 |
| aws.es.datahot.i3en | i3en | NVMe | 80:1 | 0.133 |
| aws.es.datahot.m5d | m5d | NVMe | 10:1 | 0.267 |
| aws.es.datahot.m6gd | m6gd | NVMe | 15:1 | 0.267 |
| aws.es.datahot.c5d | c5d | NVMe | 12:1 | 0.529 |
| aws.es.datahot.c6gd | c6gd | NVMe | 30:1 | 0.533 |
| aws.es.datahot.r6gd | r6gd | NVMe | 6:1 | 0.133 |
| aws.es.datawarm.d2 | d2 | HDD | 160:1 | 0.138 |
| aws.es.datawarm.d3 | d3 | HDD | 190:1 | 0.133 |
| aws.es.datawarm.i3en | i3en | NVMe | 80:1 | 0.133 |
| aws.es.datacold.d2 | d2 | HDD | 160:1 | 0.138 |
| aws.es.datacold.d3 | d3 | HDD | 190:1 | 0.133 |
| aws.es.datacold.i3en | i3en | NVMe | 80:1 | 0.133 |
| aws.es.datafrozen.i3en | i3en | NVMe | 75:1 | 0.133 |


## Additional instances [ech-aws-additional-instances] 

Following are the preferred instance type / configuration and virtual CPU to RAM ratios for additional instance configurations available on {{ess}} and provided by AWS.

| Instance configuration | Preferred Instance Type or Machine Configuration1 | vCPU/RAM Ratio |
| --- | --- | --- |
| aws.es.master.c5d | c5d | 0.529 |
| aws.es.master.c6gd | c6gd | 0.533 |
| aws.es.ml.c5d | c5d | 0.529 |
| aws.es.ml.m5d | m5d | 0.267 |
| aws.es.ml.m6gd | m6gd | 0.267 |
| aws.es.coordinating.m5d | m5d | 0.267 |
| aws.es.coordinating.m6gd | m6gd | 0.267 |
| aws.kibana.c5d | c5d | 0.529 |
| aws.kibana.c6gd | c6gd | 0.533 |
| aws.apm.c5d | c5d | 0.529 |
| aws.integrationsserver.c5d | c5d | 0.529 |
| aws.enterprisesearch.c5d | c5d | 0.529 |

1 Preferred instance and storage types are subject to provider availability. To learn more about our provider instances, check the [AWS](https://aws.amazon.com/ec2/instance-types) reference page.

2 Ratios are estimations.

## Regional availability of instances per AWS region [aws-list-region]

The following table contains the complete list of instances available in Elastic Cloud deployments per AWS region:

| Regions | Instances |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | C5d | C6gd | C5n | M5dn | D2 | D3 | I3 | I3en | M5d | M6gd | R6gd |
| Africa (Cape Town) | ✓ |  |  |  | ✓ |  | ✓ | ✓ | ✓ |  |  |
| Asia Pacific (Hong Kong) | ✓ |  |  |  | ✓ |  | ✓ | ✓ | ✓ |  |  |
| Asia Pacific (Mumbai) | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Asia Pacific (Singapore) | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Asia Pacific (Seoul) | ✓ |  |  |  | ✓ |  | ✓ | ✓ | ✓ |  |  |
| Asia Pacific (Sydney) | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Asia Pacific (Tokyo) | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Canada (Central) | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ |  | ✓ |
| Europe (Frankfurt) | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Europe (Zurich) | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ | ✓ |  |
| Europe (Ireland) | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Europe (London) | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ | ✓ |  |
| Europe (Milan) | ✓ |  |  |  | ✓ |  | ✓ | ✓ | ✓ |  |  |
| Europe (Paris) | ✓ | ✓ |  |  | ✓ |  | ✓ | ✓ | ✓ |  | ✓ |
| Europe (Stockholm) | ✓ | ✓ |  |  | ✓ |  | ✓ | ✓ | ✓ | ✓ |  |
| Middle East (Bahrain) | ✓ |  |  |  | ✓ |  | ✓ | ✓ | ✓ |  |  |
| South America (São Paulo) | ✓ |  |  |  |  |  | ✓ | ✓ | ✓ |  |  |
| US East (N. Virginia) | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| US East (Ohio) | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| US West (N. California) | ✓ | ✓ |  |  | ✓ |  | ✓ | ✓ | ✓ | ✓ | ✓ |
| US West (Oregon) | ✓ | ✓ |  |  |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| US East GovCloud (N. Virginia) |  |  | ✓ | ✓ |  |  |  | ✓ |  |  |  |


