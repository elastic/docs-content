---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-default-azure-configurations.html
---

# Elasticsearch Add-On for Heroku Azure default provider instance configurations [ech-default-azure-configurations]

Following are the preferred instance types / machine configurations, storage types, disk to memory ratios, and virtual CPU to RAM ratios for all instance configurations available on {{ess}} and provided by Azure.

| Instance configuration | Preferred Instance Type or Machine Configuration1 | Storage Type1 | Disk:Memory Ratio2 | vCPU/RAM Ratio |
| --- | --- | --- | --- | --- |
| $$$azure.es.datahot.edsv4$$$ `azure.es.datahot.edsv4` | e8dsv4 | Standard Managed Disks (SSD) | 35:1 | 0.133 |
| $$$azure.es.datahot.ddv4$$$ `azure.es.datahot.ddv4` | d16dv4 | Standard Managed Disks (SSD) | 35:1 | 0.267 |
| $$$azure.es.datahot.fsv2$$$ `azure.es.datahot.fsv2` | f32sv2 | Standard Managed Disks (SSD) | 35:1 | 0.533 |
| $$$azure.es.datahot.lsv3$$$ `azure.es.datahot.lsv3` | l8sv3 | NVMe | 28:1 | 0.133 |
| $$$azure.es.datawarm.edsv4$$$ `azure.es.datawarm.edsv4` | e8dsv4 | Standard Managed Disks (HDD) | 200:1 | 0.133 |
| $$$azure.es.datacold.edsv4$$$ `azure.es.datacold.edsv4` | e8dsv4 | Standard Managed Disks (HDD) | 200:1 | 0.133 |
| $$$azure.es.datafrozen.edsv4$$$ `azure.es.datafrozen.edsv4` | e8dsv4 | Standard Managed Disks (SSD) | 90:1 | 0.133 |


## Additional instances [ech-additional-instances] 

Following are the preferred instance type / configuration and virtual CPU to RAM ratios for additional instance configurations available on {{ess}} and provided by Azure.

| Instance configuration | Preferred Instance Type or Machine Configuration1 | vCPU/RAM Ratio |
| --- | --- | --- |
| $$$azure.es.master.fsv2$$$`azure.es.master.fsv2` | f32sv2 | 0.533 |
| $$$azure.es.ml.fsv2$$$`azure.es.ml.fsv2` | f32sv2 | 0.533 |
| $$$azure.es.coordinating.fsv2$$$`azure.es.coordinating.fsv2` | f32sv2 | 0.533 |
| $$$azure.kibana.fsv2$$$`azure.kibana.fsv2` | f32sv2 | 0.533 |
| $$$azure.apm.fsv2$$$`azure.apm.fsv2` | f32sv2 | 0.533 |
| $$$azure.integrationsserver.fsv2$$$`azure.integrationsserver.fsv2` | f32sv2 | 0.533 |
| $$$azure.enterprisesearch.fsv2$$$`azure.enterprisesearch.fsv2` | f32sv2 | 0.533 |

1 Preferred instance and storage types are subject to provider availability. To learn more about our provider instances, check [AWS](https://aws.amazon.com/ec2/instance-types), [Azure](https://azure.microsoft.com/en-us/pricing/details/virtual-machines/series/), and [GCP](https://cloud.google.com/compute/docs/machine-types) reference pages.

2 Ratios are estimations.

## Regional availability of instances per Azure region [ech-azure-list-region]

The following table contains the complete list of instances available in Elastic Cloud deployments per Azure region:

| Regions | Instances |  |  |  |
| --- | --- | --- | --- | --- |
|  | Edsv4 | Ddv4 | Fsv2 | Lsv3 |
| Australia East (New South Wales) | ✓ | ✓ | ✓ | ✓ |
| Brazil South (São Paulo) | ✓ | ✓ | ✓ | ✓ |
| Canada Central (Toronto) | ✓ | ✓ | ✓ | ✓ |
| Central India (Pune) | ✓ | ✓ | ✓ | ✓ |
| Central US (Iowa) | ✓ | ✓ | ✓ |  |
| East US (Virginia) | ✓ | ✓ | ✓ | ✓ |
| East US 2 (Virginia) | ✓ | ✓ | ✓ | ✓ |
| France Central (Paris) | ✓ | ✓ | ✓ | ✓ |
| Japan East (Tokyo) | ✓ | ✓ | ✓ | ✓ |
| North Europe (Ireland) | ✓ | ✓ | ✓ | ✓ |
| South Africa North (Johannesburg) | ✓ | ✓ | ✓ |  |
| South Central US (Texas) | ✓ | ✓ | ✓ | ✓ |
| South East Asia (Singapore) | ✓ | ✓ | ✓ | ✓ |
| UK South (London) | ✓ | ✓ | ✓ | ✓ |
| West Europe (Netherlands) | ✓ | ✓ | ✓ | ✓ |
| West US 2 (Washington) | ✓ | ✓ | ✓ | ✓ |


